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

    def accept(self, candidate):  # Metropolis
        candidateFitness = candidate.fitnessSA()

        if candidateFitness < self.currentSolution.fitnessSA():
            self.currentSolution = candidate
            
        else:
            accepting_probability = math.exp(-abs(candidateFitness - self.currentSolution.fitnessSA()) / self.temperature)
            if random.random() < accepting_probability:
                self.currentSolution = candidate


    def plot_progress(self):

        solution_set = range(len(self.solutions))
        plt.plot(solution_set, self.solutions)
        plt.ylabel("Number of mismatched tiles")
        plt.xlabel("Generation")

        plt.show()

    def simulated_annealing(self, rubik, initalState):

        # rubik.executeSA(initalState)
        self.currentSolution = rubik

        while(self.temperature >= self.temperatureLimit and self.currentGeneration <= self.maxGeneration):
            candidate = copy.deepcopy(self.currentSolution)
            candidate.toString(candidate.getStartState())

            permuteRandom = random.randint(0, 5)

            if permuteRandom == 0:
                candidate.executeSA(rubik.random_permutation())

            elif permuteRandom == 1:
                candidate.executeSA(rubik.random_permutation())
                candidate.executeSA(rubik.random_permutation())

            elif permuteRandom == 2:
                candidate.executeSA(rubik.random_full_rotation())
                candidate.executeSA(rubik.random_permutation())

            elif permuteRandom == 3:
                candidate.executeSA(rubik.random_orientation())
                candidate.executeSA(rubik.random_permutation())

            elif permuteRandom == 4:
                candidate.executeSA(rubik.random_full_rotation())
                candidate.executeSA(rubik.random_orientation())
                candidate.executeSA(rubik.random_permutation())

            elif permuteRandom == 5:
                candidate.executeSA(rubik.random_orientation())
                candidate.executeSA(rubik.random_full_rotation())
                candidate.executeSA(rubik.random_permutation())

            self.accept(candidate)
            self.temperature *= self.alpha
            self.currentGeneration += 1

            self.solutions.append(self.currentSolution.fitnessValue)



            print("Generation:", self.currentGeneration, "- Number of mismatched tiles:", self.currentSolution.fitnessValue)



            if(self.currentSolution.fitnessSA() == 0):
                rubik.toString(rubik.state)
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

