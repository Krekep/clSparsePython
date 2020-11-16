from ctypes import *
import sys
import OpenCLHelper
print("HELLO")
clSparse_path = input()
##clSparse =  cdll.LoadLibrary("/home/pavel/Documents/clSparse/" +
##"bin/clSPARSE-build/library/" +
##"libclSPARSE.so.0.10.2.0")
clSparse =  cdll.LoadLibrary(clSparse_path)

class clsparseCsrMatrix( Structure):
	_fields_ = [("num_rows",  c_ulong),
		    ("num_cols",  c_ulong),
		    ("num_nonzeros",  c_ulong),
		    ("values",  c_void_p),
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
a = clsparseCsrMatrix()
a_pointer =  pointer(a)
status = clSparse.clsparseInitCsrMatrix(a_pointer)
print("Status of matrix initialization - ", status)
print("Enter the path to matrix")
path = input()
##path = ("/home/pavel/Documents/clSparse/" +
##"bin/Externals/MTX/Small/add20/add20.mtx")
byte_path = path.encode('utf-8')
clSparse.clsparseHeaderfromFile.restype =  c_int
clSparse.clsparseHeaderfromFile.argtypes = [ POINTER(c_int),
                                             POINTER(c_int),
                                             POINTER(c_int),
                                             c_char_p]
nnz = c_int(0)
row = c_int(0)
col = c_int(0)
status = clSparse.clsparseHeaderfromFile(pointer(nnz), pointer(row),
                                         pointer(col), byte_path)
print("Status of reading header - ", status,
      "\n Nonzeros/Rows/Columns", nnz, row, col)

print("\n\n*** START OPENCL INITIALIZE ***")
OpenCLHelper.OpenCLInitializer_CPU("libOpenCL.so")
print("*** END OPENCL INITIALIZE ***", end = '\n\n')

