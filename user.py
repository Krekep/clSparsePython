from pyclsparse import wrapper, matrix, vector
import ctypes


path = "/home/pavel/Documents/clSparse/bin/Externals/MTX/Small/add20/add20.mtx"
# path = input()
a = matrix.Matrix(path)
# x = [0, 3, 5, 7]
# b = pyclsparse.vector.Vector(len(x), x)
# b.some_info()
print("Success")

