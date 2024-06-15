import numpy as np
from typing import Tuple, Dict

from scipy.ndimage import map_coordinates

from tme.types import ArrayLike
from tme.backends import backend
from tme.matching_data import MatchingData
from tme.matching_exhaustive import _normalize_under_mask


class MatchDensityToDensity:
    def __init__(
        self,
        matching_data: "MatchingData",
        pad_target_edges: bool = False,
        pad_fourier: bool = False,
        rotate_mask: bool = True,
        interpolation_order: int = 1,
        negate_score: bool = False,
    ):
        self.rotate_mask = rotate_mask
        self.interpolation_order = interpolation_order

        target_pad = matching_data.target_padding(pad_target=pad_target_edges)
        matching_data = matching_data.subset_by_slice(target_pad=target_pad)

        fast_shape, fast_ft_shape, fourier_shift = matching_data.fourier_padding(
            pad_fourier=pad_fourier
        )

        self.target = backend.topleft_pad(matching_data.target, fast_shape)
        self.target_mask = matching_data.target_mask

        self.template = matching_data.template
        self.template_rot = backend.preallocate_array(
            fast_shape, backend._default_dtype
        )

        self.template_mask, self.template_mask_rot = 1, 1
        rotate_mask = False if matching_data.template_mask is None else rotate_mask
        if matching_data.template_mask is not None:
            self.template_mask = matching_data.template_mask
            self.template_mask_rot = backend.topleft_pad(
                matching_data.template_mask, fast_shape
            )

        self.score_sign = -1 if negate_score else 1

    @staticmethod
    def rigid_transform(
        arr,
        rotation_matrix,
        translation,
        arr_mask=None,
        out=None,
        out_mask=None,
        order: int = 1,
        use_geometric_center: bool = False,
    ):
        rotate_mask = arr_mask is not None
        return_type = (out is None) + 2 * rotate_mask * (out_mask is None)
        translation = np.zeros(arr.ndim) if translation is None else translation

        center = np.floor(np.array(arr.shape) / 2)[:, None]
        grid = np.indices(arr.shape, dtype=np.float32).reshape(arr.ndim, -1)
        np.subtract(grid, center, out=grid)
        np.matmul(rotation_matrix.T, grid, out=grid)
        np.add(grid, center, out=grid)

        if out is None:
            out = np.zeros_like(arr)

        map_coordinates(arr, grid, order=order, output=out.ravel())

        if out_mask is None and arr_mask is not None:
            out_mask = np.zeros_like(arr_mask)

        if arr_mask is not None:
            map_coordinates(arr_mask, grid, order=order, output=out_mask.ravel())

        match return_type:
            case 0:
                return None
            case 1:
                return out
            case 2:
                return out_mask
            case 3:
                return out, out_mask

    @staticmethod
    def angles_to_rotationmatrix(angles: Tuple[float]) -> ArrayLike:
        angles = backend.to_numpy_array(angles)
        rotation_matrix = euler_to_rotationmatrix(angles)
        return backend.to_backend_array(rotation_matrix)

    def format_translation(self, translation: Tuple[float] = None) -> ArrayLike:
        if translation is None:
            return backend.zeros(self.template.ndim, backend._default_dtype)

        return backend.to_backend_array(translation)

    def score_translation(self, x: Tuple[float]) -> float:
        translation = self.format_translation(x)
        rotation_matrix = self.angles_to_rotationmatrix((0, 0, 0))

        return self(translation=translation, rotation_matrix=rotation_matrix)

    def score_angles(self, x: Tuple[float]) -> float:
        translation = self.format_translation(None)
        rotation_matrix = self.angles_to_rotationmatrix(x)

        return self(translation=translation, rotation_matrix=rotation_matrix)

    def score(self, x: Tuple[float]) -> float:
        split = len(x) // 2
        translation, angles = x[:split], x[split:]

        translation = self.format_translation(translation)
        rotation_matrix = self.angles_to_rotationmatrix(angles)

        return self(translation=translation, rotation_matrix=rotation_matrix)


class FLC(MatchDensityToDensity):
    def __init__(self, **kwargs: Dict):
        super().__init__(**kwargs)

        if self.target_mask is not None:
            backend.multiply(self.target, self.target_mask, out=self.target)

        self.target_square = backend.square(self.target)

        _normalize_under_mask(
            template=self.template,
            mask=self.template_mask,
            mask_intensity=backend.sum(self.template_mask),
        )

        self.template = backend.reverse(self.template)
        self.template_mask = backend.reverse(self.template_mask)

    def __call__(self, translation: ArrayLike, rotation_matrix: ArrayLike) -> float:
        if self.rotate_mask:
            self.rigid_transform(
                arr=self.template,
                arr_mask=self.template_mask,
                rotation_matrix=rotation_matrix,
                translation=translation,
                out=self.template_rot,
                out_mask=self.template_mask_rot,
                use_geometric_center=False,
                order=self.interpolation_order,
            )
        else:
            self.rigid_transform(
                arr=self.template,
                rotation_matrix=rotation_matrix,
                translation=translation,
                out=self.template_rot,
                use_geometric_center=False,
                order=self.interpolation_order,
            )
        n_observations = backend.sum(self.template_mask_rot)

        _normalize_under_mask(
            template=self.template_rot,
            mask=self.template_mask_rot,
            mask_intensity=n_observations,
        )

        ex2 = backend.sum(
            backend.divide(
                backend.sum(
                    backend.multiply(self.target_square, self.template_mask_rot),
                ),
                n_observations,
            )
        )
        e2x = backend.square(
            backend.divide(
                backend.sum(backend.multiply(self.target, self.template_mask_rot)),
                n_observations,
            )
        )

        denominator = backend.maximum(backend.subtract(ex2, e2x), 0.0)
        denominator = backend.sqrt(denominator)
        denominator = backend.multiply(denominator, n_observations)

        overlap = backend.sum(backend.multiply(self.template_rot, self.target))

        score = backend.divide(overlap, denominator) * self.score_sign
        return score
