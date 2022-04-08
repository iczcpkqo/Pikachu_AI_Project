import copy as cp
import CubeActions
import numpy as np
import matplotlib.pyplot as plt
import random
import util
import time
import os

class RubikCube():
    def __init__(self, **arg):
        self.arg = {"mix_level":5,
               "base":1.0001,
               "limit_times":0.6,
               "cost_price": 1,
               "cost_weight": 1,
               "start_actions": False,
               **arg}
        self.__moves_lookup = {
            "D": CubeActions.D, "D'": CubeActions._D, "D2": CubeActions.D2,
            "E": CubeActions.E, "E'": CubeActions._E, "E2": CubeActions.E2,
            "U": CubeActions.U, "U'": CubeActions._U, "U2": CubeActions.U2,

            "L": CubeActions.L, "L'": CubeActions._L, "L2": CubeActions.L2,
            "R": CubeActions.R, "R'": CubeActions._R, "R2": CubeActions.R2,
            "M": CubeActions.M, "M'": CubeActions._M, "M2": CubeActions.M2,

            "B": CubeActions.B, "B'": CubeActions._B, "B2": CubeActions.B2,
            "F": CubeActions.F, "F'": CubeActions._F, "F2": CubeActions.F2,
            "S": CubeActions.S, "S'": CubeActions._S, "S2": CubeActions.S2,

            "x": CubeActions.X, "x'": CubeActions._X, "x2": CubeActions.X2,
            "y": CubeActions.Y, "y'": CubeActions._Y, "y2": CubeActions.Y2,
            "z": CubeActions.Z, "z'": CubeActions._Z, "z2": CubeActions.Z2,
        }
        self.__next_actions = ["D", "D'", "D2",
                               "E", "E'", "E2",
                               "U", "U'", "U2",

                               "L", "L'", "L2",
                               "R", "R'", "R2",
                               "M", "M'", "M2",

                               "B", "B'", "B2",
                               "F", "F'", "F2",
                               "S", "S'", "S2"]

        # self.test_cube = [[[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]],
        #                   [[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]],
        #                   [[2., 2., 2.], [2., 2., 2.], [2., 2., 2.]], array([[3., 3., 3.], [3., 3., 3.],
        #                                                                                               [3., 3., 3.]]),
        #                   array([[4., 4., 4.],
        #                          [4., 4., 4.],
        #                          [4., 4., 4.]]), array([[5., 5., 5.],
        #                                                 [5., 5., 5.],
        #                                                 [5., 5., 5.]])]

        self.__last_random_actions = []
        self.__move_history = []
        self.__fitness_value = 0

        # 创建六个面，放在faces列表里，顺序为上（0），下（1），左（2），右（3），前（4），后（5）
        self.__target_state = [np.zeros((3, 3))]
        for i in range(1, 6):
            self.__target_state.append(np.ones((3, 3)) + self.__target_state[i - 1])

        self.__mixed_level = self.arg["mix_level"]
        self.arg["start_actions"] = self.arg["start_actions"] or self.random_action(self.__mixed_level)

        self.__start_actions = self.arg["start_actions"]
        self.__base = self.arg["base"]
        self.__limit_times = self.arg["limit_times"]
        self.__cost_price = self.arg["cost_price"]
        self.__cost_weight = self.arg["cost_weight"]

        self.__start_state = self.move(self.__start_actions, self.__target_state)
        self.__current_state = cp.deepcopy(self.__start_state)

        self.restore_cost = 0
        self.restore_path = []
        self.restore_heuristic = 0
        self.restore_fringe_size = 0
        self.restore_closed_size = 0

    def set_mixed_level(self, level):
        self.__mixed_level = level
        self.__start_actions = self.random_action(self.__mixed_level)
        self.__start_state = self.move(self.__start_actions, self.__target_state)
        self.__current_state = cp.deepcopy(self.__start_state)

    def get_limit_times(self):
        return self.__limit_times

    def get_base(self):
        return self.__base

    def get_cost_price(self):
        return self.__cost_price

    def get_cost_weight(self):
        return self.__cost_weight

    def get_start_actions(self):
        return self.__start_actions

    def get_start_state(self):
        return self.__start_state

    def get_target_state(self):
        return self.__target_state

    def get_current_state(self):
        return self.__current_state

    def get_level_actions(self):
        return self.__last_random_actions

    def get_mixed_level(self):
        return self.__mixed_level

    def random_action(self, level):
        actions = []
        for i in np.arange(level):
            actions.append(self.__next_actions[np.random.randint(len(self.__next_actions))])
        self.__last_random_actions = actions
        return actions

    def random_level_5(self):
        actions = self.random_action(5)

    def random_level_6(self):
        actions = self.random_action(6)

    def random_level_7(self):
        actions = self.random_action(7)

    def toString(self,state):
        print()
        for i in range(3):
            print("     ", int(state[0][i][0]), int(state[0][i][1]), int(state[0][i][2]))
        for i in range(3):
            print(int(state[2][i][0]), int(state[2][i][1]), int(state[2][i][2]), end=" ")
            print(int(state[4][i][0]), int(state[4][i][1]), int(state[4][i][2]), end=" ")
            print(int(state[3][i][0]), int(state[3][i][1]), int(state[3][i][2]), end=" ")
            print(int(state[5][i][0]), int(state[5][i][1]), int(state[5][i][2]))
        for i in range(3):
            print("     ", int(state[1][i][0]), int(state[1][i][1]), int(state[1][i][2]))
        print()

    def is_terminal(self,state):
        return np.array_equal(state,self.__target_state)

    def execute(self,actions):
        for a in actions:
            self.__current_state = self.__moves_lookup[a](self.__current_state)
        self.__move_history.append(actions)

    def move(self,action, state):
        state_operation = cp.deepcopy(state)
        for a in action:
            state_operation = self.__moves_lookup[a](state_operation)
        return state_operation

    # DONE: Get all next
    def get_next_state(self, state):
        states = []
        cost = self.__cost_price
        cost_weight = self.__cost_weight
        for action in self.__next_actions:
            state_operator = cp.deepcopy(state)
            states.append([self.__moves_lookup[action](state_operator), action, cost_weight*cost])
        return states

    # DONE: Get Fn of the State from target state
    def get_score(self, state):
        current_completion = np.array(state) - np.array(self.__target_state)
        current_completion = 54 - np.count_nonzero(current_completion)
        return current_completion

    # TODO: 启发函数
    def heuristic(self, state, steps):
        par_step_target = self.__mixed_level
        par_step = np.power(self.__base,steps)
        par_limit = self.__limit_times*par_step_target
        current_completion = np.array(state) - np.array(self.__target_state)
        current_completion = np.count_nonzero(current_completion)
        # current_opposite =
        return (current_completion/par_limit)*par_step

    # TODO: Closed 是否包含一个 state
    def is_not_in(self, state, closed):
        for clo in closed:
            if np.array_equal(state, clo):
                return False
        return True

