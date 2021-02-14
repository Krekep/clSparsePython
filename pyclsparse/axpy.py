import ctypes

from pyclsparse import vector, scalar, wrapper, dll

__all__ = [
    "axpy"
]


def axpy(result_vector: vector.Vector, a: scalar.Scalar, x: vector.Vector, y: vector.Vector):
    status = wrapper.clsparse_dll.cldenseSaxpy(
        ctypes.byref(result_vector.vector),
        ctypes.byref(a.scalar),
        ctypes.byref(x.vector),
        ctypes.byref(y.vector),
        wrapper.create_result.clsparseControl
    )
    dll.check(status)
