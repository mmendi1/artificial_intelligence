from queue import Queue

goal_state = [0, 1, 2, 5, 4, 3]

class State:
    def __init__(self,state,tile,cost,parent):
        self.state = state
        self.tile = tile
        self.cost = cost
        self.parent = parent

    def isGoal(self):
        return self.state == goal_state

    def emptyIndex(self):
        return self.state.index(0)

    def actions(self):
        actions = ['up','down','left','right']
        empty = self.emptyIndex()
        if empty<3:
            actions.remove('up')
        if empty>2:
            actions.remove('down')
        if empty%3==0:
            actions.remove('left')
        if empty==2 or empty==5:
            actions.remove('right')
        return actions

    def nextState(self,move):
        empty = self.emptyIndex()
        next = list(self.state)
        change_in_index = {'up':-3,'down':3,'left':-1,'right':1}
        new_position = empty + change_in_index[move]
        next[empty], next[new_position] = next[new_position], next[empty]
        next_state = State(next,next[empty],self.cost+1,self)
        return next_state

    def neighbourhood(self):
        neighbours = list()
        for action in self.actions():
            neighbours.append(self.nextState(action))
        neighbours.sort(key=lambda s:s.tile)
        return neighbours

    def is_in(self,lista):
        for s in lista:
            if s.state == self.state:
                return True
        return False

    def neighbourhood_dfs(self):
        neighbours = list()
        for action in self.actions():
            neighbours.append(self.nextState(action))
        neighbours.sort(key = lambda s:s.tile)
        neighbours.reverse()
        return neighbours

    def traverse(self,start):
        history = list()
        history.append(self)
        while(self!=start):
            history.append(self.parent)
            self = self.parent
        history.reverse()
        return history

    def printMatrix(self):
        one = self.state[:3]
        two = self.state[3:]
        print(one)
        print(two)

    def toList(self):
        return list(self.state)


#Breadth first search
def bfs(start):
    frontier = list()
    frontier.append(start)
    visited = list()
    while len(frontier)!=0:
       state = frontier.pop(0)
       visited.append(state)
       if state.isGoal():
           print("Total cost: " + str(state.cost))
           return state.traverse(start)
       for neighbour in state.neighbourhood():
           if not (neighbour.is_in(visited)):
               frontier.append(neighbour)
    return "Not found"


#Uniform cost search
def ucs(start):
    frontier = list()
    frontier.append(start)
    visited = list()
    while len(frontier)!=0:
       state = frontier.pop(0)
       visited.append(state)
       if state.isGoal():
           print("Total cost: " + str(state.cost))
           return state.traverse(start)
       for neighbour in state.neighbourhood():
           if not (neighbour.is_in(visited)):
               frontier.append(neighbour)
               frontier.sort(key = lambda c:c.cost)
    return "Not found"
    

#Depth first search
def dfs(start):
    frontier = []
    frontier.insert(0,start)
    visited = []
    while frontier: #while queue is not empty
        state = frontier.pop(0) #remove from the end
        visited.append(state)
        if state.isGoal():
            print("Total cost: " + str(state.cost))
            return state.traverse(start)
        else:
            for neighbour in state.neighbourhood_dfs():
                if not (neighbour.is_in(visited)):
                    #neighbour.cost = 1 + state.cost
                    frontier.insert(0,neighbour)
    return "Not found"


#Iterative deepening
def ids(start,maxDepth):
    for depth in range(maxDepth):
        frontier = []
        visited = []
        state = start
        frontier.append(state)
        while frontier:
            visited.append(state)
            if state.isGoal():
                print("Total cost:" + str(state.cost))
                return state.traverse(start)
            for neighbour in state.neighbourhood_dfs():
                if neighbour.cost <= depth and (not (neighbour.is_in(visited))):
                    frontier.append(neighbour)
            state = frontier.pop()
    return "Not found"