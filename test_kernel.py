from pyclsparse import opencl, wrapper
import ctypes


def c_str_array(strings):
    """Create ctypes const char ** from a list of Python strings.

    Parameters
    ----------
    strings : list of string
        Python strings.

    Returns
    -------
    (ctypes.c_char_p * len(strings))
        A const char ** pointer that can be passed to C API.
    """
    arr = (ctypes.c_char_p * len(strings))()
    arr[:] = [s.encode('utf-8') for s in strings]
    return arr


kernel_code = """kernel void Sample(const global int* A) {;}"""
wrapper = wrapper.singleton
x = [1, 2, 3]
status = ctypes.c_int(0)
buffer = wrapper.opencl_loaded_dll.clCreateBuffer(
    wrapper.context,
    ctypes.c_int(opencl.map_flags("CL_MEM_READ_WRITE | CL_MEM_USE_HOST_PTR")),
    len(x) * ctypes.sizeof(ctypes.c_float),
    (ctypes.c_float * len(x))(*x),
    ctypes.byref(status))
opencl.check(status.value)
print("Here1")

byte_kernel = kernel_code.encode('utf-8')
temp = c_str_array([kernel_code])
program = wrapper.opencl_loaded_dll.clCreateProgramWithSourse(
    wrapper.context,
    ctypes.c_int(1),
    temp,
    None,
    ctypes.byref(status)
)
opencl.check(status.value)
print("Here2")

status = wrapper.opencl_loaded_dll.clBuildProgram(
    program,
    ctypes.c_int(1),
    wrapper.cl_device_id,
    None,
    None,
    None
)
opencl.check(status.value)
print("Here3")

name = "Sample"
temp = (ctypes.c_char * len(name))(name)
kernel = wrapper.opencl_loaded_dll.clCreateKernel(
    program,
    temp,
    ctypes.byref(status)
)
opencl.check(status.value)
print("Here4")

status = wrapper.opencl_loaded_dll.clSetKernelArg(
    kernel,
    ctypes.c_uint(0),
    ctypes.sizeof(ctypes.c_void_p),
    buffer
)
opencl.check(status.value)
print("Here5")
