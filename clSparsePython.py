from ctypes import *
import sys
import OpenCLHelper
print("HELLO")
##clSparse_path = input()
clSparse_path =  ("/home/pavel/Documents/clSparse/" +
"bin/clSPARSE-build/library/" +
"libclSPARSE.so.0.10.2.0")
clSparse =  cdll.LoadLibrary(clSparse_path)
class cl_mem(Structure):
        _fields_ = []
class clsparseCsrMatrix( Structure):
	_fields_ = [("num_rows",  c_ulong),
		    ("num_cols",  c_ulong),
		    ("num_nonzeros",  c_ulong),
		    ("values",  cl_mem),
		    ("col_indices",  c_void_p),
		    ("row_pointer",  c_void_p),
		    ("off_values",  c_ulong),
		    ("off_col_indices",  c_ulong),
		    ("off_row_pointer",  c_ulong),
		    ("meta",  c_void_p)] 

clSparse.clsparseSetup.restype =  c_int
status = clSparse.clsparseSetup()
#print(launch, clSparse.clsparseStatus.clSparseSucces)
print("Status of clSparse launch - ", status)

clSparse.clsparseInitCsrMatrix.restype = c_int
clSparse.clsparseInitCsrMatrix.argtypes = [POINTER(clsparseCsrMatrix)]
myMatrix = clsparseCsrMatrix()
myMatrix_pointer =  pointer(myMatrix)
status = clSparse.clsparseInitCsrMatrix(myMatrix_pointer)
print("Status of matrix initialization - ", status)
print("Enter the path to matrix")
##path = input()
path = ("/home/pavel/Documents/clSparse/" +
"bin/Externals/MTX/Small/add20/add20.mtx")
byte_path = path.encode('utf-8')
clSparse.clsparseHeaderfromFile.restype =  c_int
clSparse.clsparseHeaderfromFile.argtypes = [ POINTER(c_ulong),
                                             POINTER(c_ulong),
                                             POINTER(c_ulong),
                                             c_char_p]
nnz = c_ulong(0)
row = c_ulong(0)
col = c_ulong(0)
status = clSparse.clsparseHeaderfromFile(pointer(nnz), pointer(row),
                                         pointer(col), byte_path)
print("Status of reading header - ", status,
      "\nNonzeros/Rows/Columns", nnz, row, col)
myMatrix.num_nonzeros = nnz # idk, but now type of it is python's int 
myMatrix.num_rows = row
myMatrix.num_cols = col

class cl_context(Structure):
        _fields_ = []
class cl_queue(Structure):
        _fields_ = []
OpenCLHelper.LoadLibrary("libOpenCL.so")
print("\n\n*** START OPENCL INITIALIZE ***")
OpenCLHelper.Initializer_FirstPlatform.restype = (POINTER(cl_context),
                                                  POINTER(cl_queue))
context, queue = OpenCLHelper.Initializer_FirstPlatform()
print("*** END OPENCL INITIALIZE ***", end = '\n\n')

class clsparseControl(Structure):
        _fields_ = []
class clsparseCreateResult(Structure):
        _fields_ = [("status", c_int),
                    ("control", clsparseControl)]
        
OpenCLHelper.CreateBuffer.restype = cl_mem
OpenCLHelper.CreateBuffer.argtypes = [cl_context,
                                      c_ulong,
                                      c_size_t]

myMatrix.values = OpenCLHelper.CreateBuffer(context,
                                            myMatrix.num_nonzeros,
                                            c_size_t(sizeof(c_float) * myMatrix.num_nonzeros))


