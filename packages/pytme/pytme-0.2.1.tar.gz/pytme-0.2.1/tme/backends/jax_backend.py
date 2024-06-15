""" Backend using jax for template matching.

    Copyright (c) 2023 European Molecular Biology Laboratory

    Author: Valentin Maurer <valentin.maurer@embl-hamburg.de>
"""
from typing import Tuple, Callable

from .npfftw_backend import NumpyFFTWBackend

class JaxBackend(NumpyFFTWBackend):
    def __init__(
        self, float_dtype=None, complex_dtype=None, int_dtype=None, **kwargs
    ):
        import jax.scipy as jsp
        import jax.numpy as jnp

        float_dtype = jnp.float32 if float_dtype is None else float_dtype
        complex_dtype = jnp.complex64 if complex_dtype is None else complex_dtype
        int_dtype = jnp.int32 if int_dtype is None else int_dtype

        self.scipy = jsp
        super().__init__(
            array_backend=jnp,
            float_dtype=float_dtype,
            complex_dtype=complex_dtype,
            int_dtype=int_dtype,
        )

    def to_backend_array(self, arr):
        return self._array_backend.asarray(arr)

    def preallocate_array(self, shape: Tuple[int], dtype: type):
        arr = self._array_backend.zeros(shape, dtype=dtype)
        return arr

    def topleft_pad(self, arr, shape: Tuple[int], padval: int = 0):
        b = self.preallocate_array(shape, arr.dtype)
        self.add(b, padval, out=b)
        aind = [slice(None, None)] * arr.ndim
        bind = [slice(None, None)] * arr.ndim
        for i in range(arr.ndim):
            if arr.shape[i] > shape[i]:
                aind[i] = slice(0, shape[i])
            elif arr.shape[i] < shape[i]:
                bind[i] = slice(0, arr.shape[i])
        b = b.at[tuple(bind)].set(arr[tuple(aind)])
        return b


    def add(self, x1, x2, out = None, *args, **kwargs):
        x1 = self.to_backend_array(x1)
        x2 = self.to_backend_array(x2)
        ret = self._array_backend.add(x1, x2, *args, **kwargs)

        if out is not None:
            out = out.at[:].set(ret)
        return ret

    def subtract(self, x1, x2, out = None, *args, **kwargs):
        x1 = self.to_backend_array(x1)
        x2 = self.to_backend_array(x2)
        ret = self._array_backend.subtract(x1, x2, *args, **kwargs)
        if out is not None:
            out = out.at[:].set(ret)
        return ret

    def multiply(self, x1, x2, out = None, *args, **kwargs):
        x1 = self.to_backend_array(x1)
        x2 = self.to_backend_array(x2)
        ret = self._array_backend.multiply(x1, x2, *args, **kwargs)
        if out is not None:
            out = out.at[:].set(ret)
        return ret

    def divide(self, x1, x2, out = None, *args, **kwargs):
        x1 = self.to_backend_array(x1)
        x2 = self.to_backend_array(x2)
        ret = self._array_backend.divide(x1, x2, *args, **kwargs)
        if out is not None:
            out = out.at[:].set(ret)
        return ret

    def fill(self, arr, value: float) -> None:
        arr.at[:].set(value)


    def build_fft(
        self,
        fast_shape: Tuple[int],
        fast_ft_shape: Tuple[int],
        inverse_fast_shape: Tuple[int] = None,
        **kwargs,
    ) -> Tuple[Callable, Callable]:
        """
        Build fft builder functions.

        Parameters
        ----------
        fast_shape : tuple
            Tuple of integers corresponding to fast convolution shape
            (see :py:meth:`PytorchBackend.compute_convolution_shapes`).
        fast_ft_shape : tuple
            Tuple of integers corresponding to the shape of the Fourier
            transform array (see :py:meth:`PytorchBackend.compute_convolution_shapes`).
        inverse_fast_shape : tuple, optional
            Output shape of the inverse Fourier transform. By default fast_shape.
        **kwargs : dict, optional
            Unused keyword arguments.

        Returns
        -------
        tuple
            Tupple containing callable rfft and irfft object.
        """
        if inverse_fast_shape is None:
            inverse_fast_shape = fast_shape

        def rfftn(
            arr, out, shape: Tuple[int] = fast_shape
        ) -> None:
            out = out.at[:].set(self._array_backend.fft.rfftn(arr, s=shape))

        def irfftn(
            arr, out, shape: Tuple[int] = inverse_fast_shape
        ) -> None:
            out = out.at[:].set(self._array_backend.fft.irfftn(arr, s=shape))

        return rfftn, irfftn

    def sharedarr_to_arr(self, shm, shape: Tuple[int], dtype: str):
        return shm

    @staticmethod
    def arr_to_sharedarr(arr, shared_memory_handler: type = None):
        return arr

    def rotate_array(
        self,
        arr,
        rotation_matrix,
        arr_mask = None,
        translation = None,
        use_geometric_center: bool = False,
        out = None,
        out_mask = None,
        order: int = 3,
    ) -> None:
        rotate_mask = arr_mask is not None
        return_type = (out is None) + 2 * rotate_mask * (out_mask is None)
        translation = self.zeros(arr.ndim) if translation is None else translation

        indices = self._array_backend.indices(arr.shape).reshape(
            (len(arr.shape), -1)
        ).astype(self._float_dtype)

        center = self.divide(arr.shape, 2)
        if not use_geometric_center:
            center = self.center_of_mass(arr, cutoff=0)
        center = center[:, None]
        indices = indices.at[:].add(-center)
        rotation_matrix = self._array_backend.linalg.inv(rotation_matrix)
        indices = self._array_backend.matmul(rotation_matrix, indices)
        indices = indices.at[:].add(center)

        out = self.zeros_like(arr) if out is None else out
        out_slice = tuple(slice(0, stop) for stop in arr.shape)

        out = out.at[out_slice].set(
            self.scipy.ndimage.map_coordinates(
                arr, indices, order=order
            ).reshape(arr.shape)
        )

        if rotate_mask:
            out_mask = self.zeros_like(arr_mask) if out_mask is None else out_mask
            out_mask_slice = tuple(slice(0, stop) for stop in arr_mask.shape)
            out_mask = out_mask.at[out_mask_slice].set(
                self.scipy.ndimage.map_coordinates(
                    arr_mask, indices, order=order
                ).reshape(arr.shape)
            )

        match return_type:
            case 0:
                return None
            case 1:
                return out
            case 2:
                return out_mask
            case 3:
                return out, out_mask

    def max_score_over_rotations(
        self,
        score_space,
        internal_scores,
        internal_rotations,
        rotation_index: int,
    ):
        """
        Modify internal_scores and internal_rotations inplace with scores and rotation
        index respectively, wherever score_sapce is larger than internal scores.

        Parameters
        ----------
        score_space : CupyArray
            The score space to compare against internal_scores.
        internal_scores : CupyArray
            The internal scores to update with maximum scores.
        internal_rotations : CupyArray
            The internal rotations corresponding to the maximum scores.
        rotation_index : int
            The index representing the current rotation.
        """
        indices = score_space > internal_scores
        internal_scores.at[indices].set(score_space[indices])
        internal_rotations.at[indices].set(rotation_index)
