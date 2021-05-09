import ctypes

__all__ = [
    "opencl_load_and_configure",
    "check",
    "map_flags"
]


def opencl_load_and_configure(opencl_lib_path: str):
    """
    Definition of signatures of functions of the OpenCL library
    :param opencl_lib_path:
    :return:
    """
    lib = ctypes.cdll.LoadLibrary(opencl_lib_path)

    cl_platform_id = ctypes.c_void_p
    cl_device_id = ctypes.c_void_p
    cl_context = ctypes.c_void_p
    cl_queue = ctypes.c_void_p
    cl_mem = ctypes.c_void_p
    cl_program = ctypes.c_void_p
    cl_kernel = ctypes.c_void_p

    lib.clCreateProgramWithSource.restype = cl_program  # undefined symbol???
    lib.clCreateProgramWithSource.argtype = [cl_context,
                                             ctypes.c_uint,
                                             ctypes.POINTER(ctypes.POINTER(ctypes.c_char)),
                                             ctypes.POINTER(ctypes.c_uint),
                                             ctypes.c_int]

    lib.clBuildProgram.restype = ctypes.c_int
    lib.clBuildProgram.argtype = [cl_program,
                                  ctypes.c_uint,
                                  ctypes.POINTER(cl_device_id),
                                  ctypes.POINTER(ctypes.c_char),
                                  ctypes.c_void_p,
                                  ctypes.c_void_p]

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

    lib.clGetDeviceInfo.restype = ctypes.c_int
    lib.clGetDeviceInfo.argtype = [cl_device_id,
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

    lib.clCreateKernel.restype = cl_kernel
    lib.clCreateKernel.argtype = [cl_program,
                                  ctypes.POINTER(ctypes.c_char),
                                  ctypes.POINTER(ctypes.c_int)]

    lib.clSetKernelArg.restype = ctypes.c_int
    lib.clSetKernelArg.argtype = [cl_kernel,
                                  ctypes.c_uint,
                                  ctypes.c_size_t,
                                  ctypes.c_void_p]

    lib.clEnqueueTask.restype = ctypes.c_int
    lib.clEnqueueTask.argtype = [cl_queue,
                                 cl_kernel,
                                 ctypes.c_uint,
                                 ctypes.c_void_p,  # const cl_event* event_wait_list
                                 ctypes.c_void_p]  # cl_event* event

    lib.clEnqueueReadBuffer.restype = ctypes.c_int
    lib.clEnqueueReadBuffer.argtype = [cl_queue,
                                       cl_mem,
                                       ctypes.c_bool,
                                       ctypes.c_size_t,
                                       ctypes.c_size_t,
                                       ctypes.c_void_p,
                                       ctypes.c_uint,
                                       ctypes.c_void_p,  # const cl_event* event_wait_list
                                       ctypes.c_void_p]  # cl_event* event

    return lib


"""
Several error codes from the OpenCL library 
"""
_status_codes_mappings = {
    0: "CL_SUCCESS",
    -1: "CL_DEVICE_NOT_FOUND",
    -2: "CL_DEVICE_NOT_AVAILABLE",
    -3: "CL_COMPILER_NOT_AVAILABLE",
    -4: "CL_MEM_OBJECT_ALLOCATION_FAILURE",
    -5: "CL_OUT_OF_RESOURCES",
    -6: "CL_OUT_OF_HOST_MEMORY",
    -7: "CL_PROFILING_INFO_NOT_AVAILABLE",
    -8: "CL_MEM_COPY_OVERLAP",
    -9: "CL_IMAGE_FORMAT_MISMATCH",
    -10: "CL_IMAGE_FORMAT_NOT_SUPPORTED",
    -11: "CL_BUILD_PROGRAM_FAILURE",
    -12: "CL_MAP_FAILURE",
    -30: "CL_INVALID_VALUE",
    -31: "CL_INVALID_DEVICE_TYPE",
    -32: "CL_INVALID_PLATFORM",
    -33: "CL_INVALID_DEVICE",
    -34: "CL_INVALID_CONTEXT",
    -35: "CL_INVALID_QUEUE_PROPERTIES",
    -36: "CL_INVALID_COMMAND_QUEUE",
    -37: "CL_INVALID_HOST_PTR",
    -38: "CL_INVALID_MEM_OBJECT",
}

_success = 0


def check(status_code):
    if status_code != _success:
        raise Exception(_status_codes_mappings[status_code])


_cl_device_type_mapping = {
    "CL_DEVICE_TYPE_DEFAULT": 1,
    "CL_DEVICE_TYPE_CPU": 2,
    "CL_DEVICE_TYPE_GPU": 4,
    "CL_DEVICE_TYPE_ALL": 4294967295
}

_cl_mem_flags_mapping = {
    "CL_MEM_READ_WRITE": 1,
    "CL_MEM_WRITE_ONLY": 2,
    "CL_MEM_READ_ONLY": 4,
    "CL_MEM_USE_HOST_PTR": 8,
    "CL_MEM_ALLOC_HOST_PTR": 16,
    "CL_MEM_COPY_HOST_PTR": 32
}


def map_flags(flag: str):
    result = 0
    temp = flag.split("|")
    for i in range(len(temp)):
        temp[i] = temp[i].strip(" ")
        x = _cl_device_type_mapping.get(temp[i])
        y = _cl_mem_flags_mapping.get(temp[i])
        if x is None:
            x = 0
        if y is None:
            y = 0
        result += x + y
    return result
