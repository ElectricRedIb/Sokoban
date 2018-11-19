import sys

class Node():
    def __init__(self,parent,state,pos):
        self.parent = parent
        self.state = state
        self.children = []
        self.pos = pos
        #self.children = [node(self),node(self)]

    def makeChild(self,state, pos):
        child = Node(self, state,pos)
        self.children.append(child)
        return child






class sokobanSolver():
    def __init__(self):
        self.TreeOfStates = []
        map = ""
        self.goalpos = []

        with open("../Information/testmap-easy", 'r') as file:
            setting = file.readline()
            lines = file.readlines()[0:]
        lines = [line.strip() for line in lines]
        for line in lines:
            map += line

        for idx, c in enumerate(map):
            if c == 'M':
                startNode = Node(None, map, idx)

        #startNode = Node(None, map)
        cols, rows, jewels = setting.split()
        self.cols = int(cols)
        self.rows = int(rows)
        self.jewels = int(jewels)
        self.TreeOfStates.append(startNode)

        print(startNode)

        for idx, c in enumerate(map):
            if c == "G":
                self.goalpos.append(idx)


    def goal_check(self, node):
        for pos in self.goalpos:
            if node.state[pos] != 'G':
                return False
        return True

    def get_available_states(self, node):
        pos = node.pos
        state = node.state
        tempPos = [pos+self.cols, pos+1, pos-self.cols, pos-1]
        for idx, x in  enumerate(tempPos):
            if state[x] != 'X':
                if state[x] == 'J':

                    if idx == 0:
                        if state[x + self.cols] == '.' or state[x + self.cols] == 'G':
                            string = state[:pos -1] + '.' + state[pos:x - 1] + 'M' + state[x:]
                            self.TreeOfStates.append(node.makeChild(string,tempPos[idx]))

                    elif idx == 1:
                        if state[x +1] == '.' or state[x +1] == 'G':
                            string = state[:x - 1] + '.M' + state[x:]
                            self.TreeOfStates.append(node.makeChild(string,tempPos[idx]))

                    elif idx == 2:
                        if state[x - self.cols] == '.' or state[x - self.cols] == 'G':
                            string  = state[:x - self.cols] + "J" + state[x - self.cols + 1:x] + 'M' + state[x + 1:pos] + '.' + state[pos + 1:]
                            self.TreeOfStates.append(node.makeChild(string,tempPos[idx]))

                    elif idx == 3:
                        if state[x - 1] == '.' or state[x - 1] == 'G':
                            string = state[:x - 1] +'JM.' + state[x + 2:]
                            self.TreeOfStates.append(node.makeChild(string,tempPos[idx]))

                elif state[x] == '.' or state[x] == 'G':
                    if idx == 0:
                        string = state[:pos] + '.' + state[pos + 1:x] + 'M' + state[x + 1:]
                    elif idx == 1:
                        string = state[:x - 1] + '.M' + state[x + 1:]
                    elif idx == 2:
                        string = state[:x] + 'M' + state[x + 1:pos - 1] + '.' + state[pos:]
                    elif idx == 3:
                        string = state[:x - 1] + 'M.' + state[x + 1:]
                    self.TreeOfStates.append(node.makeChild(string,tempPos[idx]))

    def print_map(self, node):
        print("\n")
        i = 0
        for c in node.state:
            sys.stdout.write(c+"\t")
            i += 1
            if i > self.cols - 1:
                i = 0
                print("\n")
        print("\n")



    def test(self):
        for idx, c in enumerate(self.TreeOfStates[0].state):
            if c == 'M':
                self.get_available_states(self.TreeOfStates[0])

        for stt in self.TreeOfStates:
            self.print_map(stt)


    def solve(self):
        for n in self.TreeOfStates:
            if(self.goal_check(n)):
                self.print_map(n)
            else:
                self.get_available_states(self.TreeOfStates)




