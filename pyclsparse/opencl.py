import ctypes

__all__ = [
    "opencl_load_and_configure"
]


def opencl_load_and_configure(opencl_lib_path: str):
    lib = ctypes.cdll.LoadLibrary(opencl_lib_path)

    cl_platform_id = ctypes.c_void_p
    cl_device_id = ctypes.c_void_p
    cl_context = ctypes.c_void_p
    cl_queue = ctypes.c_void_p
    cl_mem = ctypes.c_void_p
    cl_program = ctypes.c_void_p
    cl_kernel = ctypes.c_void_p

    lib.clGetPlatformIDs.restype = ctypes.c_int
    lib.clGetPlatformIDs.argtype = [ctypes.c_uint,
                                    ctypes.POINTER(cl_platform_id),
                                    ctypes.POINTER(ctypes.c_uint)]

    lib.clGetDeviceIDs.restype = ctypes.c_int
    lib.clGetDeviceIDs.argtype = [ctypes.POINTER(cl_platform_id),
                                  ctypes.c_uint,  # cl_device_type
                                  ctypes.c_uint,
                                  ctypes.POINTER(cl_device_id),
                                  ctypes.POINTER(ctypes.c_uint)]

    lib.clCreateContext.restype = cl_context
    lib.clCreateContext.argtype = [ctypes.POINTER(ctypes.c_uint),
                                   ctypes.c_uint,
                                   ctypes.POINTER(cl_device_id),
                                   ctypes.c_void_p,
                                   ctypes.c_void_p,
                                   ctypes.POINTER(ctypes.c_int)]

    lib.clCreateCommandQueue.restype = cl_queue
    lib.clCreateCommandQueue.argtype = [cl_context,
                                        cl_device_id,
                                        ctypes.c_void_p,
                                        ctypes.POINTER(ctypes.c_int)]

    lib.clGetCommandQueueInfo.restype = ctypes.c_int
    lib.clGetCommandQueueInfo.argtype = [cl_queue,
                                         ctypes.c_int,
                                         ctypes.c_size_t,
                                         ctypes.POINTER(ctypes.c_char),
                                         ctypes.POINTER(ctypes.c_size_t)]

    lib.clGetContextInfo.restype = ctypes.c_int
    lib.clGetContextInfo.argtype = [cl_context,
                                    ctypes.c_int,
                                    ctypes.c_size_t,
                                    ctypes.POINTER(ctypes.c_char),
                                    ctypes.POINTER(ctypes.c_size_t)]

    lib.clCreateBuffer.restype = cl_mem
    lib.clCreateBuffer.argtype = [cl_context,
                                  ctypes.c_ulong,
                                  ctypes.c_ulong,
                                  ctypes.c_void_p,
                                  ctypes.POINTER(ctypes.c_int)]

    return lib
