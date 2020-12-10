import ctypes

class cl_context(ctypes.Structure):
        _fields_ = []
class cl_queue(ctypes.Structure):
        _fields_ = []
openCL = None

def LoadLibrary(path : str):
    global openCL
    openCL = ctypes.cdll.LoadLibrary(path)
    
def Initializer_FirstPlatform():
    status = ctypes.c_int(0)

    # PLATFORMS
    num_of_platforms = ctypes.c_uint(0)
    class cl_platform_id(ctypes.Structure):
        _fields_ = []
    openCL.clGetPlatformIDs.restype = ctypes.c_int
    openCL.clGetPlatformIDs.argtype = [ctypes.c_uint,
                                       ctypes.POINTER(cl_platform_id),
                                       ctypes.POINTER(ctypes.c_uint)]
    num_platforms = ctypes.c_uint(0)
    status = openCL.clGetPlatformIDs(0, None, ctypes.pointer(num_platforms))
    print("Status of receiving amount of platfroms: " + str(status))
    platforms = ctypes.cast((cl_platform_id * num_platforms.value)(), ctypes.POINTER(cl_platform_id))
    status = openCL.clGetPlatformIDs(num_platforms,
                                     ctypes.pointer(platforms),
                                     None)
    print("Status of receiving platfroms: " + str(status))
    print("Amount of available platforms: " + str(num_platforms.value))
    size = ctypes.c_size_t(0);
    openCL.clGetPlatformInfo.argtypes = [ctypes.POINTER(cl_platform_id),
                                         ctypes.c_uint,
                                         ctypes.c_size_t,
                                         ctypes.POINTER(ctypes.c_char),
                                         ctypes.POINTER(ctypes.c_size_t)]
    status = openCL.clGetPlatformInfo(ctypes.pointer(platforms[0]),
                             ctypes.c_uint(2306), # CL_PLATFORM_NAME
                             0,
                             None,
                             ctypes.pointer(size))
    name = (ctypes.c_char * size.value)()
    status = openCL.clGetPlatformInfo(platforms[0],
                             ctypes.c_uint(2306), # CL_PLATFORM_NAME
                             size,
                             name,
                             None)
    print("Status of receiving info about platfrom: " + str(status))
    print("Name of first platform: " + str(name.value))

    # DEVICES
    class cl_device_id(ctypes.Structure):
        _fields_ = []
    num_devices = ctypes.c_uint(0)
    openCL.clGetDeviceIDs.restype = ctypes.c_int
    openCL.clGetDeviceIDs.argtype = [ctypes.POINTER(cl_platform_id),
                                     ctypes.c_uint, # cl_device_type
                                     ctypes.c_uint,
                                     ctypes.POINTER(cl_device_id),
                                     ctypes.POINTER(ctypes.c_uint)]
    status = openCL.clGetDeviceIDs(ctypes.pointer(platforms[0]),
                                   ctypes.c_uint(4294967295), # CL_DEVICE_TYPE_ALL
                                   0,
                                   None,
                                   ctypes.pointer(num_devices))
    devices = ctypes.cast((cl_device_id * num_devices.value)(), ctypes.POINTER(cl_device_id))
    status = openCL.clGetDeviceIDs(ctypes.pointer(platforms[0]),
                                   ctypes.c_uint(4294967295), # CL_DEVICE_TYPE_ALL
                                   num_devices,
                                   ctypes.pointer(devices),
                                   None)
    print("Status of receiving devices: " + str(status))

    # CONTEXT
##    props = (ctypes.c_uint * 3)()
##    props[0] = ctypes.c_uint(4228) # CL_CONTEXT_PLATFORM
##    props[1] = ctypes.pointer(platforms[0])
##    props[2] = ctypes.c_int(0)
##    props = ctypes.cast(props, ctypes.POINTER(c_void))
    openCL.clCreateContext.restype = ctypes.POINTER(cl_context)
    openCL.clCreateContext.argtype = [ctypes.POINTER(ctypes.c_uint),
                                      ctypes.c_uint,
                                      ctypes.POINTER(cl_device_id),
                                      ctypes.c_voidp,
                                      ctypes.c_voidp,
                                      ctypes.POINTER(ctypes.c_int)]
    status = ctypes.c_int(0)
    context = openCL.clCreateContext(ctypes.pointer(ctypes.c_uint(0)),
                                     ctypes.c_uint(1),
                                     ctypes.pointer(devices),
                                     None,
                                     None,
                                     ctypes.pointer(status))
    print("Status of creating context: " + str(status))
    openCL.clCreateCommandQueue.restype = ctypes.POINTER(cl_queue)
    openCL.clCreateCommandQueue.argtype = [cl_context,
                                          cl_device_id,
                                          ctypes.c_voidp,
                                          ctypes.POINTER(ctypes.c_int)]
    status = ctypes.c_int(0)
    queue = openCL.clCreateCommandQueue(context,
                                         devices,
                                         None,
                                         ctypes.pointer(status))
    print("Status of creating command queue: " + str(status))
    return context, queue

def CreateBuffer(context : cl_context, a : int, b : ctypes.c_size_t):
    class cl_mem(ctypes.Structure):
        _fields_ = []
    openCL.clCreateBuffer.restype = cl_mem
    openCL.clCreateBuffer.argtype = [cl_context,
                                     ctypes.c_ulong,
                                     ctypes.c_ulong,
                                     ctypes.c_voidp,
                                     ctypes.POINTER(ctypes.c_int)]
    status = ctypes.c_int(0)
    b = int(b.value)
    c = ctypes.c_size_t(a * b)
    print(c)
    buffer = openCL.clCreateBuffer(context,
                                   ctypes.c_ulong(4), # CL_MEM_READ_ONLY
                                   c,
                                   None,
                                   ctypes.pointer(status))
    print("Status of creating buffer: " + str(status))
                                   

#OpenCLInitializer_FirstPlatform("libOpenCL.so")
