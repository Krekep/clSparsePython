from pyclsparse import wrapper, matrix, vector
import ctypes


path = "/home/pavel/Documents/clSparse/bin/Externals/MTX/Small/add20/add20.mtx"
# path = input()
a = matrix.Matrix(path)

print("Success")

