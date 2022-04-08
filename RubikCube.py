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

class RubikCube():
    def __init__(self):

        # 创建六个面，放在faces列表里，顺序为上（0），下（1），左（2），右（3），前（4），后（5）
        self.initial = [np.zeros((3, 3))]
        for i in range(1, 6):
            self.initial.append(np.ones((3, 3)) + self.initial[i - 1])

        self.startState = self.initial
        self.state = cp.deepcopy(self.startState)

        self.faces = {
            FRONT: np.full((3, 3), GREEN),
            LEFT: np.full((3, 3), ORANGE),
            RIGHT: np.full((3, 3), RED),
            TOP: np.full((3, 3), WHITE),
            BOTTOM: np.full((3, 3), YELLOW),
            BACK: np.full((3, 3), BLUE),
        }

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
        case1 = [CubeActions.L, CubeActions.U]
        case2 = [CubeActions.B, CubeActions.M, CubeActions.L]
        case3 = [CubeActions.E, CubeActions.F, CubeActions._D, CubeActions.L]
        case4 = [CubeActions.U, CubeActions.S2, CubeActions._L, CubeActions._E, CubeActions.B]
        for action in case1:
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
                    temp1,temp2 = [],[]
                    temp1.append(self.movesLookup[i])
                    temp1.append(self.movesLookup[j])
                    temp2.append(self.movesLookup[j])
                    temp2.append(self.movesLookup[i])
                    for a in action:
                        temp1.append(self.movesLookup[a])
                        temp2.append(self.movesLookup[a])
                actions.append(temp1)
                actions.append(temp2)
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
            self.state = self.movesLookup[action](self.state)
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
        currentCompletion = np.array(self.state) - np.array(self.initial)
        currentCompletion = np.count_nonzero(currentCompletion)
        self.fitnessValue = currentCompletion
        return self.fitnessValue


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

    def copy(self, cube_to, cube_from):
        for f in cube_from.faces:
            for i in range(0, 3):
                for j in range(0, 3):
                    cube_to.faces[f][i, j] = cube_from.faces[f][i, j]

        cube_to.moveHistory = [item for item in cube_from.moveHistory]
        cube_to.fitness = cube_from.fitness


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