def a_star(cube):
    fringe = util.PriorityQueue()
    start = [cube.get_start_state(), 0, []]
    p = 0
    fringe.push(start, p)  # queue push at index_0
    closed = []
    while not fringe.isEmpty():
        [state, cost, path] = fringe.pop()
        # print(state)
        if cube.is_terminal(state):
            cube.restore_cost = cost
            cube.restore_path= path
            cube.restore_heuristic = cube.heuristic(state, len(path))
            cube.restore_fringe_size = fringe.size()
            cube.restore_closed_size = len(closed)

            print("start state: => ", cube.get_start_state())
            print("target : => " , cube.get_target_state())
            print("cur : => " , state)
            print("cost : => " , cube.restore_cost)
            print("path : => " , cube.restore_path)
            print("start actions : => " , cube.get_start_actions())
            return path  # here is a deep first algorithm in a sense
        if  cube.is_not_in(state, closed):
            closed.append(state)
            for child_state, child_action, child_cost in cube.get_next_state(state):
                new_cost = cost + child_cost
                new_path = path + [child_action]

                heuristic_num = cube.heuristic(child_state, len(new_path))
                fringe.push([child_state, new_cost, new_path], new_cost + heuristic_num)
                pr = "cost => " + str(new_cost) \
                     + " | heu => " + str(heuristic_num) \
                     + " | fringe_size => " + str(fringe.size()) \
                     + " | closed => " + str(len(closed)) \
                     + " | action => " + str(new_path) \
                     + " | start => " + str(cube.get_start_actions()) \
                     + " | limit_times => " + str(cube.get_limit_times()) \
                     + " | base => " + str(cube.get_base()) \
                     + " | cost_price => " + str(cube.get_cost_price()) \
                     + " | cost_weight => " + str(cube.get_cost_weight())

                print(pr)

                if False:
                    tit = "AVG_" + str(cube.get_mixed_level()) + " mix_level = " + str(cube.get_mixed_level())\
                          + ", limit_times = 0.7, base = 1.041, cost_price = 1.28, cost_weight = 1.0"
                    with open("results/" + tit + ".txt", "a") as f:
                        f.write(pr)
                        f.write("\r\n")

