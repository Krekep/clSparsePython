from pyclsparse import wrapper, scalar, vector, dll, opencl
import ctypes

from pyclsparse.axpy import axpy

n = 1024
y_source = [2.0] * n
x_source = [1.0] * n

y = vector.Vector(n, y_source)
x = vector.Vector(n, x_source)

a = scalar.Scalar(2.0)

wrap = wrapper.singleton
result = vector.Vector(n, [])
axpy(result, a, x, y)
result.print_values()
