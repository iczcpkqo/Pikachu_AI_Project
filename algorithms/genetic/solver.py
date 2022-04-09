import time
import random
import operator
import copy as cp
from RubikCube import RubikCube

round = 10
population = 1000
generations = 500
heritability = 0.05
genetics = population * heritability

rubik = RubikCube()

def createPopulation(scramble):
    cube = RubikCube()
    cube.execute2(scramble)
    cube.execute2(cube.random_single_move())
    cube.execute2(cube.random_single_move())
    return cube

def explore(cubes,i):
    new_cube = cubes[random.randint(0, genetics)]
    cubes[i].faces = cp.deepcopy(new_cube.faces)
    cubes[i].moveHistory = cp.deepcopy(new_cube.moveHistory)
    cubes[i].fitnessValue = cp.deepcopy(new_cube.fitnessValue)
    movement = random.randint(0, 5)

    match movement:
        case 0:
            cubes[i].execute2(rubik.random_permutation())
        case 1:
            cubes[i].execute2(rubik.random_permutation())
            cubes[i].execute2(rubik.random_permutation())
        case 2:
            cubes[i].execute2(rubik.random_full_rotation())
            cubes[i].execute2(rubik.random_permutation())
        case 3:
            cubes[i].execute2(rubik.random_orientation())
            cubes[i].execute2(rubik.random_permutation())
        case 4:
            cubes[i].execute2(rubik.random_full_rotation())
            cubes[i].execute2(rubik.random_orientation())
            cubes[i].execute2(rubik.random_permutation())
        case 5:
            cubes[i].execute2(rubik.random_orientation())
            cubes[i].execute2(rubik.random_full_rotation())
            cubes[i].execute2(rubik.random_permutation())

def solver(scramble):
    start = time.time()

    for r in range(0, round):

        cubes = []
        for i in range(0, population):
            cubes.append(createPopulation(scramble))

        for g in range(0, generations):
            cubes.sort(key=operator.attrgetter('fitnessValue'))
            print("round:" + str(r) + ", generation:" + str(g))

            for i in range(0, len(cubes)):
                if cubes[i].fitnessValue == 0:
                    print("find a solution, Scramble: " + str(scramble))
                    print("Solution:" + cubes[0].get_algorithm_string() + ",steps:" + str(len(cubes[i].get_algorithm())))
                    print("total time:" + str(time.time() - start) + " seconds")
                    return

                if i > genetics:
                    explore(cubes,i)

    print("no solution")


scramble_str = "B' R' U2 B' F D2 R2 B F' L2 R' B2 D2 L2 F' U L B2 D F L' F R B2 D' U' B' L' B' F2"
# scramble_str = "L U"
# scramble_str = "D' B2 D2 L2 U' L L2 D U' L' R' L D' B2 R2 B' R F U2 R B2 F' L' B2 L2 D' B2 D2 R' R' F L2 R2 U' L2 B' F2 D2 U L' R F2 L' B2 L2 R2 B F L D' U L R' D' U L' R2 U F' L' U2 B' F L B' F2 D' U B2 R' U B' F U F' R' U2 L' R' D F2 R' F' D2 L' R2 B' D L U2"
scramble = scramble_str.split(" ")
solver(scramble)
