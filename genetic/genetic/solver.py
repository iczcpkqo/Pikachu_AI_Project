import time
import random
import operator
import copy as cp

from matplotlib import pyplot as plt

from RubikCube import RubikCube

population = 1000
generations = 2000
mutation_probability = 0.8
heritability = 0.05
genetics = population * heritability

rubik = RubikCube()


# scramble_str = "L U"
# scramble_str = "B' R' U2 B'"
# scramble_str = "B' R' U2 B' F D2 R2 B F' L2 R' B2 D2 L2 F' U L B2 D F L' F R B2 D' U' B' L' B' F2"
# scramble_str = "D' B2 D2 L2 U' L L2 D U' L' R' L D' B2 R2 B' R F U2 R B2 F' L' B2 L2 D' B2 D2 R' R' F L2 R2 U' L2 B' F2 D2 U L' R F2 L' B2 L2 R2 B F L D' U L R' D' U L' R2 U F' L' U2 B' F L B' F2 D' U B2 R' U B' F U F' R' U2 L' R' D F2 R' F' D2 L' R2 B' D L U2"

def printParameters(scramble):
    f = open('genetic_output_' + str(len(scramble)) + '_scramble.txt', 'w')
    f.write("round=" + str(round) + '\n')
    f.write("population=" + str(population) + '\n')
    f.write("generations=" + str(generations) + '\n')
    f.write("mutation_probability=" + str(mutation_probability) + '\n')
    f.write("heritability=" + str(heritability) + '\n')
    f.write("genetics=" + str(genetics) + '\n')
    return f


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
    movement = random.randint(0, 5)

    match movement:
        case 0:
            cubes[i].execute(rubik.random_permutation())
        case 1:
            cubes[i].execute(rubik.random_permutation())
            cubes[i].execute(rubik.random_permutation())
        case 2:
            cubes[i].execute(rubik.random_full_rotation())
            cubes[i].execute(rubik.random_permutation())
        case 3:
            cubes[i].execute(rubik.random_orientation())
            cubes[i].execute(rubik.random_permutation())
        case 4:
            cubes[i].execute(rubik.random_full_rotation())
            cubes[i].execute(rubik.random_orientation())
            cubes[i].execute(rubik.random_permutation())
        case 5:
            cubes[i].execute(rubik.random_orientation())
            cubes[i].execute(rubik.random_full_rotation())
            cubes[i].execute(rubik.random_permutation())


def solver(scramble, f):
    start = time.time()

    cubes = []
    for i in range(0, population):
        cubes.append(createPopulation(scramble))

    for g in range(0, generations):
        cubes.sort(key=operator.attrgetter('fitnessValue'),reverse=False)
        # f.write(cubes[0].getFaces() + '\n')
        # print(cubes[0].getFaces())
        # cubes[0].toString() + '\n'
        cubes[0].toString(cubes[0].state)
        print(cubes[0].fitnessValue)
        # f.write("generation:" + str(g) + '\n')
        # print("generation:" + str(g))

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
                return True, time.time() - start, len(cubes[i].get_algorithm())

            if i > genetics and random.random() < mutation_probability:
                explore(cubes, i)

    f.write("no solution" + '\n')
    print("no solution")
    return False, time.time() - start, 0


# scramble = rubik.randomScrambler(9)
# f = printParameters(scramble)
# solver(scramble, f)
running_times = 10
interval = 10
max_time = 100

ii = []
rr = []
tt = []
ss = []

i = 10
while i < max_time:
    scramble = rubik.randomScrambler(i)
    f = printParameters(scramble)
    successes = 0.0
    total_time = 0.0
    total_steps = 0.0
    for j in range(running_times):
        solved, ctime, steps = solver(scramble, f)
        if solved:
            successes = successes + 1
            total_time = total_time + ctime
            total_steps = total_steps + steps

    ii.append(i)
    rr.append(successes / running_times)
    tt.append(total_time / successes)
    ss.append(total_steps / successes)

    i = i + interval

plt.figure(figsize=(7, 7))
plt.plot(ii, rr, color='b', label='Restoration success rate per scramble')
plt.xlabel('Number of scramble')
plt.ylabel('Success rate')
plt.legend()
plt.show()

plt.figure(figsize=(7, 7))
plt.plot(ii, ss, color='b', label='The number of steps required for each scramble to restore')
plt.xlabel('Number of scramble')
plt.ylabel('Average finding solution steps')
plt.legend()
plt.show()

plt.figure(figsize=(7, 7))
plt.plot(ii, tt, color='b', label='The total of time required for each scramble to restore')
plt.xlabel('Number of scramble')
plt.ylabel('Average finding solution time')
plt.legend()
plt.show()
