import ctypes

from . import wrapper, opencl
from . import dll

__all__ = [
    "Scalar"
]


class Scalar:
    """
    This class represents a wrapper over the clsparseScalar class
    """
    def __init__(self, x: float):
        self.wrapper = wrapper.singleton

        self.scalar = dll.ClsparseScalar()
        status = self.wrapper.clsparse_loaded_dll.clsparseInitScalar(ctypes.byref(self.scalar))
        dll.check(status)

        status = ctypes.c_int(0)
        self.scalar.value = self.wrapper.opencl_loaded_dll.clCreateBuffer(
            self.wrapper.context,
            ctypes.c_int(opencl.map_flags("CL_MEM_READ_ONLY | CL_MEM_USE_HOST_PTR")),
            ctypes.sizeof(ctypes.c_float),
            ctypes.pointer(ctypes.c_float(x)),
            ctypes.byref(status))
        opencl.check(status.value)

    # def __del__(self):
    #     pass

    def get_value(self) -> float:
        """
        Function return a value of scalar
        :return:
        """
        result = (ctypes.c_float * 1)()
        status = self.wrapper.opencl_loaded_dll.clEnqueueReadBuffer(
            wrapper.command_queue,
            self.scalar.value,
            ctypes.c_bool(True),
            0,
            ctypes.sizeof(ctypes.c_float),
            result,
            0,
            None,
            None
        )
        opencl.check(status)
        return result[0]
