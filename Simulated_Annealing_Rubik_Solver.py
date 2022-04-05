import random
# import Rubik
import RubikCube
import math
import copy
import matplotlib.pyplot as plt


class SimulatedAnnealing:

    def __init__(self, temperature=1, alpha=0.99, temperatureLimit=0.000000001, maxGeneration=10000):
        self.temperature = temperature
        self.alpha = 0.99 * alpha  # Accelerated convergence
        self.temperatureLimit = temperatureLimit
        self.currentGeneration = 1
        self.currentSolution = None
        self.maxGeneration = maxGeneration
        self.solutions = []


    def make_random_permutation(self):
        r = random.randint(0, len(rubik.PERMUTATIONS) - 1)
        return rubik.PERMUTATIONS[r]

    def make_random_full_rotation(self):
        r = random.randint(0, len(rubik.ROTATIONS) - 1)
        return [rubik.ROTATIONS[r]]

    def make_random_rotation_z(self):
        r = random.randint(0, len(rubik.ROTATIONS_Z) - 1)
        return [rubik.ROTATIONS_Z[r]]


    def accept(self, candidate):  # Metropolis
        candidateFitness = candidate.fitness()

        if candidateFitness < self.currentSolution.fitness():
            self.currentSolution = candidate
            
        else:
            accepting_probability = math.exp(-abs(candidateFitness - self.currentSolution.fitness()) / self.temperature)
            if random.random() < accepting_probability:
                self.currentSolution = candidate


    def plot_progress(self):

        solution_set = range(len(self.solutions))
        plt.plot(solution_set, self.solutions)
        plt.ylabel("Number of mismatched tiles")
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

            self.solutions.append(self.currentSolution.fitnessValue)



            print("Generation:", self.currentGeneration, "- Number of mismatched tiles:", self.currentSolution.fitnessValue)



            if(self.currentSolution.fitness() == 0):
                print("Solution found. The output is dumped to SA_solution.txt file")

                outputFile = open("SA_solution.txt", "w")
                outputFile.write("Rubik_Test:")
                outputFile.write(self.currentSolution.get_algorithm_string())
                outputFile.close()

                self.plot_progress()
                return

        self.plot_progress()
        print(self.currentSolution.fitnessValue)
        print("Cannot find solution.")



# scrambleInput = input("Enter the scramble string input: ")
# scramble = scrambleInput.split(" ")
rubik = RubikCube.RubikCube()
simulatedAnnealing = SimulatedAnnealing()
simulatedAnnealing.simulated_annealing(rubik, rubik.getStartState())
