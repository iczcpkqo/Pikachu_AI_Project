import numpy as np
import copy as cp
import CubeActions
import random

class RubikCube():
    def __init__(self):
        # up（0），down（1），left（2），right（3），front（4），back（5）
        self.initial = [np.zeros((3, 3))]
        for i in range(1, 6):
            self.initial.append(np.ones((3, 3)) + self.initial[i - 1])

        self.startState = self.randomGenerate()
        self.state = cp.deepcopy(self.initial)

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
        for action in case9:
            startState = action(startState)
        # for i in range(100):
        #     startState = random.choice(actions)(startState)
        return startState

    def randomScrambler(self, times):
        scramble_str = ''
        for i in range(times):
            scramble_str = scramble_str + list(cube.movesLookup.keys())[random.randint(0, len(self.movesLookup) - 1)] + " "
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

    def executeSA(self, actions):
        for action in actions:
            self.state = self.movesLookup[action](self.state)
        self.moveHistory.append(actions)
        self.fitnessSA()

    def execute(self, actions):
        for action in actions:
            self.state = self.movesLookup[action](self.state)
        self.moveHistory.append(actions)
        self.fitness()

    def move(self, action):
        self.state = action(self.state)

    def isTerminal(self, state):
        if self.correctNum(state) == 54:
            return True
        else:
            return False
        # return np.array_equal(state, self.initial)

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

    def correctNum(self, state):
        right_stickers = 0
        for face in state:
            center = face[1, 1]
            for i in range(0, 3):
                for j in range(0, 3):
                    if face[i, j] == center:
                        right_stickers += 1
        return right_stickers

    def reward(self, state, action):
        currentCompletion = self.correctNum(state)
        nextState = self.nextState(action, state)
        if self.isTerminal(nextState):
            reward = 100
        else:
            nextCompletion = self.correctNum(nextState)
            reward = nextCompletion - currentCompletion

        return reward

    def fitnessSA(self):
        currentCompletion = np.array(self.state) - np.array(self.initial)
        currentCompletion = 54 - np.count_nonzero(currentCompletion)
        self.fitnessValue = currentCompletion
        return self.fitnessValue

    def fitness(self):
        miss_stickers = 0
        for face in self.state:
            center = face[1, 1]
            for i in range(0, 3):
                for j in range(0, 3):
                    if face[i, j] != center:
                        miss_stickers += 1
        self.fitnessValue = miss_stickers
        return self.fitnessValue

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
