import copy as cp
import numpy as np

t = np.array([[0, 0, 1],
              [0, 1, 0],
              [1, 0, 0]])

def clockwise(face):
    face = face.transpose().dot(t)
    return face

def antiClockwise(face):
    face = face.dot(t).transpose()
    return face

# Rotate the up face 90 degrees clockwise
def U(FACES):
    FACES[0] = clockwise(FACES[0])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = FACES_new[4], FACES_new[2], FACES_new[5], FACES_new[3]
    FACES[4][0], FACES[2][0], FACES[5][0], FACES[3][0] = d[0], a[0], b[0], c[0]
    return FACES

# Rotate the up face 90 degrees anti-clockwise
def _U(FACES):
    FACES[0] = antiClockwise(FACES[0])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = FACES_new[4], FACES_new[2], FACES_new[5], FACES_new[3]
    FACES[4][0], FACES[2][0], FACES[5][0], FACES[3][0] = b[0], c[0], d[0], a[0]
    return FACES

# Rotate the up face 180 degrees
def U2(FACES):
    for i in range(2):
        U(FACES)
    return FACES

# Rotate the down face 90 degrees clockwise
def D(FACES):
    FACES[1] = clockwise(FACES[1])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = FACES_new[4], FACES_new[2], FACES_new[5], FACES_new[3]
    FACES[4][2], FACES[2][2], FACES[5][2], FACES[3][2] = b[2], c[2], d[2], a[2]
    return FACES

# Rotate the down face 90 degrees anti-clockwise
def _D(FACES):
    FACES[1] = antiClockwise(FACES[1])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = FACES_new[4], FACES_new[2], FACES_new[5], FACES_new[3]
    FACES[4][2], FACES[2][2], FACES[5][2], FACES[3][2] = d[2], a[2], b[2], c[2]
    return FACES

# Rotate the down face 180 degrees
def D2(FACES):
    for i in range(2):
        D(FACES)
    return FACES

# Rotate the left face 90 degrees clockwise
def L(FACES):
    FACES[2] = clockwise(FACES[2])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = clockwise(FACES_new[4]), clockwise(FACES_new[1]), antiClockwise(FACES_new[5]), clockwise(FACES_new[0])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    e[0], f[0], g[0], h[0] = d[0], a[0], b[0], c[0]
    FACES[4], FACES[1], FACES[5], FACES[0] = antiClockwise(e), antiClockwise(f), clockwise(g), antiClockwise(h)
    return FACES

# Rotate the left face 90 degrees anti-clockwise
def _L(FACES):
    FACES[2] = antiClockwise(FACES[2])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = clockwise(FACES_new[4]), clockwise(FACES_new[1]), antiClockwise(FACES_new[5]), clockwise(FACES_new[0])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    e[0], f[0], g[0], h[0] = b[0], c[0], d[0], a[0]
    FACES[4], FACES[1], FACES[5], FACES[0] = antiClockwise(e), antiClockwise(f), clockwise(g), antiClockwise(h)
    return FACES

# Rotate the left face 180 degrees
def L2(FACES):
    for i in range(2):
        L(FACES)
    return FACES

# Rotate the right face 90 degrees clockwise
def R(FACES):
    FACES[3] = clockwise(FACES[3])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = antiClockwise(FACES_new[4]), antiClockwise(FACES_new[1]), clockwise(FACES_new[5]), antiClockwise(
        FACES_new[0])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    g[0], f[0], e[0], h[0] = d[0], c[0], b[0], a[0]
    FACES[4], FACES[1], FACES[5], FACES[0] = clockwise(e), clockwise(f), antiClockwise(g), clockwise(h)
    return FACES

# Rotate the right face 90 degrees anti-clockwise
def _R(FACES):
    FACES[3] = antiClockwise(FACES[3])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = antiClockwise(FACES_new[4]), antiClockwise(FACES_new[1]), clockwise(FACES_new[5]), antiClockwise(
        FACES_new[0])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    f[0], g[0], h[0], e[0] = a[0], b[0], c[0], d[0]
    FACES[4], FACES[1], FACES[5], FACES[0] = clockwise(e), clockwise(f), antiClockwise(g), clockwise(h)
    return FACES

