import ctypes

from . import wrapper, opencl
from . import dll

__all__ = [
    "Vector"
]


class Vector:
    """
    This class represents a wrapper over the clsparseDenseVector class
    """
    def __init__(self, n: int, x: list):
        self.wrapper = wrapper.singleton

        self.vector = dll.ClsparseDenseVector()
        status = self.wrapper.clsparse_loaded_dll.clsparseInitVector(ctypes.byref(self.vector))
        dll.check(status)

        status = ctypes.c_int(0)
        self.vector.values = self.wrapper.opencl_loaded_dll.clCreateBuffer(
            self.wrapper.context,
            ctypes.c_int(opencl.map_flags("CL_MEM_READ_WRITE | CL_MEM_USE_HOST_PTR")),
            n * ctypes.sizeof(ctypes.c_float),
            (ctypes.c_float * n)(*x),
            ctypes.byref(status))
        opencl.check(status.value)
        self.vector.num_values = ctypes.c_ulong(n)

    def get_values(self) -> list:
        """
        Function returns vector values
        :return:
        """
        result = (ctypes.c_float * self.vector.num_values)()
        status = self.wrapper.opencl_loaded_dll.clEnqueueReadBuffer(
            wrapper.command_queue,
            self.vector.values,
            ctypes.c_bool(True),
            0,
            ctypes.c_int(self.vector.num_values * ctypes.sizeof(ctypes.c_float)),
            result,
            0,
            None,
            None
        )
        opencl.check(status)
        ret = list()
        for i in range(self.vector.num_values):
            ret.append(result[i])
        return ret

    # def __del__(self):
    #     pass
