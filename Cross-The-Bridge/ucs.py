import queue
import itertools


def equalTuple(tu1, tu2):
    """ Check for equality of two tuple representing State """
    for _, (a, b) in enumerate(zip(tu1[0], tu2[0])):
        if a != b:
            return False
    return tu1[1] == tu2[1]

    """ Check for existence of st in vstAry list """
    for tup in vstAry:
        if equalTuple(st, tup):
            return True
    return False


class CrossState():

    def __init__(self, n_person=0, st=([], 0), c=0, prev_state=None, action=None):
        """ Initializes the state with information passed from the arguments """
        # Number of persons
        self.num = n
        # Tuple representing state
        # First element-list represents state about remaining persons
        # Second element represents action to be done. 0: W->E, 1: E->W
        self.state = st
        # Path cost (Time)
        self.cost = c
        # previous state
        self.prev = prev_state
        # action from previous state
        self.action_from_prev = action

    def __lt__(self, other):
        """ Allows for ordering the states by the path cost """
        return self.cost < other.cost

    move_num = 1  # Used by show_path() to count moves in the solution path

    def show_path(self):
        """ Recursively outputs the list of moves and states along path """
        if self.prev is None:
            return

        self.prev.show_path()
        if self.state[1] == 1:
            print('\t{}. {} move to the west side'.format(CrossState.move_num + 1, self.action_from_prev))
        else:
            print('\t{}. {} returns with the flashlight'.format(CrossState.move_num + 1, self.action_from_prev))

        CrossState.move_num += 1

    def get_next_state(self):
        """ Generates list of moveable CrossState objects """
        result = []
        global time
        if self.state[1] == 0:  # This means that two people should be crossed
            if sum(self.state[0]) == 0:
                return []

            elif sum(self.state[0]) == 1:  # Generally this is when n = 1
                index = self.state[0].index(1)
                tempList = [0 for i in range(self.num)]

                new_state = CrossState(self.num, (tempList, 1), self.cost + time[index], self, (index))
                result.append(new_state)

            else:
                # Get combination(2) of indices of remaining people
                remains = [i for i in range(n) if self.state[0][i] == 1]
                peopleToGo = itertools.combinations(remains, 2)

                for e in peopleToGo:
                    tempList = self.state[0].copy()
                    tempList[e[0]], tempList[e[1]] = 0, 0
                    addCost = max(time[e[0]], time[e[1]])
                    new_state = CrossState(self.num, (tempList, 1), self.cost + addCost, self, e)
                    result.append(new_state)

        else:  # This means that one person should be returned
            if sum(self.state[0]) == 0:  # Generally There is no such case.
                return []
            else:
                arrived = [i for i in range(self.num) if self.state[0][i] == 0]
                for person in arrived:
                    tempList = self.state[0].copy()
                    tempList[person] = 1
                    new_state = CrossState(self.num, (tempList, 0), self.cost + time[person], self, (person))
                    result.append(new_state)

        return result


def iterative_deepening_search(node, target, current_depth, max_depth):
    global finalresult
    global search_cost
    global space
    space = max(space, depth)
    if equalTuple(node.state, END):  # We have found the goal node we we're searching for
        # Find goal. But to find optimal path, we continue searching and store current node to resultlist
        finalresult.append(node)
        return True

    # Get possible next states of node
    possibleState = node.get_next_state()

    if current_depth == max_depth:
        # We have reached the end for this depth...
        if len(possibleState) > 0:
            # ...but we have not yet reached the bottom of the tree
            return False
        else:
            return True

    # Recurse with all children
    bottom_reached = True
    for st in possibleState:
        search_cost += 1
        bottom_reached_rec = iterative_deepening_search(st, target, current_depth + 1, max_depth)
        bottom_reached = bottom_reached and bottom_reached_rec

    # We've gone through all children and not found the goal node
    return bottom_reached


with open("input.txt", "r") as infile:
    cases = int(infile.readline())

    for case in range(cases):

        n = int(infile.readline())
        if n <= 0:
            print("Number of people should be positive")
            exit()

        temp = infile.readline()
        time = []

        for x in temp.split(","):
            time.append(int(x))

        if n != len(time):
            print("The length of time series should be equal to number of persons")
            exit()

        print("Test Case #", case + 1)

        START = ([1 for k in range(n)], 0)
        END = ([0 for k in range(n)], 1)

        # Initialize variable move_num of CrossState with zero
        CrossState.move_num = 0
        finalresult = []
        # Initialize visit array, search cost, space
        search_cost = 0
        space = 0
        startObject = CrossState(n_person=n, st=START)

        # Start by doing DFS with a depth of 1, keep doubling depth
        # until we reach the "bottom" of the tree or find the END state
        depth = 1
        bottom_reached = False  # Variable to keep track if we have reached the bottom of the tree
        while not bottom_reached:
            # One of the "end nodes" of the search with this depth has to still have children and set this to False again
            bottom_reached = iterative_deepening_search(startObject, END, 0, depth)

            # We haven't found the goal node, but there are still deeper nodes to search through
            depth *= 2

        result = None
        mincost = float('inf')
        for res in finalresult:
            # To find optimal path, select res with minimum cost
            if mincost > res.cost:
                mincost = res.cost
                result = res

        print("Solution:")
        result.show_path()
        print("Solution Cost: {}".format(result.cost))

        # Print out results
        print("Search Cost: {}".format(search_cost))
        print("Space Requirement: {}\n".format(space))