# Rotate the right face 180 degrees
def R2(FACES):
    for i in range(2):
        R(FACES)
    return FACES

# Rotate the front face 90 degrees clockwise
def F(FACES):
    FACES[4] = clockwise(FACES[4])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = clockwise(clockwise(FACES_new[0])), FACES_new[1], antiClockwise(FACES_new[2]), clockwise(FACES_new[3])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    e[0], g[0], f[0], h[0] = c[0], b[0], d[0], a[0]
    FACES[0], FACES[1], FACES[2], FACES[3] = clockwise(clockwise(e)), f, clockwise(g), antiClockwise(h)
    return FACES

# Rotate the front face 90 degrees anti-clockwise
def _F(FACES):
    FACES[4] = antiClockwise(FACES[4])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = clockwise(clockwise(FACES_new[0])), FACES_new[1], antiClockwise(FACES_new[2]), clockwise(FACES_new[3])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    g[0], f[0], h[0], e[0] = a[0], c[0], b[0], d[0]
    FACES[0], FACES[1], FACES[2], FACES[3] = clockwise(clockwise(e)), f, clockwise(g), antiClockwise(h)
    return FACES

# Rotate the front face 180 degrees
def F2(FACES):
    for _ in range(2):
        F(FACES)
    return FACES

# Rotate the back face 90 degrees clockwise
def B(FACES):
    FACES[5] = clockwise(FACES[5])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = FACES_new[0], clockwise(clockwise(FACES_new[1])), clockwise(FACES_new[2]), antiClockwise(FACES_new[3])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    g[0], f[0], h[0], e[0] = a[0], c[0], b[0], d[0]
    FACES[0], FACES[1], FACES[2], FACES[3] = e, clockwise(clockwise(f)), antiClockwise(g), clockwise(h)
    return FACES

# Rotate the back face 90 degrees anti-clockwise
def _B(FACES):
    FACES[5] = antiClockwise(FACES[5])
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = FACES_new[0], clockwise(clockwise(FACES_new[1])), clockwise(FACES_new[2]), antiClockwise(FACES_new[3])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    e[0], g[0], f[0], h[0] = c[0], b[0], d[0], a[0]
    FACES[0], FACES[1], FACES[2], FACES[3] = e, clockwise(clockwise(f)), antiClockwise(g), clockwise(h)
    return FACES

# Rotate the back face 180 degrees
def B2(FACES):
    for i in range(2):
        B(FACES)
    return FACES

# Rotate the middle layer on x-axis direction 90 degrees clockwise
def E(FACES):
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = FACES_new[4], FACES_new[2], FACES_new[5], FACES_new[3]
    FACES[4][1], FACES[2][1], FACES[5][1], FACES[3][1] = b[1], c[1], d[1], a[1]
    return FACES

# Rotate the middle layer on x-axis direction 90 degrees anti-clockwise
def _E(FACES):
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = FACES_new[4], FACES_new[2], FACES_new[5], FACES_new[3]
    FACES[4][1], FACES[2][1], FACES[5][1], FACES[3][1] = d[1], a[1], b[1], c[1]
    return FACES

# Rotate the middle layer on x-axis direction 180 degrees
def E2(FACES):
    for i in range(2):
        E(FACES)
    return FACES

# Rotate the middle layer on y-axis direction 90 degrees clockwise
def M(FACES):
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = clockwise(FACES_new[4]), clockwise(FACES_new[1]), antiClockwise(FACES_new[5]), clockwise(FACES_new[0])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    e[1], f[1], g[1], h[1] = d[1], a[1], b[1], c[1]
    FACES[4], FACES[1], FACES[5], FACES[0] = antiClockwise(e), antiClockwise(f), clockwise(g), antiClockwise(h)
    return FACES

