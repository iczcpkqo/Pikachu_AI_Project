import random
# import Rubik
import RubikCube
import math
import copy
import matplotlib.pyplot as plt

ROTATIONS = ["x", "x'", "x2", "y", "y'", "y2"]

ROTATIONS_Z = ["z", "z'", "z2"]

PERMUTATIONS = [
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


class SimulatedAnnealing:
    def __init__(self, temperature=1, alpha=0.999, temperatureLimit=0.0000000001, maxGeneration=30000):
        self.temperature = temperature
        self.alpha = alpha
        self.temperatureLimit = temperatureLimit
        self.currentGeneration = 1
        self.currentSolution = None
        self.maxGeneration = maxGeneration
        self.progressFitness = []

    def make_random_permutation(self):
        r = random.randint(0, len(PERMUTATIONS) - 1)
        return PERMUTATIONS[r]

    def make_random_full_rotation(self):
        r = random.randint(0, len(ROTATIONS) - 1)
        return [ROTATIONS[r]]

    def make_random_rotation_z(self):
        r = random.randint(0, len(ROTATIONS_Z) - 1)
        return [ROTATIONS_Z[r]]


    def accepting_probability(self, candidateFitness):
        return math.exp(-abs(candidateFitness - self.currentSolution.fitness()) / self.temperature)


    def accept(self, candidate):
        candidateFitness = candidate.fitness()

        if candidateFitness < self.currentSolution.fitness():
            self.currentSolution = candidate
            
        else:
            if random.random() < self.accepting_probability(candidateFitness):
                self.currentSolution = candidate


    def plot_progress(self):
        plt.plot([i for i in range(len(self.progressFitness))], self.progressFitness)
        plt.ylabel("Fitness")
        plt.xlabel("Generation")
        plt.show()

    def simulated_annealing(self, rubik, initalState):

        # rubik.execute(initalState)
        self.currentSolution = rubik

        while(self.temperature >= self.temperatureLimit and self.currentGeneration <= self.maxGeneration):
            candidate = copy.deepcopy(self.currentSolution)
            candidate.toString(candidate.getStartState())

            permuteRandom = random.randint(0, 5)

            if permuteRandom == 0:
                candidate.execute(self.make_random_permutation())

            elif permuteRandom == 1:
                candidate.execute(self.make_random_permutation())
                candidate.execute(self.make_random_permutation())

            elif permuteRandom == 2:
                candidate.execute(self.make_random_full_rotation())
                candidate.execute(self.make_random_permutation())

            elif permuteRandom == 3:
                candidate.execute(self.make_random_rotation_z())
                candidate.execute(self.make_random_permutation())

            elif permuteRandom == 4:
                candidate.execute(self.make_random_full_rotation())
                candidate.execute(self.make_random_rotation_z())
                candidate.execute(self.make_random_permutation())

            elif permuteRandom == 5:
                candidate.execute(self.make_random_rotation_z())
                candidate.execute(self.make_random_full_rotation())
                candidate.execute(self.make_random_permutation())

            self.accept(candidate)

            self.temperature *= self.alpha
            self.currentGeneration += 1

            self.progressFitness.append(self.currentSolution.fitnessValue)

            print("Generation:", self.currentGeneration, ": Number of mismatched tiles:", self.currentSolution.fitnessValue)

            if(self.currentSolution.fitness() == 0):
                print("Solution found. The output is dumped to output.txt file")

                outputFile = open("output.txt", "w")
                outputFile.write(self.currentSolution.get_algorithm_string())
                outputFile.close()

                self.plot_progress()
                return

        print(self.currentSolution.fitnessValue)
        print("Cannot find solution.")




# scrambleInput = input("Enter the scramble string input: ")
# scramble = scrambleInput.split(" ")
rubik = RubikCube.RubikCube()
simulatedAnnealing = SimulatedAnnealing()
simulatedAnnealing.simulated_annealing(rubik, rubik.getStartState())

