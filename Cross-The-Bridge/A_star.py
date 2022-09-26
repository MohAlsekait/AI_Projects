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


class AStar_CrossState():

    def __init__(self, n_person=0, st=([], 0), g=0, h=0, prev_state=None, action=None):
        """ Initializes the state with information passed from the arguments """
        # Number of persons
        self.num = n
        # The leftmost bit represents action to be done. 0: W->E, 1: E->W
        # The other bits represents states of each people
        self.state = st
        # Path cost (Time)
        self.gcost = g
        # Heuristic cost
        self.hcost = h
        # previous state
        self.prev = prev_state
        # action from previous state
        self.action_from_prev = action

    def __lt__(self, other):
        """ Allows for ordering the states by the path cost """
        return self.gcost + self.hcost < other.gcost + other.hcost

    move_num = 0

    def show_path(self):
        if self.prev is None:
            return

        self.prev.show_path()

        if self.state[1] == 1:
            print('\t{}. {} move to the west side'.format(AStar_CrossState.move_num + 1, self.action_from_prev))
        else:
            print('\t{}. ({}) returns with the flashlight'.format(AStar_CrossState.move_num + 1, self.action_from_prev))

        AStar_CrossState.move_num += 1

    def get_next_state(self):
        result = []
        global time

        if self.state[1] == 0:

            if sum(self.state[0]) == 0:
                return []

            elif sum(self.state[0]) == 1:
                index = self.state[0].index(1)
                tempList = [0 for i in range(self.num)]

                new_state = AStar_CrossState(self.num, (tempList, 1), self.gcost + time[index], 0, self, index + 1)
                result.append(new_state)

            else:
                remains = [i for i in range(n) if self.state[0][i] == 1]
                peopleToGo = itertools.combinations(remains, 2)

                for e in peopleToGo:
                    tempList = self.state[0].copy()
                    tempList[e[0]], tempList[e[1]] = 0, 0
                    heuristic = (self.num - sum(self.state[0]) * sum(time)) / self.num
                    addCost = max(time[e[0]], time[e[1]])

                    new_state = AStar_CrossState(self.num, (tempList, 1), self.gcost + addCost, heuristic, self,
                                                 (e[0] + 1, e[1] + 1))
                    result.append(new_state)

        else:
            if sum(self.state[0]) == 0:
                return []
            else:
                arrived = [i for i in range(self.num) if self.state[0][i] == 0]
                for person in arrived:
                    tempList = self.state[0].copy()
                    tempList[person] = 1

                    heuristic = (self.num - sum(self.state[0]) * sum(time)) / self.num

                    new_state = AStar_CrossState(self.num, (tempList, 0), self.gcost + time[person], heuristic, self,
                                                 person + 1)
                    result.append(new_state)

        return result


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

        AStar_CrossState.move_num = 0

        Open_List = queue.PriorityQueue()
        start_state = AStar_CrossState(n_person=n, st=START)
        Open_List.put(start_state)

        Closed_List = []


        search_cost = 0
        space = 0

        while True:
            length = Open_List.qsize()
            if length == 0:
                break
            space = max(space, length)


            p = Open_List.get()


            if p.state == END:
                print("Solution:")
                p.show_path()
                print("Solution Cost: {}".format(p.gcost))
                break

            search_cost += 1


            possibleState = p.get_next_state()

            for st in possibleState:
                cost = st.gcost + st.hcost

                flag = 0
                for val in Closed_List:
                    if equalTuple(st.state, val.state) and val.gcost + val.hcost < st.gcost + st.hcost:
                        flag = 1
                        break
                if flag:
                    continue


                Open_List.put(st)

            Closed_List.append(p)


        print("Search Cost: {}".format(search_cost))
        print("Space Requirement: {}\n".format(space))