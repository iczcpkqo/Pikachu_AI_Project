import numpy as np

GREEN = "G"
ORANGE = "O"
RED = "R"
WHITE = "W"
YELLOW = "Y"
BLUE = "B"

FRONT = "Front"
LEFT = "Left"
BACK = "Back"
RIGHT = "Right"
TOP = "Top"
BOTTOM = "Bottom"

CLOCKWISE = (1, 0)
COUNTERCLOCKWISE = (0, 1)


def D(faces):
    faces[BOTTOM] = np.rot90(faces[BOTTOM], axes=CLOCKWISE)
    faces = __swap_x(faces, (FRONT, 2), (RIGHT, 2), (BACK, 2), (LEFT, 2))
    return faces


def D_prime(faces):
    faces[BOTTOM] = np.rot90(faces[BOTTOM], axes=COUNTERCLOCKWISE)
    faces = __swap_x(faces, (FRONT, 2), (LEFT, 2), (BACK, 2), (RIGHT, 2))
    return faces


def D2(faces):
    faces = D(faces)
    faces = D(faces)
    return faces


def E(faces):
    faces = __swap_x(faces, (FRONT, 1), (RIGHT, 1), (BACK, 1), (LEFT, 1))
    return faces


def E_prime(faces):
    faces = __swap_x(faces, (FRONT, 1), (LEFT, 1), (BACK, 1), (RIGHT, 1))
    return faces


def E2(faces):
    faces = E(faces)
    faces = E(faces)
    return faces


def U(faces):
    faces[TOP] = np.rot90(faces[TOP], axes=CLOCKWISE)
    faces = __swap_x(faces, (FRONT, 0), (LEFT, 0), (BACK, 0), (RIGHT, 0))
    return faces


def U_prime(faces):
    faces[TOP] = np.rot90(faces[TOP], axes=COUNTERCLOCKWISE)
    faces = __swap_x(faces, (FRONT, 0), (RIGHT, 0), (BACK, 0), (LEFT, 0))
    return faces


def U2(faces):
    faces = U(faces)
    faces = U(faces)
    return faces


def __swap_x(faces, t1, t2, t3, t4):
    backup = np.array(["", "", ""])
    __copy_stickers(backup, faces[t4[0]][t4[1]])
    __copy_stickers(faces[t4[0]][t4[1]], faces[t3[0]][t3[1]])
    __copy_stickers(faces[t3[0]][t3[1]], faces[t2[0]][t2[1]])
    __copy_stickers(faces[t2[0]][t2[1]], faces[t1[0]][t1[1]])
    __copy_stickers(faces[t1[0]][t1[1]], backup)
    return faces


def L(faces):
    faces[LEFT] = np.rot90(faces[LEFT], axes=CLOCKWISE)
    faces = __swap_y(faces, (BOTTOM, 0, True), (BACK, 2, True), (TOP, 0, False), (FRONT, 0, False))
    return faces


def L_prime(faces):
    faces[LEFT] = np.rot90(faces[LEFT], axes=COUNTERCLOCKWISE)
    faces = __swap_y(faces, (BOTTOM, 0, False), (FRONT, 0, False), (TOP, 0, True), (BACK, 2, True))
    return faces


def L2(faces):
    faces = L(faces)
    faces = L(faces)
    return faces


def M(faces):
    faces = __swap_y(faces, (BOTTOM, 1, True), (BACK, 1, True), (TOP, 1, False), (FRONT, 1, False))
    return faces


def M_prime(faces):
    faces = __swap_y(faces, (BOTTOM, 1, False), (FRONT, 1, False), (TOP, 1, True), (BACK, 1, True))
    return faces


def M2(faces):
    faces = M(faces)
    faces = M(faces)
    return faces


def R(faces):
    faces[RIGHT] = np.rot90(faces[RIGHT], axes=CLOCKWISE)
    faces = __swap_y(faces, (BOTTOM, 2, False), (FRONT, 2, False), (TOP, 2, True), (BACK, 0, True))
    return faces


def R_prime(faces):
    faces[RIGHT] = np.rot90(faces[RIGHT], axes=COUNTERCLOCKWISE)
    faces = __swap_y(faces, (BOTTOM, 2, True), (BACK, 0, True), (TOP, 2, False), (FRONT, 2, False))
    return faces


def R2(faces):
    faces = R(faces)
    faces = R(faces)
    return faces


