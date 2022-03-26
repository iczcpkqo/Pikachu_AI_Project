import numpy as np


RED = "R"
GREEN = "G"
BLUE = "B"
ORANGE = "O"
YELLOW = "Y"
WHITE = "W"

TOP = "Top"
BOTTOM = "Bottom"
RIGHT = "Right"
LEFT = "Left"
FRONT = "Front"
BACK = "Back" 


CLOCKWISE = (1, 0)
COUNTERCLOCKWISE = (0, 1)


class Rubik:
    def __init__(self):
        self.moveHistory = []
        self.fitnessValue = 0

        self.faces = {
            FRONT: np.full((3, 3), RED),
            LEFT: np.full((3, 3), GREEN),
            RIGHT: np.full((3, 3), BLUE),
            TOP: np.full((3, 3), ORANGE),
            BOTTOM: np.full((3, 3), YELLOW),
            BACK: np.full((3, 3), WHITE),
        }

        self.movesLookup = {
            "D": self.d, "D'": self.d_prime, "D2": self.d2,
            "E": self.e, "E'": self.e_prime, "E2": self.e2,
            "U": self.u, "U'": self.u_prime, "U2": self.u2,

            "L": self.l, "L'": self.l_prime, "L2": self.l2,
            "R": self.r, "R'": self.r_prime, "R2": self.r2,
            "M": self.m, "M'": self.m_prime, "M2": self.m2,

            "B": self.b, "B'": self.b_prime, "B2": self.b2,
            "F": self.f, "F'": self.f_prime, "F2": self.f2,
            "S": self.s, "S'": self.s_prime, "S2": self.s2,

            "x": self.x_full, "x'": self.x_prime_full, "x2": self.x2_full,
            "y": self.y_full, "y'": self.y_prime_full, "y2": self.y2_full,
            "z": self.z_full, "z'": self.z_prime_full, "z2": self.z2_full,
        }

    ###
    #Moves
    ###
    def swap_x(self, t1, t2, t3, t4):
        backup = np.array(["", "", ""])
        self.copy_tiles(backup, self.faces[t4[0]][t4[1]])
        self.copy_tiles(self.faces[t4[0]][t4[1]], self.faces[t3[0]][t3[1]])
        self.copy_tiles(self.faces[t3[0]][t3[1]], self.faces[t2[0]][t2[1]])
        self.copy_tiles(self.faces[t2[0]][t2[1]], self.faces[t1[0]][t1[1]])
        self.copy_tiles(self.faces[t1[0]][t1[1]], backup)

    def copy_tiles(self, destination, origin):
        destination[0] = origin[0]
        destination[1] = origin[1]
        destination[2] = origin[2]
# X轴上的操作
# 拧最下面那一层90（逆
    def d(self):
        self.faces[BOTTOM] = np.rot90(self.faces[BOTTOM], axes=CLOCKWISE)
        self.swap_x((FRONT, 2), (RIGHT, 2), (BACK, 2), (LEFT, 2))
# 顺
    def d_prime(self):
        self.faces[BOTTOM] = np.rot90(self.faces[BOTTOM], axes=COUNTERCLOCKWISE)
        self.swap_x((FRONT, 2), (LEFT, 2), (BACK, 2), (RIGHT, 2))
# 拧180
    def d2(self):
        self.d()
        self.d()

# 拧中间一层90
    def e(self):
        self.swap_x((FRONT, 1), (RIGHT, 1), (BACK, 1), (LEFT, 1))
#
    def e_prime(self):
        self.swap_x((FRONT, 1), (LEFT, 1), (BACK, 1), (RIGHT, 1))

    def e2(self):
        self.e()
        self.e()
# 拧最上面一层
    def u(self):
        self.faces[TOP] = np.rot90(self.faces[TOP], axes=CLOCKWISE)
        self.swap_x((FRONT, 0), (LEFT, 0), (BACK, 0), (RIGHT, 0))

    def u_prime(self):
        self.faces[TOP] = np.rot90(self.faces[TOP], axes=COUNTERCLOCKWISE)
        self.swap_x((FRONT, 0), (RIGHT, 0), (BACK, 0), (LEFT, 0))

    def u2(self):
        self.u()
        self.u()

