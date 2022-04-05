

import sys

import CubeActions

sys.path.append("lib/cube-solver/twophase")

import random
import numpy as np

import RubikCube

from twophase import solve

minScrambleLen = 1
maxScrambleLen = 25

fileExt = ".npy"

actions = [CubeActions.B, CubeActions.D, CubeActions.F,
                   CubeActions.L, CubeActions.R, CubeActions.U,
                   CubeActions._B, CubeActions._D, CubeActions._F,
                   CubeActions._L, CubeActions._R, CubeActions._U,
                   CubeActions.B2, CubeActions.D2, CubeActions.F2,
                   CubeActions.L2, CubeActions.R2, CubeActions.U2,
                   CubeActions.E, CubeActions.S, CubeActions.M,
                   CubeActions._E, CubeActions._S, CubeActions._M,
                   CubeActions.E2, CubeActions.S2, CubeActions.M2,]


stickerToFace = {
    0: "D",
    1: "U",
    2: "F",
    3: "B",
    4: "L",
    5: "R"
}


def generateData(m, numFiles=1, filePathBase="d:/traing_data/"):
    for i in range(numFiles):
        print("Dataset for file #" + str(i) + " is generating.")
        data = getRandomScrambles(int(m / numFiles))
        np.save(filePathBase + str(i) + fileExt, data)
        print("Dataset for file #" + str(i) + " is saved.")


# Returns a list of random sticker and solution pairs
def getRandomScrambles(iterations):
    res = np.zeros((0, 55))  # 54 stickers + 1 solution move
    while res.shape[0] < iterations:
        print("Training examples generated: " +
              str(res.shape[0]) + "/" + str(iterations), end="\r")
        res = np.concatenate((res, randomScrambles()), axis=0)

    return res[:iterations]


# Generates a random scramble and last move pairs from one solve() call
def randomScrambles():

    cube = RubikCube()
    cube = _randomlyScrambleCube(cube)

    # Attempt to get solution
    try:
        solution = solve(_toStickerString(cube.stickers))
    # Get another scramble if solution cannot be found
    except RuntimeError:
        print("Solution not found. Attempting another scramble.")
        return randomScrambles()

    return _getDataFromSolution(cube, solution)



# Returns all training data corresponding to solution.
# Each move in solution has respective flattened sticker layout
# res.shape = (len(solution), 55)
def _getDataFromSolution(cube, solution):
    moves = solution.split()
    res = np.zeros((len(moves), 55))

    for i in range(len(moves)):
        row = cube.stickers.flatten()
        row = np.append(row, [turns.index(moves[i])], axis=0)
        res[i] = row

        cube(moves[i])

    return res


# Randomly scramble cube in range [minScrambleLen, maxScrambleLen], and until not solved
def _randomlyScrambleCube(cube):
    for _ in range(random.randint(minScrambleLen, maxScrambleLen)):
        index = random.randint(0, len(turns) - 1)
        cube(turns[index])

    # Make sure cube isn't solved
    while cube.isSolved():
        index = random.randint(0, len(turns) - 1)
        cube(turns[index])

    return cube

# Converts a 6x3x3 sticker tensor into a 54 character string
# Then passed into twophase.solve() using Kociemba optimal cube solving algorithm
# Credit: tcbegley on GitHub: https://github.com/tcbegley/cube-solver


def _toStickerString(stickers):

    # Shifts 6x3x3 tensor from default representation to twophase representation
    #   (note that twophasel.solve() requires different sticker order)
    # I.e.  1            0
    #     4 2 5 3  =>  4 2 1 5
    #       0            3
    def toTwoPhase(stickers):
        return stickers[[1, 5, 2, 0, 4, 3], :, :]

    # Converts index of sticker to face character
    def indexToFace(index):
        return stickerToFace[index]

    stickerList = toTwoPhase(stickers).flatten()
    stickerList = map(indexToFace, stickerList)
    return "".join(stickerList)



if __name__ == "__main__":
    generateData(5400, numFiles=1)
