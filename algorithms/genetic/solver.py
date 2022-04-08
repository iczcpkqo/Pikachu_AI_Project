import time
import random
import operator
import copy as cp
from RubikCube import RubikCube

population = 1000
generations = 300
round = 10
heritability = 0.05
genetics = population * heritability


def solve(scramble):
    start_time = time.time()

    for r in range(0, round):

        cubes = []
        for i in range(0, population):
            cube = RubikCube()
            cube.execute2(scramble)
            cube.execute2(cube.random_single_move())
            cube.execute2(cube.random_single_move())
            cubes.append(cube)

        # evolve population
        for g in range(0, generations):
            # sort by fitness
            cubes.sort(key=operator.attrgetter('fitnessValue'))

            if g % 20 == 0 and g != 0:
                print(f"World: {r + 1} - Generation: {g}")
                print(f"Best solution so far")
                print(f"{cubes[0].get_algorithm_string()}")
                print("")

            # the goal is to minimize the fitness function
            # 0 means that the cube is solved
            for i in range(0, len(cubes)):
                if cubes[i].fitnessValue == 0:
                    print("Solution found")
                    print(f"World: {r + 1} - Generation: {g + 1}")
                    print(f"Scramble: {cubes[0].get_algorithm_string()}")
                    print(f"Solution")
                    print(f"{cubes[0].get_algorithm_string()}")
                    print(f"Moves: {len(cubes[i].get_algorithm())}")
                    print(f"{time.time() - start_time} seconds")
                    print("")
                    return

                if i > genetics:
                    new_cube = cubes[random.randint(0, genetics)]
                    cubes[i].faces = cp.deepcopy(new_cube.faces)
                    cubes[i].moveHistory = cp.deepcopy(new_cube.moveHistory)
                    cubes[i].fitnessValue = cp.deepcopy(new_cube.fitnessValue)
                    evolution_type = random.randint(0, 5)

                    if evolution_type == 0:
                        cubes[i].execute2(cube.random_permutation())
                    elif evolution_type == 1:
                        cubes[i].execute2(cube.random_permutation())
                        cubes[i].execute2(cube.random_permutation())
                    elif evolution_type == 2:
                        cubes[i].execute2(cube.random_full_rotation())
                        cubes[i].execute2(cube.random_permutation())
                    elif evolution_type == 3:
                        cubes[i].execute2(cube.random_orientation())
                        cubes[i].execute2(cube.random_permutation())
                    elif evolution_type == 4:
                        cubes[i].execute2(cube.random_full_rotation())
                        cubes[i].execute2(cube.random_orientation())
                        cubes[i].execute2(cube.random_permutation())
                    elif evolution_type == 5:
                        cubes[i].execute2(cube.random_orientation())
                        cubes[i].execute2(cube.random_full_rotation())
                        cubes[i].execute2(cube.random_permutation())

    # if a solution was found we returned
    print("")
    print(f"Solution not found")
    print(f"{time.time() - start_time} seconds")

# scramble_str = "B' R' U2 B' F D2 R2 B F' L2 R' B2 D2 L2 F' U L B2 D F L' F R B2 D' U' B' L' B' F2"
scramble_str = "L U"
# scramble_str = "D' B2 D2 L2 U' L L2 D U' L' R' L D' B2 R2 B' R F U2 R B2 F' L' B2 L2 D' B2 D2 R' R' F L2 R2 U' L2 B' F2 D2 U L' R F2 L' B2 L2 R2 B F L D' U L R' D' U L' R2 U F' L' U2 B' F L B' F2 D' U B2 R' U B' F U F' R' U2 L' R' D F2 R' F' D2 L' R2 B' D L U2"
scramble = scramble_str.split(" ")
solve(scramble)