# def pick_helper():
#

def main():
    """ Best Rank
        mix_level=6,
        limit_times=0.7,
        base=1.041,
        cost_price=1.28,
        cost_weight=1.0,
        start_actions=['F2', "B'", 'D2', 'R', "E'", 'B2'])
    """

    # cube = RubikCube()
    # te = [np.zeros((3, 3))]
    # tt = [np.ones((3, 3))]
    #
    # # for i in range(1, 6):
    # #     self.__target_state.append(np.ones((3, 3)) + self.__target_state[i - 1])
    # # print(cube.get_target_state())
    # print(te)
    # print(tt)
    #
    # return

    for k in [7]:
        arr = []
        min_finder = util.PriorityQueue()
        max_finder = util.PriorityQueue()

        # range_cost_price = np.arange(1.001, 1.1, 0.005)
        start = 1
        end = 10
        stp = 1
        lev = k
        range_cost_price = np.arange(start, end, stp)
        # tit = "cost_weight between " + str(start) + " to " + str(end) + ", step=" + str(stp)
        tit = "AVG_" + str(lev) + " mix_level = " + str(lev) + ", limit_times = 0.7, base = 1.041, cost_price = 1.28, cost_weight = 1.0"
        label1 = "time"
        label2 = "steps"


        for i in range_cost_price:
            time_start = time.time()

            # cube = RubikCube(mix_level=6, limit_times=0.7, base=1.041, cost_price=1.28, cost_weight=1.0,
            #                  start_actions=['F2', "B'", 'D2', 'R', "E'", 'B2'])

            cube = RubikCube(mix_level=lev, limit_times=0.7, base=1.041, cost_price=1.28, cost_weight=1.0)

            path = a_star(cube)

            time_end = time.time()
            time_cost = time_end - time_start
            min_finder.push((i, time_cost), time_cost)
            max_finder.push((i, time_cost), -time_cost)
            arr.append((i, time_cost, len(path)))

            print('time cost', time_cost, 's | steps cost: ', len(path))


        min_time = min(min_finder.pop())
        max_time = max(max_finder.pop())
        print("#############")
        print("min => ", min_time, " | max => ", max_time)

        fig = plt.figure()
        x = range_cost_price
        y1 = [a[1] for a in arr]
        y2 = [a[2] for a in arr]
        plt.xlabel('times')

        ax1 = fig.add_subplot(111)
        ax1.plot(x, y1, 'r.-')
        ax1.set_ylabel(label1)
        ax1.set_title(tit)

        ax2 = ax1.twinx()  # this is the important function
        ax2.plot(x, y2, 'g.-')
        ax2.set_ylabel(label2)

        plt.title(tit)
        plt.legend()
        plt.savefig("results/" + str(tit) + ".png", bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    main()