import numpy as np
import copy as cp
import CubeActions2
import random

class RubikCube():
    def __init__(self):
        # 创建六个面，放在faces列表里，顺序为上（0），下（1），左（2），右（3），前（4），后（5）
        self.initial = [np.zeros((2, 2))]
        for i in range(1, 6):
            self.initial.append(np.ones((2, 2)) + self.initial[i - 1])

        self.startState = self.randomGenerate()
        self.state = cp.deepcopy(self.startState)

    def getInitialState(self):
        return self.initial

    def randomGenerate(self):
        startState = cp.deepcopy(self.initial)
        actions = self.getActions()
        for i in range(100):
            startState = random.choice(actions)(startState)
        return startState

    def getStartState(self):
        return self.startState

    def getCurrentState(self):
        return self.state

    def getActions(self):
        actions = [CubeActions2.B, CubeActions2.D, CubeActions2.F,
                   CubeActions2.L, CubeActions2.R, CubeActions2.U,
                   CubeActions2._B, CubeActions2._D, CubeActions2._F,
                   CubeActions2._L, CubeActions2._R, CubeActions2._U
                   ]
        return actions

    def move(self,action):
        self.state = action(self.state)

    def isTerminal(self,state):
        return np.array_equal(state,self.initial)

    def toString(self,state):
        print()
        for i in range(2):
            print("   ", int(state[0][i][0]), int(state[0][i][1]))
        for i in range(2):
            print(int(state[2][i][0]), int(state[2][i][1]), end=" ")
            print(int(state[4][i][0]), int(state[4][i][1]), end=" ")
            print(int(state[3][i][0]), int(state[3][i][1]), end=" ")
            print(int(state[5][i][0]), int(state[5][i][1]))
        for i in range(2):
            print("   ", int(state[1][i][0]), int(state[1][i][1]))
        print()

    def reward(self,state,action):
        currentCompletion = np.array(state) - np.array(self.initial)
        currentCompletion = 24 - np.count_nonzero(currentCompletion)
        nextState = action(state)
        if self.isTerminal(nextState):
            reward = 100
        else:
            nextCompletion = np.array(nextState) - np.array(self.initial)
            nextCompletion = 24 - np.count_nonzero(nextCompletion)
            reward = nextCompletion-currentCompletion

        return reward

cube = RubikCube()
# cube.toString(cube.getInitialState())
# cube.toString(cube.getStartState())
# cube.toString(cube.getCurrentState())
# actions = cube.getActions()
# cube.toString(actions[1](cube.getInitialState()))
# cube.move(actions[1])
# cube.toString(cube.getCurrentState())
# print(cube.isTerminal(cube.getCurrentState()))
# print(cube.isTerminal(cube.getInitialState()))
# print(cube.reward(cube.getStartState(),actions[1]))