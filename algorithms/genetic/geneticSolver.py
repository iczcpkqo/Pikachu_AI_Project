import time
import random
import operator
from RubikCube import RubikCube

population_size = 500
max_generations = 300
max_resets = 10
elitism_num = 50

def solve(scramble):
    start_time = time.time()

    for r in range(0, max_resets):
        # initialize population
        cubes = []
        for i in range(0, population_size):
            cube = RubikCube()
            cube.execute(scramble)
            # randomize it
            cube.execute(cube.random_single_move())
            cube.execute(cube.random_single_move())
            cubes.append(cube)

        # evolve population
        for g in range(0, max_generations):
            # sort by fitness
            cubes.sort(key=operator.attrgetter('fitnessValue'))

            print(f"World: {r + 1} - Generation: {g}")
            print(f"Best solution so far")
            print(f"{cubes[0].get_algorithm_string()}")
            print("")

            # the goal is to minimize the fitness function
            # 0 means that the cube is solved
            for i in range(0, len(cubes)):
                if cubes[i].fitness == 0:
                    print("Solution found")
                    print(f"World: {r + 1} - Generation: {g + 1}")
                    print(f"Scramble: {cubes[i].get_algorithm_string()}")
                    print(f"Solution")
                    print(f"{cubes[i].get_algorithm_string()}")
                    print(f"Moves: {len(cubes[i].get_algorithm())}")
                    print(f"{time.time() - start_time} seconds")
                    print("")
                    return

                # elitism: the best performers move to the next generation without changes
                if i > elitism_num:
                    # copy a random top performer cube
                    cube.copy(cubes[i], cubes[random.randint(0, elitism_num)])
                    evolution_type = random.randint(0, 5)

                    if evolution_type == 0:
                        cubes[i].execute(cube.random_permutation())
                    elif evolution_type == 1:
                        cubes[i].execute(cube.random_permutation())
                        cubes[i].execute(cube.random_permutation())
                    elif evolution_type == 2:
                        cubes[i].execute(cube.random_full_rotation())
                        cubes[i].execute(cube.random_permutation())
                    elif evolution_type == 3:
                        cubes[i].execute(cube.random_orientation())
                        cubes[i].execute(cube.random_permutation())
                    elif evolution_type == 4:
                        cubes[i].execute(cube.random_full_rotation())
                        cubes[i].execute(cube.random_orientation())
                        cubes[i].execute(cube.random_permutation())
                    elif evolution_type == 5:
                        cubes[i].execute(cube.random_orientation())
                        cubes[i].execute(cube.random_full_rotation())
                        cubes[i].execute(cube.random_permutation())

    # if a solution was found we returned
    print("")
    print(f"Solution not found")
    print(f"{time.time() - start_time} seconds")


scramble_str = "F2"
# scramble_str = "D' B2 D2 L2 U' L L2 D U' L' R' L D' B2 R2 B' R F U2 R B2 F' L' B2 L2 D' B2 D2 R' R' F L2 R2 U' L2 B' F2 D2 U L' R F2 L' B2 L2 R2 B F L D' U L R' D' U L' R2 U F' L' U2 B' F L B' F2 D' U B2 R' U B' F U F' R' U2 L' R' D F2 R' F' D2 L' R2 B' D L U2"
scramble = scramble_str.split(" ")

solve(scramble)