# y轴上的操作

    def swap_y(self, t1, t2, t3, t4):
        backup = np.array(["", "", ""])

        if t4[2]:
            self.copy_tiles(backup, np.flip(self.faces[t4[0]][:, t4[1]]))
        else:
            self.copy_tiles(backup, self.faces[t4[0]][:, t4[1]])

        if t3[2]:
            self.copy_tiles(self.faces[t4[0]][:, t4[1]], np.flip(self.faces[t3[0]][:, t3[1]]))
        else:
            self.copy_tiles(self.faces[t4[0]][:, t4[1]], self.faces[t3[0]][:, t3[1]])

        if t2[2]:
            self.copy_tiles(self.faces[t3[0]][:, t3[1]], np.flip(self.faces[t2[0]][:, t2[1]]))
        else:
            self.copy_tiles(self.faces[t3[0]][:, t3[1]], self.faces[t2[0]][:, t2[1]])

        if t1[2]:
            self.copy_tiles(self.faces[t2[0]][:, t2[1]], np.flip(self.faces[t1[0]][:, t1[1]]))
        else:
            self.copy_tiles(self.faces[t2[0]][:, t2[1]], self.faces[t1[0]][:, t1[1]])

        self.copy_tiles(self.faces[t1[0]][:, t1[1]], backup)

# 拧最左边那一列90（逆
    def l(self):
        self.faces[LEFT] = np.rot90(self.faces[LEFT], axes=CLOCKWISE)
        self.swap_y((BOTTOM, 0, True), (BACK, 2, True), (TOP, 0, False), (FRONT, 0, False))
# 顺90
    def l_prime(self):
        self.faces[LEFT] = np.rot90(self.faces[LEFT], axes=COUNTERCLOCKWISE)
        self.swap_y((BOTTOM, 0, False), (FRONT, 0, False), (TOP, 0, True), (BACK, 2, True))

    def l2(self):
        self.l()
        self.l()
# 拧中间一列90逆
    def m(self):
        self.swap_y((BOTTOM, 1, True), (BACK, 1, True), (TOP, 1, False), (FRONT, 1, False))
# 顺
    def m_prime(self):
        self.swap_y((BOTTOM, 1, False), (FRONT, 1, False), (TOP, 1, True), (BACK, 1, True))

    def m2(self):
        self.m()
        self.m()
# 拧最右边一列
    def r(self):
        self.faces[RIGHT] = np.rot90(self.faces[RIGHT], axes=CLOCKWISE)
        self.swap_y((BOTTOM, 2, False), (FRONT, 2, False), (TOP, 2, True), (BACK, 0, True))

    def r_prime(self):
        self.faces[RIGHT] = np.rot90(self.faces[RIGHT], axes=COUNTERCLOCKWISE)
        self.swap_y((BOTTOM, 2, True), (BACK, 0, True), (TOP, 2, False), (FRONT, 2, False))

    def r2(self):
        self.r()
        self.r()

    def swap_z(self, t1, t2, t3, t4):
        backup = np.array(["", "", ""])

        if t4[2]:
            self.copy_tiles(backup, np.flip(self.faces[t4[0]][:, t4[1]]))
        else:
            self.copy_tiles(backup, self.faces[t4[0]][:, t4[1]])

        if t3[2]:
            self.copy_tiles(self.faces[t4[0]][:, t4[1]], np.flip(self.faces[t3[0]][t3[1]]))
        else:
            self.copy_tiles(self.faces[t4[0]][:, t4[1]], self.faces[t3[0]][t3[1]])

        if t2[2]:
            self.copy_tiles(self.faces[t3[0]][t3[1]], np.flip(self.faces[t2[0]][:, t2[1]]))
        else:
            self.copy_tiles(self.faces[t3[0]][t3[1]], self.faces[t2[0]][:, t2[1]])

        if t1[2]:
            self.copy_tiles(self.faces[t2[0]][:, t2[1]], np.flip(self.faces[t1[0]][t1[1]]))
        else:
            self.copy_tiles(self.faces[t2[0]][:, t2[1]], self.faces[t1[0]][t1[1]])

        self.copy_tiles(self.faces[t1[0]][t1[1]], backup)

