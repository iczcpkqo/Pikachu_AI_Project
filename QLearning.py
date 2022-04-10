import random
import copy as cp
from RubikCube import cube
from collections import Counter

class QLearningAgent():
    def __init__(self, alpha, discount, epsilon):
        self.alpha = alpha
        self.discount = discount
        self.epsilon = epsilon
        self.qValues = Counter()

    def getQValue(self,state,action):
        qValue = self.qValues[(self.converState(state),tuple(action))]
        return qValue

    def computeValueFromQValues(self, state):
        # store q value for actions
        action_counter = Counter()
        # get legal actions
        actions = cube.getActions()
        # if there are no legal actions
        if len(actions) == 0:
            return 0.0
        # get q value
        for action in actions:
            action_counter[tuple(action)] = self.getQValue(state, action)
        # get maximum value
        max = action_counter[self.argMax(action_counter)]
        return max

    def computeActionFromQValues(self, state):
        # store q value for actions
        action_counter = Counter()
        # get legal actions
        actions = cube.getActions()
        # if there are no legal actions
        if len(actions) == 0:
            return None
        # get q value
        for action in actions:
            action_counter[tuple(action)] = self.getQValue(state, action)
        # get best action
        act = self.argMax(action_counter)
        return act

    def selectAction(self, state):
        # Get Actions
        legalActions = cube.getActions()
        # random action
        if random.random() < self.epsilon:
            action = random.choice(legalActions)
        # best policy action
        else:
            action = self.computeActionFromQValues(state)
        return action

    # update q values
    def update(self, state, action):
        # sample = R(state,action,nextState) + discount * max(Q(nextState,action'))
        # new Q value = (1-alpha) * old Q value + alpha * sample
        sample = cube.reward(state,action) + self.discount * self.computeValueFromQValues(cube.nextState(action,state))
        self.qValues[(self.converState(state), tuple(action))] = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * sample

    def argMax(self,counter):
        if len(list(counter.keys())) == 0:
            return None
        all = list(counter.items())
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def converState(self,state):
        result = tuple(tuple(tuple(i) for i in s) for s in state)
        return result



agent = QLearningAgent(0.5,0.9,0.2)
# agent.selectAction(cube.getCurrentState())
for episode in range(1000):
    state = cp.deepcopy(cube.getStartState())
    cube.toString(state)
    print('Episode:',episode+1)
    i = 1
    while True:
        if cube.isTerminal(state):
            break
        print(i)
        # generate action
        action = agent.selectAction(state)
        # update Q values
        agent.update(state,action)
        state = cube.nextState(action,state)
        i = i + 1

    print(agent.qValues)

qValueDic = {}
keys = agent.qValues.keys()
for key in keys:
    qValueDic[key[0]] = {key[1]:agent.qValues[key]}
print(qValueDic)

state = cp.deepcopy(cube.getCurrentState())
cube.toString(state)
while cube.isTerminal(state) == False:
    actions = qValueDic[agent.converState(state)]
    best_action = max(actions, key=actions.get)
    cube.move(best_action)
    state = cp.deepcopy(cube.getCurrentState())
    cube.toString(state)


