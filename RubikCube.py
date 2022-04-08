import numpy as np
import copy as cp
import CubeActions
import random

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

class RubikCube():
    def __init__(self):

        # 创建六个面，放在faces列表里，顺序为上（0），下（1），左（2），右（3），前（4），后（5）
        self.initial = [np.zeros((3, 3))]
        for i in range(1, 6):
            self.initial.append(np.ones((3, 3)) + self.initial[i - 1])

        self.startState = self.randomGenerate()
        self.state = cp.deepcopy(self.startState)

        self.faces = {
            FRONT: np.full((3, 3), GREEN),
            LEFT: np.full((3, 3), ORANGE),
            RIGHT: np.full((3, 3), RED),
            TOP: np.full((3, 3), WHITE),
            BOTTOM: np.full((3, 3), YELLOW),
            BACK: np.full((3, 3), BLUE),
        }

        #
        self.CW = (1, 0)
        self.CCW = (0, 1)

        self.SINGLE_MOVES = ["U", "U'", "U2", "D", "D'", "D2",
                             "R", "R'", "R2", "L", "L'", "L2",
                             "F", "F'", "F2", "B", "B'", "B2"]

        self.ROTATIONS = ["x", "x'", "x2", "y", "y'", "y2"]
        self.ROTATIONS_Z = ["z", "z'", "z2"]
        self.PERMUTATIONS = [
            "D L D' L2 U L' B2 R' U R B2 U' L2".split(" "),
            "R' U L' U2 R U' L R' U L' U2 R U' L U'".split(" "),
            "L' U2 L R' F2 R".split(" "),
            "R' U2 R L' B2 L".split(" "),
            "M2 U M2 U2 M2 U M2".split(" "),
            "F' L' B' R' U' R U' B L F R U R' U".split(" "),
            "F R B L U L' U B' R' F' L' U' L U'".split(" "),
            "L U' R U2 L' U R' L U' R U2 L' U R' U".split(" "),
            "F' U B U' F U B' U'".split(" "),
            "F U' B' U F' U' B U".split(" "),
            "U2 B U2 B' R2 F R' F' U2 F' U2 F R'".split(" "),
            "U2 R U2 R' F2 L F' L' U2 L' U2 L F'".split(" "),
            "U' B2 D2 L' F2 D2 B2 R' U'".split(" "),
            "U B2 D2 R F2 D2 B2 L U".split(" "),
            "D' R' D R2 U' R B2 L U' L' B2 U R2".split(" ")
        ]

        self.moveMap = {
            # hortizontal
            "D": self.D, "D'": self.D_prime, "D2": self.D2,
            "E": self.E, "E'": self.E_prime, "E2": self.E2,
            "U": self.U, "U'": self.U_prime, "U2": self.U2,
            # vertical
            "L": self.L, "L'": self.L_prime, "L2": self.L2,
            "R": self.R, "R'": self.R_prime, "R2": self.R2,
            "M": self.M, "M'": self.M_prime, "M2": self.M2,
            # z
            "B": self.B, "B'": self.B_prime, "B2": self.B2,
            "F": self.F, "F'": self.F_prime, "F2": self.F2,
            "S": self.S, "S'": self.S_prime, "S2": self.S2,
            # full rotations
            "x": self.x_full, "x'": self.x_prime_full, "x2": self.x2_full,
            "y": self.y_full, "y'": self.y_prime_full, "y2": self.y2_full,
            "z": self.z_full, "z'": self.z_prime_full, "z2": self.z2_full,
        }
        self.movesLookup = {
            "D": CubeActions.D, "D'": CubeActions._D, "D2": CubeActions.D2,
            "E": CubeActions.E, "E'": CubeActions._E, "E2": CubeActions.E2,
            "U": CubeActions.U, "U'": CubeActions._U, "U2": CubeActions.U2,

            "L": CubeActions.L, "L'": CubeActions._L, "L2": CubeActions.L2,
            "R": CubeActions.R, "R'": CubeActions._R, "R2": CubeActions.R2,
            "M": CubeActions.M, "M'": CubeActions._M, "M2": CubeActions.M2,

            "B": CubeActions.B, "B'": CubeActions._B, "B2": CubeActions.B2,
            "F": CubeActions.F, "F'": CubeActions._F, "F2": CubeActions.F2,
            "S": CubeActions.S, "S'": CubeActions._S, "S2": CubeActions.S2,

            "x": CubeActions.X, "x'": CubeActions._X, "x2": CubeActions.X2,
            "y": CubeActions.Y, "y'": CubeActions._Y, "y2": CubeActions.Y2,
            "z": CubeActions.Z, "z'": CubeActions._Z, "z2": CubeActions.Z2,
        }
        self.moveHistory = []
        self.fitnessValue = 0

    def getInitialState(self):
        return self.initial

    def randomGenerate(self):
        startState = cp.deepcopy(self.initial)
        case0 = [CubeActions._U]
        case1 = [CubeActions.L,CubeActions.U]
        case2 = [CubeActions.B,CubeActions.M,CubeActions.L]
        case3 = [CubeActions.E,CubeActions.F,CubeActions._D,CubeActions.L]
        case4 = [CubeActions.U,CubeActions.S2, CubeActions._L,CubeActions._E,CubeActions.B]
        case5 = [CubeActions.U, CubeActions.S2, CubeActions._L, CubeActions._E, CubeActions.B, CubeActions.M]
        case6 = [CubeActions.L, CubeActions._S, CubeActions._B, CubeActions._L, CubeActions.B,CubeActions.M,CubeActions.B,]
        case7 = [CubeActions.U, CubeActions.S2, CubeActions.M,CubeActions._L, CubeActions._E, CubeActions.B, CubeActions.L,CubeActions.U]
        case8 = [ CubeActions.S2, CubeActions.M,CubeActions._L, CubeActions._E, CubeActions.B, CubeActions.E,CubeActions.F,CubeActions._D,CubeActions.L]
        case9 = [CubeActions.U, CubeActions.S2, CubeActions.M,CubeActions._L, CubeActions._E, CubeActions.B, CubeActions.E,CubeActions.F,CubeActions._D,CubeActions.L]


     # test cases
        for action in case9:
            startState = action(startState)
        # for i in range(100):
        #     startState = random.choice(actions)(startState)
        return startState

    def getStartState(self):
        return self.startState

    def getCurrentState(self):
        return self.state

    def getActions(self):
        actions = []
        for action in self.PERMUTATIONS:
            temp = []
            for a in action:
                temp.append(self.movesLookup[a])
            actions.append(temp)
        for i in self.ROTATIONS:
            for action in self.PERMUTATIONS:
                temp = []
                temp.append(self.movesLookup[i])
                for a in action:
                    temp.append(self.movesLookup[a])
            actions.append(temp)

        for i in self.ROTATIONS_Z:
            for action in self.PERMUTATIONS:
                temp = []
                temp.append(self.movesLookup[i])
                for a in action:
                    temp.append(self.movesLookup[a])
            actions.append(temp)

        for i in self.ROTATIONS:
            for j in self.ROTATIONS_Z:
                for action in self.PERMUTATIONS:
                    temp1, temp2 = [], []
                    temp1.append(self.movesLookup[i])
                    temp1.append(self.movesLookup[j])
                    temp2.append(self.movesLookup[j])
                    temp2.append(self.movesLookup[i])
                    for a in action:
                        temp1.append(self.movesLookup[a])
                        temp2.append(self.movesLookup[a])
                actions.append(temp1)
                actions.append(temp2)

        for i in self.PERMUTATIONS:
            for j in self.PERMUTATIONS:
                temp = []
                for a in i:
                    temp.append(self.movesLookup[a])
                for b in j:
                    temp.append(self.movesLookup[b])
                actions.append(temp)
        return actions

    def getBasicActions(self):
        actions = [CubeActions.B, CubeActions.D, CubeActions.F,
                   CubeActions.L, CubeActions.R, CubeActions.U,
                   CubeActions._B, CubeActions._D, CubeActions._F,
                   CubeActions._L, CubeActions._R, CubeActions._U,
                   CubeActions.B2, CubeActions.D2, CubeActions.F2,
                   CubeActions.L2, CubeActions.R2, CubeActions.U2,
                   CubeActions.E, CubeActions.S, CubeActions.M,
                   CubeActions._E, CubeActions._S, CubeActions._M,
                   CubeActions.E2, CubeActions.S2, CubeActions.M2,
                   ]
        return actions

    # def moveRotations(self):
    #     for action in self.ROTATIONS:
    #         self.move(action)
    #
    # def moveRotations_z(self):
    #     for action in self.ROTATIONS_Z:
    #         self.move(action)
    #
    # def movePermutations(self):
    #     for action in self.PERMUTATIONS:
    #         self.move(action)

    def execute(self, actions):
        for action in actions:
            # print(self.movesLookup[action])
            self.state = self.movesLookup[action](self.state)
            # print(self.state)
            # self.toString(self.state)
            # self.move(self.movesLookup[action])
        self.moveHistory.append(actions)
        self.fitness()

    def execute2(self, actions):
        for action in actions:
            # print(self.movesLookup[action])
            self.moveMap[action]()
            # print(self.state)
            # self.toString(self.state)
            # self.move(self.movesLookup[action])
        self.moveHistory.append(actions)
        self.fitness2()

    def move(self, action):
        self.state = action(self.state)

    def isTerminal(self, state):
        return np.array_equal(state, self.initial)

    def toString(self, state):
        print()
        for i in range(3):
            print("     ", int(state[0][i][0]), int(state[0][i][1]), int(state[0][i][2]))
        for i in range(3):
            print(int(state[2][i][0]), int(state[2][i][1]), int(state[2][i][2]), end=" ")
            print(int(state[4][i][0]), int(state[4][i][1]), int(state[4][i][2]), end=" ")
            print(int(state[3][i][0]), int(state[3][i][1]), int(state[3][i][2]), end=" ")
            print(int(state[5][i][0]), int(state[5][i][1]), int(state[5][i][2]))
        for i in range(3):
            print("     ", int(state[1][i][0]), int(state[1][i][1]), int(state[1][i][2]))
        print()

    def nextState(self, action, state):
        nextState = cp.deepcopy(state)
        for a in action:
            nextState = a(nextState)
        return nextState

    def reward(self, state, action):
        currentCompletion = np.array(state) - np.array(self.initial)
        currentCompletion = 54 - np.count_nonzero(currentCompletion)
        nextState = self.nextState(action, state)
        if self.isTerminal(nextState):
            reward = 100
        else:
            nextCompletion = np.array(nextState) - np.array(self.initial)
            nextCompletion = 54 - np.count_nonzero(nextCompletion)
            reward = nextCompletion - currentCompletion

        return reward

    def fitness(self):
        currentCompletion = np.array(self.state) - np.array(self.initial)
        currentCompletion = 54 - np.count_nonzero(currentCompletion)
        self.fitnessValue = currentCompletion
        return self.fitnessValue

    def fitness2(self):
        misplaced_stickers = 0

        for k, face in self.faces.items():
            # centers are fixed in a Rubik cube
            center = face[1, 1]

            for i in range(0, 3):
                for j in range(0, 3):
                    if face[i, j] != center:
                        misplaced_stickers += 1

        self.fitnessValue = misplaced_stickers

    def get_algorithm(self):
        # we don't want to include the scramble
        return [item for sublist in self.moveHistory[1:] for item in sublist]

    def get_algorithm_string(self):
        return " ".join(self.get_algorithm())

    def random_single_move(self):
        r = random.randint(0, len(self.SINGLE_MOVES) - 1)
        return [self.SINGLE_MOVES[r]]

    def random_permutation(self):
        r = random.randint(0, len(self.PERMUTATIONS) - 1)
        return self.PERMUTATIONS[r]

    def random_full_rotation(self):
        r = random.randint(0, len(self.ROTATIONS) - 1)
        return [self.ROTATIONS[r]]

    def random_orientation(self):
        r = random.randint(0, len(self.ROTATIONS_Z) - 1)
        return [self.ROTATIONS_Z[r]]

    def D(self):
        self.faces[BOTTOM] = np.rot90(self.faces[BOTTOM], axes=CLOCKWISE)
        self.__swap_x((FRONT, 2), (RIGHT, 2), (BACK, 2), (LEFT, 2))

    def D_prime(self):
        self.faces[BOTTOM] = np.rot90(self.faces[BOTTOM], axes=COUNTERCLOCKWISE)
        self.__swap_x((FRONT, 2), (LEFT, 2), (BACK, 2), (RIGHT, 2))

    def D2(self):
        self.D()
        self.D()

    def E(self):
        self.__swap_x((FRONT, 1), (RIGHT, 1), (BACK, 1), (LEFT, 1))

    def E_prime(self):
        self.__swap_x((FRONT, 1), (LEFT, 1), (BACK, 1), (RIGHT, 1))

    def E2(self):
        self.E()
        self.E()

    def U(self):
        self.faces[TOP] = np.rot90(self.faces[TOP], axes=CLOCKWISE)
        self.__swap_x((FRONT, 0), (LEFT, 0), (BACK, 0), (RIGHT, 0))

    def U_prime(self):
        self.faces[TOP] = np.rot90(self.faces[TOP], axes=COUNTERCLOCKWISE)
        self.__swap_x((FRONT, 0), (RIGHT, 0), (BACK, 0), (LEFT, 0))

    def U2(self):
        self.U()
        self.U()

    def __swap_x(self, t1, t2, t3, t4):
        backup = np.array(["", "", ""])
        self.__copy_stickers(backup, self.faces[t4[0]][t4[1]])
        self.__copy_stickers(self.faces[t4[0]][t4[1]], self.faces[t3[0]][t3[1]])
        self.__copy_stickers(self.faces[t3[0]][t3[1]], self.faces[t2[0]][t2[1]])
        self.__copy_stickers(self.faces[t2[0]][t2[1]], self.faces[t1[0]][t1[1]])
        self.__copy_stickers(self.faces[t1[0]][t1[1]], backup)

    def L(self):
        self.faces[LEFT] = np.rot90(self.faces[LEFT], axes=CLOCKWISE)
        self.__swap_y((BOTTOM, 0, True), (BACK, 2, True), (TOP, 0, False), (FRONT, 0, False))

    def L_prime(self):
        self.faces[LEFT] = np.rot90(self.faces[LEFT], axes=COUNTERCLOCKWISE)
        self.__swap_y((BOTTOM, 0, False), (FRONT, 0, False), (TOP, 0, True), (BACK, 2, True))

    def L2(self):
        self.L()
        self.L()

    def M(self):
        self.__swap_y((BOTTOM, 1, True), (BACK, 1, True), (TOP, 1, False), (FRONT, 1, False))

    def M_prime(self):
        self.__swap_y((BOTTOM, 1, False), (FRONT, 1, False), (TOP, 1, True), (BACK, 1, True))

    def M2(self):
        self.M()
        self.M()

    def R(self):
        self.faces[RIGHT] = np.rot90(self.faces[RIGHT], axes=CLOCKWISE)
        self.__swap_y((BOTTOM, 2, False), (FRONT, 2, False), (TOP, 2, True), (BACK, 0, True))

    def R_prime(self):
        self.faces[RIGHT] = np.rot90(self.faces[RIGHT], axes=COUNTERCLOCKWISE)
        self.__swap_y((BOTTOM, 2, True), (BACK, 0, True), (TOP, 2, False), (FRONT, 2, False))

    def R2(self):
        self.R()
        self.R()

    def __swap_y(self, t1, t2, t3, t4):
        backup = np.array(["", "", ""])

        if t4[2]:
            self.__copy_stickers(backup, np.flip(self.faces[t4[0]][:, t4[1]]))
        else:
            self.__copy_stickers(backup, self.faces[t4[0]][:, t4[1]])

        if t3[2]:
            self.__copy_stickers(self.faces[t4[0]][:, t4[1]], np.flip(self.faces[t3[0]][:, t3[1]]))
        else:
            self.__copy_stickers(self.faces[t4[0]][:, t4[1]], self.faces[t3[0]][:, t3[1]])

        if t2[2]:
            self.__copy_stickers(self.faces[t3[0]][:, t3[1]], np.flip(self.faces[t2[0]][:, t2[1]]))
        else:
            self.__copy_stickers(self.faces[t3[0]][:, t3[1]], self.faces[t2[0]][:, t2[1]])

        if t1[2]:
            self.__copy_stickers(self.faces[t2[0]][:, t2[1]], np.flip(self.faces[t1[0]][:, t1[1]]))
        else:
            self.__copy_stickers(self.faces[t2[0]][:, t2[1]], self.faces[t1[0]][:, t1[1]])

        self.__copy_stickers(self.faces[t1[0]][:, t1[1]], backup)


    def B(self):
        self.faces[BACK] = np.rot90(self.faces[BACK], axes=CLOCKWISE)
        self.__swap_z((BOTTOM, 2, True), (RIGHT, 2, False), (TOP, 0, True), (LEFT, 0, False))

    def B_prime(self):
        self.faces[BACK] = np.rot90(self.faces[BACK], axes=COUNTERCLOCKWISE)
        self.__swap_z((BOTTOM, 2, False), (LEFT, 0, True), (TOP, 0, False), (RIGHT, 2, True))

    def B2(self):
        self.B()
        self.B()

    def F(self):
        self.faces[FRONT] = np.rot90(self.faces[FRONT], axes=CLOCKWISE)
        self.__swap_z((BOTTOM, 0, False), (LEFT, 2, True), (TOP, 2, False), (RIGHT, 0, True))

    def F_prime(self):
        self.faces[FRONT] = np.rot90(self.faces[FRONT], axes=COUNTERCLOCKWISE)
        self.__swap_z((BOTTOM, 0, True), (RIGHT, 0, False), (TOP, 2, True), (LEFT, 2, False))

    def F2(self):
        self.F()
        self.F()

    def S(self):
        self.__swap_z((BOTTOM, 1, False), (LEFT, 1, True), (TOP, 1, False), (RIGHT, 1, True))

    def S_prime(self):
        self.__swap_z((BOTTOM, 1, True), (RIGHT, 1, False), (TOP, 1, True), (LEFT, 1, False))

    def S2(self):
        self.S()
        self.S()

    def __swap_z(self, t1, t2, t3, t4):
        backup = np.array(["", "", ""])

        if t4[2]:
            self.__copy_stickers(backup, np.flip(self.faces[t4[0]][:, t4[1]]))
        else:
            self.__copy_stickers(backup, self.faces[t4[0]][:, t4[1]])

        if t3[2]:
            self.__copy_stickers(self.faces[t4[0]][:, t4[1]], np.flip(self.faces[t3[0]][t3[1]]))
        else:
            self.__copy_stickers(self.faces[t4[0]][:, t4[1]], self.faces[t3[0]][t3[1]])

        if t2[2]:
            self.__copy_stickers(self.faces[t3[0]][t3[1]], np.flip(self.faces[t2[0]][:, t2[1]]))
        else:
            self.__copy_stickers(self.faces[t3[0]][t3[1]], self.faces[t2[0]][:, t2[1]])

        if t1[2]:
            self.__copy_stickers(self.faces[t2[0]][:, t2[1]], np.flip(self.faces[t1[0]][t1[1]]))
        else:
            self.__copy_stickers(self.faces[t2[0]][:, t2[1]], self.faces[t1[0]][t1[1]])

        self.__copy_stickers(self.faces[t1[0]][t1[1]], backup)

    def x_full(self):
        self.L_prime()
        self.M_prime()
        self.R()

    def x_prime_full(self):
        self.L()
        self.M()
        self.R_prime()

    def x2_full(self):
        self.x_full()
        self.x_full()

    def y_full(self):
        self.U()
        self.E_prime()
        self.D_prime()

    def y_prime_full(self):
        self.U_prime()
        self.E()
        self.D()

    def y2_full(self):
        self.y_full()
        self.y_full()

    def z_full(self):
        self.F()
        self.S()
        self.B_prime()

    def z_prime_full(self):
        self.F_prime()
        self.S_prime()
        self.B()

    def z2_full(self):
        self.z_full()
        self.z_full()

    def __copy_stickers(self, destination, origin):
        destination[0] = origin[0]
        destination[1] = origin[1]
        destination[2] = origin[2]

cube = RubikCube()
print(cube.getActions())
# cube.toString(cube.getInitialState())
# cube.toString(cube.getStartState())
# cube.toString(cube.getCurrentState())
# actions = cube.getActions()
# cube.move(actions[1])
# cube.toString(cube.getCurrentState())
# print(cube.isTerminal(cube.getCurrentState()))
# print(cube.isTerminal(cube.getInitialState()))
# print(cube.reward(cube.getStartState(),actions[1]))