# 最后边那一层90逆
    def b(self):
        self.faces[BACK] = np.rot90(self.faces[BACK], axes=CLOCKWISE)
        self.swap_z((BOTTOM, 2, True), (RIGHT, 2, False), (TOP, 0, True), (LEFT, 0, False))

    def b_prime(self):
        self.faces[BACK] = np.rot90(self.faces[BACK], axes=COUNTERCLOCKWISE)
        self.swap_z((BOTTOM, 2, False), (LEFT, 0, True), (TOP, 0, False), (RIGHT, 2, True))

    def b2(self):
        self.b()
        self.b()
# 最前边那一层90逆
    def f(self):
        self.faces[FRONT] = np.rot90(self.faces[FRONT], axes=CLOCKWISE)
        self.swap_z((BOTTOM, 0, False), (LEFT, 2, True), (TOP, 2, False), (RIGHT, 0, True))

    def f_prime(self):
        self.faces[FRONT] = np.rot90(self.faces[FRONT], axes=COUNTERCLOCKWISE)
        self.swap_z((BOTTOM, 0, True), (RIGHT, 0, False), (TOP, 2, True), (LEFT, 2, False))

    def f2(self):
        self.f()
        self.f()
# 中间那一层90逆
    def s(self):
        self.swap_z((BOTTOM, 1, False), (LEFT, 1, True), (TOP, 1, False), (RIGHT, 1, True))

    def s_prime(self):
        self.swap_z((BOTTOM, 1, True), (RIGHT, 1, False), (TOP, 1, True), (LEFT, 1, False))

    def s2(self):
        self.s()
        self.s()

# 上面变前面
    def x_full(self):
        self.l_prime() # y轴最左边一列顺时针拧90
        self.m_prime() # y轴中间一列拧90
        self.r()  # y轴拧最右边那一列逆90

# 上面变后面
    def x_prime_full(self):
        self.l()
        self.m()
        self.r_prime()
# 上面变下面
    def x2_full(self):
        self.x_full()
        self.x_full()
# 正面变右面
    def y_full(self):
        self.u()
        self.e_prime()
        self.d_prime()
# 正面变左面
    def y_prime_full(self):
        self.u_prime()
        self.e()
        self.d()
# 正面变背面
    def y2_full(self):
        self.y_full()
        self.y_full()
# 上面变左面
    def z_full(self):
        self.f()
        self.s()
        self.b_prime()
# 上面变右面
    def z_prime_full(self):
        self.f_prime()
        self.s_prime()
        self.b()
# 上面变下面
    def z2_full(self):
        self.z_full()
        self.z_full()
    ###
    #End of moves
    ###


    def execute(self, moves):
        for move in moves:
            self.movesLookup[move]()

        self.moveHistory.append(moves)
        self.fitness()


    def fitness(self):
        mismatchedTiles = 0

        for _, face in self.faces.items():
            centerTile = face[1, 1]

            for i in range(0, 3):
                for j in range(0, 3):
                    if face[i, j] != centerTile:
                        mismatchedTiles += 1

        self.fitnessValue = mismatchedTiles
        return self.fitnessValue


    def get_face_string(self, face):
        m = self.faces[face]
        return f"{m[0, 0]} {m[0, 1]} {m[0, 2]} - {m[1, 0]} {m[1, 1]} {m[1, 2]} - {m[2, 0]} {m[2, 1]} {m[2, 2]}"

    def get_scramble(self):
        return self.moveHistory[0]

    def get_scramble_string(self):
        return " ".join(self.get_scramble())

    def get_algorithm(self):
        # we don't want to include the scramble
        return [item for sublist in self.moveHistory[1:] for item in sublist]
        

    def get_algorithm_string(self):
        return " ".join(self.get_algorithm())
