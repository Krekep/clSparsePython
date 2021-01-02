import ctypes

from . import wrapper
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
        self.matrix.num_rows = _header[0]
        self.matrix.num_cols = _header[1]
        self.matrix.num_nonzeros = _header[2]
        status = ctypes.c_int(0)
        self.matrix.values = self.wrapper.opencl_loaded_dll.clCreateBuffer(self.wrapper.context,
                                                                           ctypes.c_int(4),  # CL_MEM_READ_ONLY
                                                                           ctypes.c_int(self.matrix.num_nonzeros
                                                                                        * ctypes.sizeof(ctypes.c_float)),
                                                                           None,
                                                                           ctypes.byref(status))
        dll.check(status.value)
        self.matrix.col_indices = self.wrapper.opencl_loaded_dll.clCreateBuffer(self.wrapper.context,
                                                                                ctypes.c_int(4),  # CL_MEM_READ_ONLY
                                                                                ctypes.c_int(
                                                                                    self.matrix.num_nonzeros
                                                                                    * ctypes.sizeof(ctypes.c_ulong)),
                                                                                # perhaps c_uint
                                                                                None,
                                                                                ctypes.byref(status))
        dll.check(status.value)
        self.matrix.row_pointer = self.wrapper.opencl_loaded_dll.clCreateBuffer(self.wrapper.context,
                                                                                ctypes.c_int(4),  # CL_MEM_READ_ONLY
                                                                                ctypes.c_int(
                                                                                    (self.matrix.num_rows + 1)
                                                                                    * ctypes.sizeof(ctypes.c_ulong)),
                                                                                # perhaps c_uint
                                                                                None,
                                                                                ctypes.byref(status))
        dll.check(status.value)
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
