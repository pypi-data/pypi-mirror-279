# VectorAnalysis
This is a tutorial on how to use a PyPI application.
You can culculate gradient, divergence and curl by using this application.

# How to install VectorAnalysis
$ pip install VectorAnalysis

# How to run VectorAnalysis
You need also "sympy" to run this application.<br>
$ pip install sympy

example:<br>
In [1]: from sympy.vector import CoordSys3D<br>
In [2]: C = CoordSys3D('C')<br>
In [3]: g = C.x * C.y * C.z<br>
In [4]: gradient(g)<br>
Out[4]: C.y*C.z*C.i + C.x*C.z*C.j + C.x*C.y*C.k<br>