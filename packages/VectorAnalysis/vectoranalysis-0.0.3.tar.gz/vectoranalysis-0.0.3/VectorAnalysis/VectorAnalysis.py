from sympy.vector import CoordSys3D, Del

def gradient(C):
    delop=Del()
    gradient_field=delop(C)
    return gradient_field.doit()

def divergence(C):
    delop=Del()
    return delop.dot(C).doit()

def curl(C):
    delop=Del()
    return delop.cross(C).doit()
