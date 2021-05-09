from pyclsparse import wrapper, scalar, vector, dll, opencl
import ctypes

from pyclsparse.axpy import axpy

n = 1024
y_source = [2.0] * n
x_source = [1.0] * n
y = vector.Vector(n, y_source)
x = vector.Vector(n, x_source)
print("Vector y:", y.get_values())
print("Vector x:", x.get_values())
a = scalar.Scalar(2.0)
print("Alpha:", a.get_value())

wrap = wrapper.singleton
result = vector.Vector(n, [])
axpy(result, a, x, y)
print("Result of AXPY operation:", result.get_values())