# Rotate the middle layer on y-axis direction 90 degrees anti-clockwise
def _M(FACES):
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = clockwise(FACES_new[4]), clockwise(FACES_new[1]), antiClockwise(FACES_new[5]), clockwise(FACES_new[0])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    e[1], f[1], g[1], h[1] = b[1], c[1], d[1], a[1]
    FACES[4], FACES[1], FACES[5], FACES[0] = antiClockwise(e), antiClockwise(f), clockwise(g), antiClockwise(h)
    return FACES

# Rotate the middle layer on y-axis direction 180 degrees
def M2(FACES):
    for i in range(2):
        M(FACES)
    return FACES

# Rotate the middle layer on z-axis direction 90 degrees clockwise
def S(FACES):
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = clockwise(clockwise(FACES_new[0])), FACES_new[1], antiClockwise(FACES_new[2]), clockwise(FACES_new[3])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    e[1], g[1], f[1], h[1] = c[1], b[1], d[1], a[1]
    FACES[0], FACES[1], FACES[2], FACES[3] = clockwise(clockwise(e)), f, clockwise(g), antiClockwise(h)
    return FACES

# Rotate the middle layer on z-axis direction 90 degrees anti-clockwise
def _S(FACES):
    FACES_new = cp.deepcopy(FACES)
    a, b, c, d = clockwise(clockwise(FACES_new[0])), FACES_new[1], antiClockwise(FACES_new[2]), clockwise(FACES_new[3])
    e, f, g, h = cp.deepcopy(a), cp.deepcopy(b), cp.deepcopy(c), cp.deepcopy(d)
    g[1], f[1], h[1], e[1] = a[1], c[1], b[1], d[1]
    FACES[0], FACES[1], FACES[2], FACES[3] = clockwise(clockwise(e)), f, clockwise(g), antiClockwise(h)
    return FACES

# Rotate the middle layer on z-axis direction 180 degrees
def S2(FACES):
    for i in range(2):
        S(FACES)
    return FACES

# Rotate the Rubik's Cube 90 degrees clockwise on the x-axis direction
def X(FACES):
    _L(FACES)
    _M(FACES)
    R(FACES)
    return FACES

# Rotate the Rubik's Cube 90 degrees anti-clockwise on the x-axis direction
def _X(FACES):
    L(FACES)
    M(FACES)
    _R(FACES)
    return FACES

# Rotate the Rubik's Cube 180 degrees on the x-axis direction
def X2(FACES):
    L2(FACES)
    M2(FACES)
    R2(FACES)
    return FACES

# Rotate the Rubik's Cube 90 degrees clockwise on the y-axis direction
def Y(FACES):
    U(FACES)
    _E(FACES)
    _D(FACES)
    return FACES

# Rotate the Rubik's Cube 90 degrees anti-clockwise on the y-axis direction
def _Y(FACES):
    _U(FACES)
    E(FACES)
    D(FACES)
    return FACES

# Rotate the Rubik's Cube 180 degrees on the y-axis direction
def Y2(FACES):
    U2(FACES)
    E2(FACES)
    D2(FACES)
    return FACES

# Rotate the Rubik's Cube 90 degrees clockwise on the z-axis direction
def Z(FACES):
    F(FACES)
    S(FACES)
    _B(FACES)
    return FACES

# Rotate the Rubik's Cube 90 degrees anti-clockwise on the z-axis direction
def _Z(FACES):
    _F(FACES)
    _S(FACES)
    B(FACES)
    return FACES

# Rotate the Rubik's Cube 180 degrees on the z-axis direction
def Z2(FACES):
    F2(FACES)
    S2(FACES)
    B2(FACES)
    return FACES

'''
                          |************|
                          |*U1**U2**U3*|
                          |************|
                          |*U4**U5**U6*|
                          |************|
                          |*U7**U8**U9*|
                          |************|
              ************|************|************|************|
              *L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*|
              ************|************|************|************|
              *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*|
              ************|************|************|************|
              *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*|
              ************|************|************|************|
                          |************|
                          |*D1**D2**D3*|
                          |************|
                          |*D4**D5**D6*|
                          |************|
                          |*D7**D8**D9*|
                          |************|
'''