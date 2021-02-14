import ctypes

from . import wrapper, opencl
from . import dll

__all__ = [
    "Scalar"
]


class Scalar:
    def __init__(self, x: float):
        self.wrapper = wrapper.singleton

        self.scalar = dll.ClsparseScalar()
        status = self.wrapper.clsparse_loaded_dll.clsparseInitScalar(ctypes.byref(self.scalar))
        dll.check(status)

        status = ctypes.c_int(0)
        self.scalar.values = self.wrapper.opencl_loaded_dll.clCreateBuffer(
            self.wrapper.context,
            ctypes.c_int(opencl.map_flags("CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR")),
            ctypes.sizeof(ctypes.c_float),
            ctypes.pointer(ctypes.c_float(x)),
            ctypes.byref(status))
        opencl.check(status.value)

    # def __del__(self):
    #     pass