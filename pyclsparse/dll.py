import ctypes

__all__ = [
    "ClsparseCreateResult",
    "clsparse_load_and_configure",
    "check",
    "ClsparseCsrMatrix"
]


class ClsparseCreateResult(ctypes.Structure):
    _fields_ = [("clsparseStatus", ctypes.c_int),
                ("clsparseControl", ctypes.c_void_p)]


class ClsparseCsrMatrix(ctypes.Structure):
    _fields_ = [("num_rows", ctypes.c_ulong),
                ("num_cols", ctypes.c_ulong),
                ("num_nonzeros", ctypes.c_ulong),
                ("values", ctypes.c_void_p),
                ("col_indices", ctypes.c_void_p),
                ("row_pointer", ctypes.c_void_p),
                ("off_values", ctypes.c_ulong),
                ("off_col_indices", ctypes.c_ulong),
                ("off_row_pointer", ctypes.c_ulong),
                ("meta", ctypes.c_void_p)]


class ClsparseScalar(ctypes.Structure):
    _fields_ = [("value", ctypes.c_void_p),
                ("off_value", ctypes.c_ulong)]


class ClsparseDenseVector(ctypes.Structure):
    _fields_ = [("num_values", ctypes.c_ulong),
                ("values", ctypes.c_void_p),
                ("off_values", ctypes.c_ulong)]


def clsparse_load_and_configure(clsparse_lib_path: str):
    """
    Definition of signatures of functions of the clSPARSE library
    :param clsparse_lib_path:
    :return:
    """
    lib = ctypes.cdll.LoadLibrary(clsparse_lib_path)

    lib.clsparseSetup.restype = ctypes.c_uint

    lib.clsparseCreateControl.restype = ClsparseCreateResult
    lib.clsparseCreateControl.argtypes = [ctypes.c_void_p]  # opencl command queue

    lib.clsparseInitCsrMatrix.restype = ctypes.c_int
    lib.clsparseInitCsrMatrix.argtypes = [ctypes.POINTER(ClsparseCsrMatrix)]

    lib.clsparseInitVector.restype = ctypes.c_int
    lib.clsparseInitVector.argtypes = [ctypes.POINTER(ClsparseDenseVector)]

    lib.clsparseInitScalar.restype = ctypes.c_int
    lib.clsparseInitScalar.argtypes = [ctypes.POINTER(ClsparseScalar)]

    lib.clsparseHeaderfromFile.restype = ctypes.c_int
    lib.clsparseHeaderfromFile.argtypes = [ctypes.POINTER(ctypes.c_ulong),
                                           ctypes.POINTER(ctypes.c_ulong),
                                           ctypes.POINTER(ctypes.c_ulong),
                                           ctypes.c_char_p]

    lib.clsparseSCsrMatrixfromFile.restype = ctypes.c_int
    lib.clsparseSCsrMatrixfromFile.argtypes = [ctypes.POINTER(ClsparseCsrMatrix),
                                               ctypes.c_char_p,
                                               ctypes.c_void_p,
                                               ctypes.c_bool]

    lib.cldenseSaxpy.restype = ctypes.c_int
    lib.cldenseSaxpy.argtype = [ctypes.POINTER(ClsparseDenseVector),
                                ctypes.POINTER(ClsparseScalar),
                                ctypes.POINTER(ClsparseDenseVector),
                                ctypes.POINTER(ClsparseDenseVector),
                                ctypes.c_void_p]

    return lib


"""
Error codes from the clSPARSE library 
"""
_status_codes_mappings = {
    0: "clsparseSuccess",
    1: "clsparseInvalidValue",
    2: "clsparseInvalidCommandQueue",
    3: "clsparseInvalidContext",
    4: "clsparseInvalidMemObject",
    5: "clsparseInvalidDevice",
    6: "clsparseInvalidEventWaitList",
    7: "clsparseInvalidEvent",
    8: "clsparseOutOfResources",
    9: "clsparseOutOfHostMemory",
    10: "clsparseInvalidOperation",
    11: "clsparseCompilerNotAvailable",
    12: "clsparseBuildProgramFailure",
    13: "clsparseInvalidKernelArgs",
}

_success = 0


def check(status_code):
    if status_code != _success:
        raise Exception(_status_codes_mappings[status_code])