def __swap_y(faces, t1, t2, t3, t4):
    backup = np.array(["", "", ""])

    if t4[2]:
        __copy_stickers(backup, np.flip(faces[t4[0]][:, t4[1]]))
    else:
        __copy_stickers(backup, faces[t4[0]][:, t4[1]])

    if t3[2]:
        __copy_stickers(faces[t4[0]][:, t4[1]], np.flip(faces[t3[0]][:, t3[1]]))
    else:
        __copy_stickers(faces[t4[0]][:, t4[1]], faces[t3[0]][:, t3[1]])

    if t2[2]:
        __copy_stickers(faces[t3[0]][:, t3[1]], np.flip(faces[t2[0]][:, t2[1]]))
    else:
        __copy_stickers(faces[t3[0]][:, t3[1]], faces[t2[0]][:, t2[1]])

    if t1[2]:
        __copy_stickers(faces[t2[0]][:, t2[1]], np.flip(faces[t1[0]][:, t1[1]]))
    else:
        __copy_stickers(faces[t2[0]][:, t2[1]], faces[t1[0]][:, t1[1]])

    __copy_stickers(faces[t1[0]][:, t1[1]], backup)
    return faces


def B(faces):
    faces[BACK] = np.rot90(faces[BACK], axes=CLOCKWISE)
    faces = __swap_z(faces, (BOTTOM, 2, True), (RIGHT, 2, False), (TOP, 0, True), (LEFT, 0, False))
    return faces


def B_prime(faces):
    faces[BACK] = np.rot90(faces[BACK], axes=COUNTERCLOCKWISE)
    faces = __swap_z(faces, (BOTTOM, 2, False), (LEFT, 0, True), (TOP, 0, False), (RIGHT, 2, True))
    return faces


def B2(faces):
    faces = B(faces)
    faces = B(faces)
    return faces


def F(faces):
    faces[FRONT] = np.rot90(faces[FRONT], axes=CLOCKWISE)
    faces = __swap_z(faces, (BOTTOM, 0, False), (LEFT, 2, True), (TOP, 2, False), (RIGHT, 0, True))
    return faces


def F_prime(faces):
    faces[FRONT] = np.rot90(faces[FRONT], axes=COUNTERCLOCKWISE)
    faces = __swap_z(faces, (BOTTOM, 0, True), (RIGHT, 0, False), (TOP, 2, True), (LEFT, 2, False))
    return faces


def F2(faces):
    faces = F(faces)
    faces = F(faces)
    return faces


def S(faces):
    faces = __swap_z(faces, (BOTTOM, 1, False), (LEFT, 1, True), (TOP, 1, False), (RIGHT, 1, True))
    return faces


def S_prime(faces):
    faces = __swap_z(faces, (BOTTOM, 1, True), (RIGHT, 1, False), (TOP, 1, True), (LEFT, 1, False))
    return faces


def S2(faces):
    faces = S(faces)
    faces = S(faces)
    return faces


def __swap_z(faces, t1, t2, t3, t4):
    backup = np.array(["", "", ""])

    if t4[2]:
        __copy_stickers(backup, np.flip(faces[t4[0]][:, t4[1]]))
    else:
        __copy_stickers(backup, faces[t4[0]][:, t4[1]])

    if t3[2]:
        __copy_stickers(faces[t4[0]][:, t4[1]], np.flip(faces[t3[0]][t3[1]]))
    else:
        __copy_stickers(faces[t4[0]][:, t4[1]], faces[t3[0]][t3[1]])

    if t2[2]:
        __copy_stickers(faces[t3[0]][t3[1]], np.flip(faces[t2[0]][:, t2[1]]))
    else:
        __copy_stickers(faces[t3[0]][t3[1]], faces[t2[0]][:, t2[1]])

    if t1[2]:
        __copy_stickers(faces[t2[0]][:, t2[1]], np.flip(faces[t1[0]][t1[1]]))
    else:
        __copy_stickers(faces[t2[0]][:, t2[1]], faces[t1[0]][t1[1]])

    __copy_stickers(faces[t1[0]][t1[1]], backup)
    return faces


def x_full(faces):
    faces = L_prime(faces)
    faces = M_prime(faces)
    faces = R(faces)
    return faces


def x_prime_full(faces):
    faces = L(faces)
    faces = M(faces)
    faces = R_prime(faces)
    return faces


def x2_full(faces):
    faces = x_full(faces)
    faces = x_full(faces)
    return faces


def y_full(faces):
    faces = U(faces)
    faces = E_prime(faces)
    faces = D_prime(faces)
    return faces


def y_prime_full(faces):
    faces = U_prime(faces)
    faces = E(faces)
    faces = D(faces)
    return faces


def y2_full(faces):
    faces = y_full(faces)
    faces = y_full(faces)
    return faces


def z_full(faces):
    faces = F(faces)
    faces = S(faces)
    faces = B_prime(faces)
    return faces


def z_prime_full(faces):
    faces = F_prime(faces)
    faces = S_prime(faces)
    faces = B(faces)
    return faces


def z2_full(faces):
    faces = z_full(faces)
    faces = z_full(faces)
    return faces


def __copy_stickers(destination, origin):
    destination[0] = origin[0]
    destination[1] = origin[1]
    destination[2] = origin[2]
