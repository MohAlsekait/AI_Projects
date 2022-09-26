import queue
import itertools


def equalTuple(tu1, tu2):
    """ Check for equality of two tuple representing State """
    for _, (a, b) in enumerate(zip(tu1[0], tu2[0])):
        if a != b:
            return False
    return tu1[1] == tu2[1]


def visited(st, vstAry):
    """ Check for existence of st in vstAry list """
    for tup in vstAry:
        if equalTuple(st, tup):
            return True
    return False


class UCS_CrossState():

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

    move_num = 1

    def show_path(self):
        """ Recursively outputs the list of moves and states along path """
        if self.prev is None:
            return

        self.prev.show_path()
        if self.state[1] == 1:
            print('\t{}. {} move to the west side'.format(UCS_CrossState.move_num + 1, self.action_from_prev))
        else:
            print('\t{}. {} returns with the flashlight'.format(UCS_CrossState.move_num + 1, self.action_from_prev))

        UCS_CrossState.move_num += 1

    def get_next_state(self):
        result = []
        global time
        if self.state[1] == 0:
            if sum(self.state[0]) == 0:
                return []

            elif sum(self.state[0]) == 1:  # Generally this is when n = 1
                index = self.state[0].index(1)
                tempList = [0 for i in range(self.num)]

                new_state = UCS_CrossState(self.num, (tempList, 1), self.cost + time[index], self, (index))
                result.append(new_state)

            else:
                # Get combination(2) of indices of remaining people
                remains = [i for i in range(n) if self.state[0][i] == 1]
                peopleToGo = itertools.combinations(remains, 2)

                for e in peopleToGo:
                    tempList = self.state[0].copy()
                    tempList[e[0]], tempList[e[1]] = 0, 0
                    addCost = max(time[e[0]], time[e[1]])
                    new_state = UCS_CrossState(self.num, (tempList, 1), self.cost + addCost, self, e)
                    result.append(new_state)

        else:
            if sum(self.state[0]) == 0:
                return []
            else:
                arrived = [i for i in range(self.num) if self.state[0][i] == 0]
                for person in arrived:
                    tempList = self.state[0].copy()
                    tempList[person] = 1
                    new_state = UCS_CrossState(self.num, (tempList, 0), self.cost + time[person], self, (person))
                    result.append(new_state)

        return result



print("ucs algorithm:")
with open("input.txt", "r") as filex:
        cases = int(filex.readline())

        for case in range(cases):

            n = int(filex.readline())
            if n <= 0:
                print("Number of people should be positive")
                exit()

            temp = filex.readline()
            time = []

            for x in temp.split(","):
                time.append(int(x))

            if n != len(time):
                print("The length of time series should be equal to number of persons")
                exit()

            print("Test Case #", case + 1)

            START = ([1 for k in range(n)], 0)
            END = ([0 for k in range(n)], 1)

            UCS_CrossState.move_num = 0

            frontier = queue.PriorityQueue()
            start_state = UCS_CrossState(n_person=n, st=START)
            frontier.put(start_state)

            visit = []
            search_cost = 0
            space = 0

            while True:
                length = frontier.qsize()
                if length == 0:
                    break
                space = max(space, length)

                p = frontier.get()
                if equalTuple(p.state, END):
                    print("Solution:")
                    p.show_path()
                    print("Solution Cost: {}".format(p.cost))
                    break

                search_cost += 1
                visit.append(p.state)


                possibleState = p.get_next_state()

                for st in possibleState:
                    if visited(st.state, visit):
                        continue
                    frontier.put(st)


            print("Search Cost: {}".format(search_cost))
            print("Space Requirement: {}\n".format(space))
print("**************************")
def iterative_deepening_search(node, target, current_depth, max_depth):
    global finalresult
    global search_cost
    global space
    space = max(space, depth)
    if equalTuple(node.state, END):

        finalresult.append(node)
        return True


    possibleState = node.get_next_state()

    if current_depth == max_depth:
        if len(possibleState) > 0:

            return False
        else:
            return True

    bottom_reached = True
    for st in possibleState:
        search_cost += 1
        bottom_reached_rec = iterative_deepening_search(st, target, current_depth + 1, max_depth)
        bottom_reached = bottom_reached and bottom_reached_rec

    return bottom_reached

with open("input.txt", "r") as infile:
    print("ids algorithm:")

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

        UCS_CrossState.move_num= 0
        finalresult = []
        search_cost = 0
        space = 0
        startObject = UCS_CrossState(n_person=n, st=START)


        depth = 1
        bottom_reached = False  # Variable to keep track if we have reached the bottom of the tree
        while not bottom_reached:

            bottom_reached = iterative_deepening_search(startObject, END, 0, depth)

            depth *= 2

        result = None
        mincost = float('inf')
        for res in finalresult:

            if mincost > res.cost:
                mincost = res.cost
                result = res

        print("Solution:")
        result.show_path()
        print("Solution Cost: {}".format(result.cost))

        # Print out results
        print("Search Cost: {}".format(search_cost))
        print("Space Requirement: {}\n".format(space))