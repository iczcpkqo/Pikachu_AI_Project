import numpy as np
import copy as cp
import CubeActions
import FaceActions
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


class RubikCube():
    def __init__(self):
        # up（0），down（1），left（2），right（3），front（4），back（5）
        self.initial = [np.zeros((3, 3))]
        for i in range(1, 6):
            self.initial.append(np.ones((3, 3)) + self.initial[i - 1])

        self.startState = self.randomGenerate()
        self.state = cp.deepcopy(self.initial)

        self.faces = {
            FRONT: np.full((3, 3), GREEN),
            LEFT: np.full((3, 3), ORANGE),
            RIGHT: np.full((3, 3), RED),
            TOP: np.full((3, 3), WHITE),
            BOTTOM: np.full((3, 3), YELLOW),
            BACK: np.full((3, 3), BLUE),
        }

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

        self.faceMoveMap = {
            # hortizontal
            "D": FaceActions.D, "D'": FaceActions.D_prime, "D2": FaceActions.D2,
            "E": FaceActions.E, "E'": FaceActions.E_prime, "E2": FaceActions.E2,
            "U": FaceActions.U, "U'": FaceActions.U_prime, "U2": FaceActions.U2,
            # vertical
            "L": FaceActions.L, "L'": FaceActions.L_prime, "L2": FaceActions.L2,
            "R": FaceActions.R, "R'": FaceActions.R_prime, "R2": FaceActions.R2,
            "M": FaceActions.M, "M'": FaceActions.M_prime, "M2": FaceActions.M2,
            # z
            "B": FaceActions.B, "B'": FaceActions.B_prime, "B2": FaceActions.B2,
            "F": FaceActions.F, "F'": FaceActions.F_prime, "F2": FaceActions.F2,
            "S": FaceActions.S, "S'": FaceActions.S_prime, "S2": FaceActions.S2,
            # full rotations
            "x": FaceActions.x_full, "x'": FaceActions.x_prime_full, "x2": FaceActions.x2_full,
            "y": FaceActions.y_full, "y'": FaceActions.y_prime_full, "y2": FaceActions.y2_full,
            "z": FaceActions.z_full, "z'": FaceActions.z_prime_full, "z2": FaceActions.z2_full,
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
        case1 = [CubeActions.L, CubeActions.U]
        case2 = [CubeActions.B, CubeActions.M, CubeActions.L]
        case3 = [CubeActions.E, CubeActions.F, CubeActions._D, CubeActions.L]
        case4 = [CubeActions.U, CubeActions.S2, CubeActions._L, CubeActions._E, CubeActions.B]
        case5 = [CubeActions.U, CubeActions.S2, CubeActions._L, CubeActions._E, CubeActions.B, CubeActions.M]
        case6 = [CubeActions.L, CubeActions._S, CubeActions._B, CubeActions._L, CubeActions.B, CubeActions.M,
                 CubeActions.B, ]
        case7 = [CubeActions.U, CubeActions.S2, CubeActions.M, CubeActions._L, CubeActions._E, CubeActions.B,
                 CubeActions.L, CubeActions.U]
        case8 = [CubeActions.S2, CubeActions.M, CubeActions._L, CubeActions._E, CubeActions.B, CubeActions.E,
                 CubeActions.F, CubeActions._D, CubeActions.L]
        case9 = [CubeActions.U, CubeActions.S2, CubeActions.M, CubeActions._L, CubeActions._E, CubeActions.B,
                 CubeActions.E, CubeActions.F, CubeActions._D, CubeActions.L]

        # test cases
        for action in case2:
            startState = action(startState)
        # for i in range(100):
        #     startState = random.choice(actions)(startState)
        return startState

    def randomScrambler(self, times):
        scramble_str = ''
        for i in range(times):
            scramble_str = scramble_str + list(cube.faceMoveMap.keys())[random.randint(0, len(self.faceMoveMap) - 1)] + " "
        scramble_str = scramble_str[:-1]
        return scramble_str.split(" ")

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

    def execute(self, actions):
        for action in actions:
            self.state = self.movesLookup[action](self.state)
        self.moveHistory.append(actions)
        self.fitness()

    def execute2(self, actions):
        for action in actions:
            self.faces = self.faceMoveMap[action](self.faces)
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

    def toStringi(self):
        print()
        for i in range(3):
            print("     ", int(self.initial[0][i][0]), int(self.initial[0][i][1]), int(self.initial[0][i][2]))
        for i in range(3):
            print(int(self.initial[2][i][0]), int(self.initial[2][i][1]), int(self.initial[2][i][2]), end=" ")
            print(int(self.initial[4][i][0]), int(self.initial[4][i][1]), int(self.initial[4][i][2]), end=" ")
            print(int(self.initial[3][i][0]), int(self.initial[3][i][1]), int(self.initial[3][i][2]), end=" ")
            print(int(self.initial[5][i][0]), int(self.initial[5][i][1]), int(self.initial[5][i][2]))
        for i in range(3):
            print("     ", int(self.initial[1][i][0]), int(self.initial[1][i][1]), int(self.initial[1][i][2]))
        print()

    def getFaces(self):
        result = ''
        result = result + 'Front:' + '\n' + str(self.faces.get('Front')) + '\n'
        result = result + 'Left:' + '\n' + str(self.faces.get('Left')) + '\n'
        result = result + 'Back:' + '\n' + str(self.faces.get('Back')) + '\n'
        result = result + 'Right:' + '\n' + str(self.faces.get('Right')) + '\n'
        result = result + 'Top:' + '\n' + str(self.faces.get('Top')) + '\n'
        result = result + 'Bottom:' + '\n' + str(self.faces.get('Bottom')) + '\n'
        return result

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

    # def fitness(self):
    #     currentCompletion = np.array(self.state) - np.array(self.initial)
    #     currentCompletion = 54 - np.count_nonzero(currentCompletion)
    #     self.fitnessValue = currentCompletion
    #     return self.fitnessValue

    def fitness(self):
        misplaced_stickers = 0
        for face in self.state:
            center = face[1, 1]
            for i in range(0, 3):
                for j in range(0, 3):
                    if face[i, j] != center:
                        misplaced_stickers += 1
        self.fitnessValue = misplaced_stickers

    def fitness2(self):
        misplaced_stickers = 0
        for k, face in self.faces.items():
            center = face[1, 1]
            for i in range(0, 3):
                for j in range(0, 3):
                    if face[i, j] != center:
                        misplaced_stickers += 1
        self.fitnessValue = misplaced_stickers

    def get_algorithm(self):
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


cube = RubikCube()
print(cube.randomScrambler(5))
# print(cube.getActions())
# cube.toString(cube.getInitialState())
# cube.toString(cube.getStartState())
# cube.toString(cube.getCurrentState())
# actions = cube.getActions()
# cube.move(actions[1])
# cube.toString(cube.getCurrentState())
# print(cube.isTerminal(cube.getCurrentState()))
# print(cube.isTerminal(cube.getInitialState()))
# print(cube.reward(cube.getStartState(),actions[1]))
