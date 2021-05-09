import ctypes
import os
from . import dll
from . import opencl

__all__ = [
    "singleton",
    "clsparse_dll",
    "opencl_dll",
    "init_wrapper",
    "context",
    "device",
    "command_queue",
    "create_result"
]

# Wrapper
singleton = None

clsparse_dll = None
opencl_dll = None
context = None
device = None
command_queue = None
create_result = None


def init_wrapper():
    global singleton
    global clsparse_dll
    global opencl_dll
    global context
    global device
    global command_queue
    global create_result

    singleton = Wrapper()
    clsparse_dll = singleton.clsparse_loaded_dll
    opencl_dll = singleton.opencl_loaded_dll
    context = singleton.context
    device = singleton.cl_device_id
    command_queue = singleton.command_queue
    create_result = singleton.clsparse_create_result


class Wrapper:
    """
    Performs initial initialization of libraries and provides access to them
    """
    def __init__(self):
        self._cl_platform_id = None
        self.cl_device_id = None
        self.context = None
        self.command_queue = None
        self.clsparse_create_result = None

        self.clsparse_path = os.environ["CLSPARSE_PATH"]
        self.opencl_path = os.environ["OPENCL_PATH"]
        # self.clsparse_path = "/home/pavel/Documents/clSparse/bin/clSPARSE-build/library/libclSPARSE.so"
        # self.opencl_path = "/opt/intel/system_studio_2020/opencl/SDK/lib64/libOpenCL.so"
        self.opencl_loaded_dll = opencl.opencl_load_and_configure(self.opencl_path)
        self.clsparse_loaded_dll = dll.clsparse_load_and_configure(self.clsparse_path)

        status = self.clsparse_loaded_dll.clsparseSetup()
        dll.check(status)
        self._setup_platform()
        self._setup_device()
        self._setup_context()
        self._setup_command_queue()
        self._clsparse_create_result()

        # self.test_queue()
        # self.test_context()
        # self.test_device()

    def __del__(self):
        pass

    def test_queue(self):
        size = ctypes.c_size_t(0)
        status = self.opencl_loaded_dll.clGetCommandQueueInfo(self.command_queue,
                                                              ctypes.c_int(4240),
                                                              0,
                                                              None,
                                                              ctypes.pointer(size))
        name = (ctypes.c_char * size.value)()
        status = self.opencl_loaded_dll.clGetCommandQueueInfo(self.command_queue,
                                                              ctypes.c_int(4240),
                                                              size,
                                                              name,
                                                              None)
        print(name.value)

        status = self.opencl_loaded_dll.clGetCommandQueueInfo(self.command_queue,
                                                              ctypes.c_int(4241),
                                                              0,
                                                              None,
                                                              ctypes.pointer(size))
        name = (ctypes.c_char * size.value)()
        status = self.opencl_loaded_dll.clGetCommandQueueInfo(self.command_queue,
                                                              ctypes.c_int(4241),
                                                              size,
                                                              name,
                                                              None)
        print(str(name.value))

        status = self.opencl_loaded_dll.clGetCommandQueueInfo(self.command_queue,
                                                              ctypes.c_int(4242),
                                                              0,
                                                              None,
                                                              ctypes.pointer(size))
        name = (ctypes.c_char * size.value)()
        status = self.opencl_loaded_dll.clGetCommandQueueInfo(self.command_queue,
                                                              ctypes.c_int(4242),
                                                              size,
                                                              name,
                                                              None)
        print(str(name.value))

        status = self.opencl_loaded_dll.clGetCommandQueueInfo(self.command_queue,
                                                              ctypes.c_int(4243),
                                                              0,
                                                              None,
                                                              ctypes.pointer(size))
        name = (ctypes.c_char * size.value)()
        status = self.opencl_loaded_dll.clGetCommandQueueInfo(self.command_queue,
                                                              ctypes.c_int(4243),
                                                              size,
                                                              name,
                                                              None)
        print(str(name.value))

    def test_context(self):
        print("context info")
        size = ctypes.c_size_t(0)
        status = self.opencl_loaded_dll.clGetContextInfo(self.context,
                                                         ctypes.c_int(4224),
                                                         0,
                                                         None,
                                                         ctypes.pointer(size))
        name = (ctypes.c_char * size.value)()
        opencl.check(status)
        status = self.opencl_loaded_dll.clGetContextInfo(self.context,
                                                         ctypes.c_int(4224),
                                                         size,
                                                         name,
                                                         None)
        print("CL_CONTEXT_REFERENCE_COUNT " + str(name.value))
        opencl.check(status)

        status = self.opencl_loaded_dll.clGetContextInfo(self.context,
                                                         ctypes.c_int(4225),
                                                         0,
                                                         None,
                                                         ctypes.pointer(size))
        name = (ctypes.c_char * size.value)()
        opencl.check(status)
        status = self.opencl_loaded_dll.clGetContextInfo(self.context,
                                                         ctypes.c_int(4225),
                                                         size,
                                                         name,
                                                         None)
        print("CL_CONTEXT_DEVICES " + str(name.value))
        opencl.check(status)

        status = self.opencl_loaded_dll.clGetContextInfo(self.context,
                                                         ctypes.c_int(4226),
                                                         0,
                                                         None,
                                                         ctypes.pointer(size))
        name = (ctypes.c_char * size.value)()
        opencl.check(status)
        status = self.opencl_loaded_dll.clGetContextInfo(self.context,
                                                         ctypes.c_int(4226),
                                                         size,
                                                         name,
                                                         None)
        print("CL_CONTEXT_PROPERTIES " + str(name.value))
        opencl.check(status)

    def test_device(self):
        print("device info")
        size = ctypes.c_size_t(0)
        status = self.opencl_loaded_dll.clGetDeviceInfo(self.cl_device_id,
                                                        ctypes.c_int(4096),  # CL_DEVICE_TYPE
                                                        0,
                                                        None,
                                                        ctypes.pointer(size))
        name = (ctypes.c_char * size.value)()
        opencl.check(status)
        status = self.opencl_loaded_dll.clGetDeviceInfo(self.cl_device_id,
                                                        ctypes.c_int(4096),  # CL_DEVICE_TYPE
                                                        size,
                                                        name,
                                                        None)
        opencl.check(status)
        print("CL_DEVICE_TYPE " + str(name.value))

        size = ctypes.c_size_t(0)
        status = self.opencl_loaded_dll.clGetDeviceInfo(self.cl_device_id,
                                                        ctypes.c_int(4097),  # CL_DEVICE_VENDOR_ID
                                                        0,
                                                        None,
                                                        ctypes.pointer(size))
        name = (ctypes.c_char * size.value)()
        opencl.check(status)
        status = self.opencl_loaded_dll.clGetDeviceInfo(self.cl_device_id,
                                                        ctypes.c_int(4097),  # CL_DEVICE_VENDOR_ID
                                                        size,
                                                        name,
                                                        None)
        print("CL_DEVICE_TYPE " + str(name.value))
        opencl.check(status)

        size = ctypes.c_size_t(0)
        status = self.opencl_loaded_dll.clGetDeviceInfo(self.cl_device_id,
                                                        ctypes.c_int(4141),  # CL_DRIVER_VERSION
                                                        0,
                                                        None,
                                                        ctypes.pointer(size))
        opencl.check(status)
        name = (ctypes.c_char * size.value)()
        status = self.opencl_loaded_dll.clGetDeviceInfo(self.cl_device_id,
                                                        ctypes.c_int(4141),  # CL_DRIVER_VERSION
                                                        size,
                                                        name,
                                                        None)
        print("CL_DRIVER_VERSION " + str(name.value))
        opencl.check(status)

    def _setup_platform(self):
        num_of_platforms = ctypes.c_uint(0)
        self._cl_platform_id = ctypes.c_void_p(0)
        status = self.opencl_loaded_dll.clGetPlatformIDs(0,
                                                         None,
                                                         ctypes.byref(num_of_platforms))
        opencl.check(status)
        if num_of_platforms == 0:
            raise Exception("No OpenCL platform found")
        status = self.opencl_loaded_dll.clGetPlatformIDs(1,
                                                         ctypes.byref(self._cl_platform_id),
                                                         None)
        opencl.check(status)

    def _setup_device(self):
        num_devices = ctypes.c_uint(0)
        self.cl_device_id = ctypes.c_void_p(0)
        status = self.opencl_loaded_dll.clGetDeviceIDs(self._cl_platform_id,
                                                       ctypes.c_uint(opencl.map_flags("CL_DEVICE_TYPE_GPU")),
                                                       0,
                                                       None,
                                                       ctypes.pointer(num_devices))
        opencl.check(status)
        if num_devices == 0:
            raise Exception("No OpenCL devices found")
        status = self.opencl_loaded_dll.clGetDeviceIDs(self._cl_platform_id,
                                                       ctypes.c_uint(opencl.map_flags("CL_DEVICE_TYPE_GPU")),
                                                       1,  # num_devices
                                                       ctypes.byref(self.cl_device_id),
                                                       None)
        opencl.check(status)

    def _setup_context(self):
        _context = ctypes.c_void_p(0)
        status = ctypes.c_int(0)
        _context = self.opencl_loaded_dll.clCreateContext(ctypes.pointer(ctypes.c_uint(0)),
                                                          ctypes.c_uint(1),
                                                          ctypes.byref(self.cl_device_id),
                                                          None,
                                                          None,
                                                          ctypes.pointer(status))
        opencl.check(status.value)
        self.context = _context

    def _setup_command_queue(self):
        _queue = ctypes.c_void_p(0)
        status = ctypes.c_int(0)
        _queue = self.opencl_loaded_dll.clCreateCommandQueue(self.context,
                                                             self.cl_device_id,
                                                             None,
                                                             ctypes.pointer(status))
        opencl.check(status.value)
        self.command_queue = _queue

    def _clsparse_create_result(self):
        _create_result = self.clsparse_loaded_dll.clsparseCreateControl(self.command_queue)
        dll.check(_create_result.clsparseStatus)
        self.clsparse_create_result = _create_result
