import ctypes
import numpy

from . import wrapper, opencl
from . import dll

__all__ = [
    "Vector"
]


class Vector:
    def __init__(self, n: int, x: list):
        self.wrapper = wrapper.singleton

        self.vector = dll.ClsparseDenseVector()
        status = self.wrapper.clsparse_loaded_dll.clsparseInitVector(ctypes.byref(self.vector))
        dll.check(status)

        status = ctypes.c_int(0)
        self.vector.values = self.wrapper.opencl_loaded_dll.clCreateBuffer(self.wrapper.context,
                                                                           ctypes.c_int(opencl.map_flags("CL_MEM_READ_WRITE | CL_MEM_USE_HOST_PTR")),
                                                                           n * ctypes.sizeof(ctypes.c_float),
                                                                           (ctypes.c_float * n)(*x),
                                                                           ctypes.byref(status))
        opencl.check(status.value)
        self.vector.num_values = ctypes.c_ulong(n)

    # def __del__(self):
    #     pass

    def some_info(self):
        ofs = getattr(dll.ClsparseDenseVector, "values").offset
        print("ofs", ofs)
        p = ctypes.pointer(ctypes.c_void_p.from_buffer(self.vector, ofs))
        print(p, p.contents)
        _address = ctypes.cast(p, ctypes.c_void_p).value
        print("adr", _address)
        _array_type = ctypes.c_float * self.vector.num_values
        a = numpy.frombuffer(_array_type.from_address(_address), dtype="float32")
        print("array", a)
        a = numpy.frombuffer(_array_type.from_address(self.vector.values), dtype="float32")
        print("array", a)

        k = ctypes.c_void_p.from_address(self.vector.values)
        print(k)
