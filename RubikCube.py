import numpy as np
import CubeActions
import random

class RubikCube():
    def __init__(self):
        # 创建六个面，放在faces列表里，顺序为上（0），下（1），左（2），右（3），前（4），后（5）
        self.faces = [np.zeros((3, 3))]
        for i in range(1, 6):
            self.faces.append(np.ones((3, 3)) + self.faces[i - 1])

    def randomGenerate(self):
        actions = self.getActions()
        for i in range(100):
            self.faces = random.choice(actions)(self.faces)

    def getCube(self):
        return self.faces

    def getActions(self):
        actions = [CubeActions.B, CubeActions.D, CubeActions.F,
                   CubeActions.L, CubeActions.R, CubeActions.U,
                   CubeActions._B, CubeActions._D, CubeActions._F,
                   CubeActions._L, CubeActions._R, CubeActions._U
                   ]
        return actions

    def toString(self):
        print()
        for i in range(3):
            print("     ", int(self.faces[0][i][0]), int(self.faces[0][i][1]), int(self.faces[0][i][2]))
        for i in range(3):
            print(int(self.faces[2][i][0]), int(self.faces[2][i][1]), int(self.faces[2][i][2]), end=" ")
            print(int(self.faces[4][i][0]), int(self.faces[4][i][1]), int(self.faces[4][i][2]), end=" ")
            print(int(self.faces[3][i][0]), int(self.faces[3][i][1]), int(self.faces[3][i][2]), end=" ")
            print(int(self.faces[5][i][0]), int(self.faces[5][i][1]), int(self.faces[5][i][2]))
        for i in range(3):
            print("     ", int(self.faces[1][i][0]), int(self.faces[1][i][1]), int(self.faces[1][i][2]))
        print()


cube = RubikCube()
cube.toString()
cube.randomGenerate()
cube.toString()
