import ctypes
import os

import numpy

from . import wrapper, opencl
from . import dll

__all__ = [
    "Matrix"
]


class Matrix:
    def __init__(self, path_to_matrix: str):
        byte_path = path_to_matrix.encode('utf-8')

        self.wrapper = wrapper.singleton
        _header = self._read_header(byte_path)

        self.matrix = dll.ClsparseCsrMatrix()
        status = self.wrapper.clsparse_loaded_dll.clsparseInitCsrMatrix(ctypes.byref(self.matrix))
        dll.check(status)

        self.matrix.num_rows = _header[0]
        self.matrix.num_cols = _header[1]
        self.matrix.num_nonzeros = _header[2]
        status = ctypes.c_int(0)

        self.matrix.values = self.wrapper.opencl_loaded_dll.clCreateBuffer(self.wrapper.context,
                                                                           ctypes.c_int(opencl.map_flags("CL_MEM_READ_WRITE")),
                                                                           ctypes.c_uint(self.matrix.num_nonzeros
                                                                                         * ctypes.sizeof(ctypes.c_float)),
                                                                           None,
                                                                           ctypes.byref(status))
        opencl.check(status.value)
        self.matrix.col_indices = self.wrapper.opencl_loaded_dll.clCreateBuffer(self.wrapper.context,
                                                                                ctypes.c_int(opencl.map_flags("CL_MEM_READ_WRITE")),
                                                                                ctypes.c_uint(
                                                                                    self.matrix.num_nonzeros
                                                                                    * ctypes.sizeof(ctypes.c_ulong)),
                                                                                # perhaps c_uint
                                                                                None,
                                                                                ctypes.byref(status))
        opencl.check(status.value)
        self.matrix.row_pointer = self.wrapper.opencl_loaded_dll.clCreateBuffer(self.wrapper.context,
                                                                                ctypes.c_int(opencl.map_flags("CL_MEM_READ_WRITE")),
                                                                                ctypes.c_uint(
                                                                                    (self.matrix.num_rows + 1)
                                                                                    * ctypes.sizeof(ctypes.c_ulong)),
                                                                                # perhaps c_uint
                                                                                None,
                                                                                ctypes.byref(status))
        opencl.check(status.value)
        # self.some_info()
        status = self.wrapper.clsparse_loaded_dll.clsparseSCsrMatrixfromFile(ctypes.byref(self.matrix),
                                                                             byte_path,
                                                                             wrapper.create_result.clsparseControl,
                                                                             ctypes.c_bool(True))
        dll.check(status.value)

    # def __del__(self):
    #     dll.check(self.wrapper.loaded_dll.CuBool_Matrix_Free(wrapper.instance, self.hnd))

    def _read_header(self, byte_path):
        nnz = ctypes.c_ulong(0)
        nrow = ctypes.c_ulong(0)
        ncol = ctypes.c_ulong(0)

        status = self.wrapper.clsparse_loaded_dll.clsparseHeaderfromFile(ctypes.pointer(nnz),
                                                                         ctypes.pointer(nrow),
                                                                         ctypes.pointer(ncol),
                                                                         byte_path)
        dll.check(status)
        return nrow, ncol, nnz

    def some_info(self):
        fields = ["num_rows", "num_cols", "num_nonzeros", "values", "col_indices",
                  "row_pointer", "off_values", "off_col_indices", "off_row_pointer", "meta"]
        for i in range(len(fields)):
            ofs = getattr(dll.ClsparseCsrMatrix, fields[i]).offset
            print("ofs", fields[i], ofs)
            p = ctypes.pointer(ctypes.c_void_p.from_buffer(self.matrix, ofs))
            print(p, p.contents)
            print()

        k = ctypes.c_void_p.from_address(self.matrix.values)
        print(k)

        print(self.matrix)
