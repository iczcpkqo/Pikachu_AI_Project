import time
import random
import operator
import copy as cp
from RubikCube import RubikCube

round = 10
population = 1000
generations = 500
mutation_probability = 0.8
heritability = 0.05
genetics = population * heritability

rubik = RubikCube()

# scramble_str = "L U"
# scramble_str = "D' B2 D2 L2 U' L L2 D U' L' R' L D' B2 R2 B' R F U2 R B2 F' L' B2 L2 D' B2 D2 R' R' F L2 R2 U' L2 B' F2 D2 U L' R F2 L' B2 L2 R2 B F L D' U L R' D' U L' R2 U F' L' U2 B' F L B' F2 D' U B2 R' U B' F U F' R' U2 L' R' D F2 R' F' D2 L' R2 B' D L U2"
scramble_str = "B' R' U2 B' F D2 R2 B F' L2 R' B2 D2 L2 F' U L B2 D F L' F R B2 D' U' B' L' B' F2"
# scramble_str = "B' R' U2 B'"
scramble = scramble_str.split(" ")
f = open('genetic_output' + str(len(scramble)) + 'scramble.txt', 'w')
f.write("round=" + str(round) + '\n')
f.write("population=" + str(population) + '\n')
f.write("generations=" + str(generations) + '\n')
f.write("mutation_probability=" + str(mutation_probability) + '\n')
f.write("heritability=" + str(heritability) + '\n')
f.write("genetics=" + str(genetics) + '\n')


def createPopulation(scramble):
    cube = RubikCube()
    cube.execute(scramble)
    cube.execute(cube.random_single_move())
    cube.execute(cube.random_single_move())
    return cube


def explore(cubes, i):
    new_cube = cubes[random.randint(0, genetics)]
    cubes[i].state = cp.deepcopy(new_cube.state)
    cubes[i].moveHistory = cp.deepcopy(new_cube.moveHistory)
    cubes[i].fitnessValue = cp.deepcopy(new_cube.fitnessValue)
    movement = random.randint(0, 6)

    if movement == 0:
        cubes[i].execute(rubik.random_permutation())

    elif movement == 1:
        cubes[i].execute(rubik.random_permutation())
        cubes[i].execute(rubik.random_permutation())

    elif movement == 2:
        cubes[i].execute(rubik.random_full_rotation())
        cubes[i].execute(rubik.random_permutation())

    elif movement == 3:
        cubes[i].execute(rubik.random_orientation())
        cubes[i].execute(rubik.random_permutation())

    elif movement == 4:
        cubes[i].execute(rubik.random_full_rotation())
        cubes[i].execute(rubik.random_orientation())
        cubes[i].execute(rubik.random_permutation())

    elif movement == 5:
        cubes[i].execute(rubik.random_orientation())
        cubes[i].execute(rubik.random_full_rotation())
        cubes[i].execute(rubik.random_permutation())


def solver(scramble):
    start = time.time()

    for r in range(0, round):

        cubes = []
        for i in range(0, population):
            cubes.append(createPopulation(scramble))

        for g in range(0, generations):
            cubes.sort(key=operator.attrgetter('fitnessValue'))
            f.write(cubes[0].getFaces() + '\n')
            print(cubes[0].getFaces())
            f.write("round:" + str(r) + ", generation:" + str(g) + '\n')
            print("round:" + str(r) + ", generation:" + str(g))

            for i in range(0, len(cubes)):
                if cubes[i].fitnessValue == 0:
                    f.write("find a solution, Scramble: " + str(scramble) + '\n')
                    print("find a solution, Scramble: " + str(scramble))
                    f.write("Solution:" + cubes[0].get_algorithm_string() + ",steps:" + str(
                        len(cubes[i].get_algorithm())) + '\n')
                    print(
                        "Solution:" + cubes[0].get_algorithm_string() + ",steps:" + str(len(cubes[i].get_algorithm())))
                    f.write("total time:" + str(time.time() - start) + " seconds" + '\n')
                    print("total time:" + str(time.time() - start) + " seconds")
                    return

                if i > genetics and random.random() < mutation_probability:
                    explore(cubes, i)

    f.write("no solution" + '\n')
    print("no solution")


solver(scramble)