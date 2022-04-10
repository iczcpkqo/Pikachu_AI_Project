# CS7IS2 Project - A-star

## Introduction

## Related work

### Search algorithms

A search algorithm is a method of solving a problem by purposefully exhausting all possible scenarios for the problem.
There are three search algorithms considered, BFS, DFS, and A-star. The final choice is A-star.

* BFS Algorithm
A breadth-first search algorithm restores the cube by traversing all possible scenarios when the cube has been unscrewed a small number of times. However, as the number of moves increases, the number of calculations increases exponentially, making it difficult to restore.

* The DFS algorithm
  The depth-first search algorithm will always prefer a certain state for the next iteration, but the tesseract can be searched continuously along with a certain state and has almost no endpoint, so if the end state of the tesseract is not on the path of the starting state, the tesseract problem will not be solved.

* A-star algorithm
  A-star differs from BFS and DFS in two ways. The first is that it calculates the total cost of node selection from the heuristic function and the cost of each step, thus generating a priority. The second is that each search selects the node with the lowest cost. Since each selection is made closer to the endpoint, nodes that would be searched in BFS and DFS with high cost are not searched in A-star, and therefore A-star has less search volume for the same search result. Therefore, A-star is more suitable for solving the Rubik's Cube problem than BFS and DFS.

## Definition of the problem and algorithm

The A-star algorithm is a search algorithm that requires knowledge of the starting state and the ability to estimate the distance between each step and the final state. The shortest path is obtained step by step.
The main features of the A-star algorithm compared to other algorithms are:

1. Heuristic function. The result of the heuristic function is used to estimate the distance between the current state and the target state, i.e., $f(n)=g(n)+h(n)$.
2. State recording. Each iteration stores a list of states that can be used for the iteration and a list of states that have been processed. 
3. Select the optimal. At each iteration, an optimal next step is chosen from the list of states available for iteration to continue the procedure, and the nodes in the list of processed states are not computed again.

## Experimental results

### Method

The performance of the A-star search algorithm is evaluated by the solution time.
Since the A-star algorithm solves for the shortest path, the test result will always be less than or equal to the number of times the cube was initially twisted, and the search effect directly influences the reduction effect, so the time taken to reduce is chosen as the evaluation criterion.

### Results

The cube can be restored if the initial state of the cube has been twisted less than or equal to 7 times.

![AVG_7 mix_level = 7, limit_times = 0.7, base = 1.041, cost_price = 1.28, cost_weight = 1.0](../../../../../../../sync/dropbox/im/notes/data/resource/image/AVG_7%20mix_level%20=%207,%20limit_times%20=%200.7,%20base%20=%201.041,%20cost_price%20=%201.28,%20cost_weight%20=%201.0.png)

### Discussion

The A-star algorithm solves the Rubik's Cube problem by selecting the node with the lowest current arrival cost and calculating 21 different next states and calculating the arrival cost of the next state, which is determined by adding up the cost of each step and the heuristic function. 

The advantage of A-star is that it will find the least reduction method. In contrast to the Q-leaning algorithm, A-star does not calculate all states before reaching the destination at the beginning but rather starts the next search by continuously finding the nodes that are most necessary for the search.

The disadvantage is that as the number of times the cube is initially twisted increases, the time required to restore it increases more quickly, so it is not as fast as the genetic algorithm when solving more complex cases.
In contrast to genetic algorithms, the cost of each step of the A-star calculation is greatly influenced by the heuristic function, **which can seriously affect the selection of nodes when the distance between the current position and the target position cannot be effectively estimated, thus seriously affecting the search results.** For example, in the problem of restoring a Rubik's cube, the 21 different states can be interpreted as a point in a two-dimensional plane, which can move in 21 different directions in the next step, but once it moves four steps in any direction, it returns to the origin, which is very different from the motion of a point in a typical Cartesian coordinate system, and therefore cannot be evaluated by If the heuristic function is evaluated by the number of small squares in the correct position, this is valid when the number of initial moves is small, but as the number of moves increases, the confusion of the imitation stabilises, but the difficulty of restoration continues to increase, and the heuristic function cannot be evaluated accurately, which is a weakness of A-star. 

## Conclusion

It has been observed experimentally that the A-star algorithm can solve the Rubik's Cube problem if the level of confusion is not too high. The reason for not being able to restore the cube after the level of confusion has stabilised is that the heuristic function uses the correct rate at which the cube is restored, and when the level of confusion has stabilised, the heuristic function does not correctly evaluate the correct rate, regardless of the direction of the cube's next state.
A possible improvement would be to modify the way in which the degree of confusion is evaluated, for example, by making the correctness rate the sum of the distances of each piece from its starting position.



































