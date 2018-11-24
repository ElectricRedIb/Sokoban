import sys
import heapq

class Node():
    def __init__(self,parent,state,pos, heu):
        self.parent = parent
        self.state = state
        self.children = []
        self.pos = pos
        self.heu = heu
        if self.parent == None:
            self.step = 0
        else:
            self.step = self.parent.step
        #self.children = [node(self),node(self)]

    def makeChild(self,state, pos, heu):
        child = Node(self, state,pos, heu)
        self.children.append(child)
        return child

    def stepped(self):
        self.step = self.step + 1

    def __lt__(self, other):
        return self.heu < other.heu




class sokobanSolver():
    def __init__(self):
        self.TreeOfStates = []
        map = ""
        self.goalpos = []

        with open("../Information/2018-competation-map", 'r') as file:
            setting = file.readline()
            lines = file.readlines()[0:]
        lines = [line.strip() for line in lines]
        for line in lines:
            map += line

        for idx, c in enumerate(map):
            if c == 'M':
                startNode = Node(None, map, idx, 99)

        #startNode = Node(None, map)
        cols, rows, jewels = setting.split()
        self.cols = int(cols)
        self.rows = int(rows)
        self.jewels = int(jewels)
        self.TreeOfStates.append(startNode)
        self.deadPixel = self.zombiePix(map)


        print(startNode)

        for idx, c in enumerate(map):
            if c == "G":
                self.goalpos.append(idx)
        print(self.deadPixel)
        print(self.goalpos)

    def goal_check(self, node):
        for pos in self.goalpos:
            if node.state[pos] != 'J':
                return False
        return True

    def get_available_states(self, node):
        node.stepped()
        pos = node.pos
        state = node.state
        tempPos = [pos+self.cols, pos+1, pos-self.cols, pos-1]
        for idx, x in  enumerate(tempPos):
            if state[x] != 'X':
                if state[x] == 'J':
                    if idx == 0:
                        if state[x + self.cols] == '.' or state[x + self.cols] == 'G':
                            string = state[:pos] + '.' + state[pos+ 1:x] + 'M' + state[x+1:x+self.cols] + 'J' + state[x+self.cols+1:]
                            if not self.deadString(string,x+self.cols):
                                self.inputNode(node,string,tempPos[idx])
                                #self.TreeOfStates.insert(0,node.makeChild(string,tempPos[idx]))

                    elif idx == 1:
                        if state[x +1] == '.' or state[x +1] == 'G':
                            string = state[:x - 1] + '.MJ' + state[x+2:]
                            if not self.deadString(string, x + 1):
                                self.inputNode(node, string, tempPos[idx])
                               # self.TreeOfStates.insert(0,node.makeChild(string,tempPos[idx]))

                    elif idx == 2:
                        if state[x - self.cols] == '.' or state[x - self.cols] == 'G':
                            string  = state[:x - self.cols] + "J" + state[x - self.cols + 1:x] + 'M' + state[x + 1:pos] + '.' + state[pos + 1:]
                            if not self.deadString(string, x - self.cols):
                                self.inputNode(node, string, tempPos[idx])
                               # self.TreeOfStates.insert(0,node.makeChild(string,tempPos[idx]))

                    elif idx == 3:
                        if state[x - 1] == '.' or state[x - 1] == 'G':
                            string = state[:x - 1] +'JM.' + state[x + 2:]
                            if not self.deadString(string, x - 1):
                                self.inputNode(node, string, tempPos[idx])
                                #self.TreeOfStates.insert(0,node.makeChild(string,tempPos[idx]))

                elif state[x] == '.' or state[x] == 'G':
                    if idx == 0:
                        string = state[:pos] + '.' + state[pos + 1:x] + 'M' + state[x + 1:]
                    elif idx == 1:
                        string = state[:pos] + '.M' + state[x + 1:]
                    elif idx == 2:
                        string = state[:x] + 'M' + state[x + 1:pos] + '.' + state[pos+1:]
                    elif idx == 3:
                        string = state[:x] + 'M.' + state[pos+1:]
                    self.inputNode(node, string, tempPos[idx])
                    #self.TreeOfStates.append(node.makeChild(string,tempPos[idx]))

    def print_map(self, node):
        printstring = "\n"
        if node == None:
            return
        i = 0
        for c in node.state:
            printstring += c
            printstring += "\t"
            i += 1
            if i > self.cols - 1:
                i = 0
                printstring += "\n"
        printstring += "\n"
        print(printstring)


    def zombiePix(self,string):
        deadPixels = []
        for x in [1,self.rows-1]:       # dead cols
            for g in self.goalpos:
                if g%self.cols == x:
                    break
                for ind in range(1,self.rows-1):
                    deadPixels.append(ind*x)

        for x in [1,self.cols-1]:       # dead cols
            for g in self.goalpos:
                if int(g/self.cols) == x:
                    break
                for ind in range(1,self.cols-1):
                    deadPixels.append(ind*x)

        for idx, c in enumerate(string):    # corners that aren't goals
            if not c == 'G' and not c == 'X':
                if string[idx - 1] == 'X':
                    if string[idx + self.cols] == 'X' or string[idx - self.cols] == 'X':
                        deadPixels.append(idx)
                elif string[idx + 1] == 'X':
                    if string[idx + self.cols] == 'X' or string[idx - self.cols] == 'X':
                        deadPixels.append(idx)
        goalRow = False
        tempIdx = 1
        for idx in range(1,self.rows-1):
            print(idx * self.cols + 1)
            if string[idx * self.cols + 1] == 'G':
                goalRow = True
            elif string[idx * self.cols + 1] == 'X':
                goalRow = False
                tempIdx = idx
        if not goalRow:
            for idx in range(tempIdx,self.rows-1):
                deadPixels.append(idx * self.cols + 1)
        return deadPixels

    def deadString(self,string, j):
        #if not string[j] == 'J' :
         #   print("You Fucked Up")
        if string[j+1] == 'J':
            if string[j-self.cols] == 'X' and string[j + 1-self.cols] == 'X' or string[j+self.cols] == 'X' and string[j + 1+ self.cols] == 'X':
                return True
        elif string[j-1] == 'J':
            if string[j - self.cols] == 'X' and string[j - 1 - self.cols] == 'X' or string[j + self.cols] == 'X' and string[j - 1 + self.cols] == 'X':
                return True

        if string[j - self.cols] == 'J':
            if string[j - 1] == 'X' and string[j - self.cols - 1] == 'X' or string[j + 1] == 'X' and string[j - self.cols + 1] == 'X':
                return True
        elif string[j + self.cols] == 'J':
            if string[j - 1] == 'X' and string[j + self.cols - 1] == 'X' or string[j + 1] == 'X' and string[j + self.cols + 1] == 'X':
                return True


        return False

    def calcManhatten(self, pos1, pos2):
        xdif = abs((pos1 % self.cols) - (pos2 % self.cols))
        ydif = abs(int(pos1 / self.cols) - int(pos2 / self.cols))
        return xdif + ydif

    def getHeuristic(self, string, step, robPos):
        dist = 0
        tempcandist = 99
        tempgoaldist = 99
        tempdist = 0

        #Get manhatten distance from robot to nearest gem:
        for idx, c in enumerate(string):
            if c == "J" and not(self.goalpos[0] == idx or self.goalpos[1] == idx or self.goalpos[2] == idx or self.goalpos[3] == idx):
                tempdist = self.calcManhatten(robPos, idx)
                if  tempdist < tempcandist:
                    tempcandist = tempdist
        #print("Dist from robot to can: " + str(tempcandist))
        dist = tempcandist

        #Find manhatten distance between any can and nearest goal
        for idx, c in enumerate(string):
            if c == "J" and not(self.goalpos[0] == idx or self.goalpos[1] == idx or self.goalpos[2] == idx or self.goalpos[3] == idx):
                for i in range(0, self.jewels):
                    tempdist = self.calcManhatten(idx, self.goalpos[i])
                    if tempdist < tempgoaldist:
                        tempgoaldist = tempdist
                #print("Distance from can to goal: " + str(tempgoaldist))
                dist += tempgoaldist
                tempgoaldist = 99

        goaldist = self.goalCount(string)
        return (dist * goaldist) + step

    def inputNode(self,node,string,pos):
        heu = self.getHeuristic(string,node.step,pos)
        heapq.heappush(self.TreeOfStates,node.makeChild(string,pos,heu))
        # for idx , n in enumerate(self.TreeOfStates):
        #     if heu < n.heu:
        #         self.TreeOfStates.insert(idx,node.makeChild(string,pos,heu))
        #         return
        # self.TreeOfStates.append(node.makeChild(string,pos,heu + node.step))

    def test(self):
        for idx, c in enumerate(self.TreeOfStates[0].state):
            if c == 'M':
                self.get_available_states(self.TreeOfStates[0])

        for stt in self.TreeOfStates:
            self.print_map(stt)

    def isdead(self,node):
        for idx, c in enumerate(node.state):
            if c == 'J':
                for pix in self.deadPixel:
                    if idx == pix:
                        return True
        return False

        # dead = False
        # for idx, c in enumerate(node.state):
        #     if c == 'J':
        #         if node.state[idx - 1] == 'X':
        #             if node.state[idx + self.cols] == 'X' or node.state[idx - self.cols] == 'X':
        #                 dead = True
        #                 for g in self.goalpos:
        #                     if idx == g:
        #                         dead = False
        #                         break
        #                 if dead:
        #                     del node
        #                     return True
        #         elif node.state[idx + 1] == 'X':
        #             if node.state[idx + self.cols] == 'X' or node.state[idx - self.cols] == 'X':
        #                 dead = True
        #                 for g in self.goalpos:
        #                     if idx == g:
        #                         dead = False
        #                         break
        #                 if dead:
        #                     del node
        #                     return True
        # return dead

    def stateCheck(self,node):
        temp = node.parent
        i = 0
        while not temp == None:
            i = i + 1
            if temp.state == node.state:
                del node
                return False
            temp = temp.parent
        #print(i, " - many layers")
        return True

    def goalCount(self, string):
        goalcount = 0
        for pos in self.goalpos:
            if not string[pos] == 'J':
                goalcount += 1

        return goalcount

    def printSolution(self,node):
        #while not node == None:
        if node.parent == None:
            return node
        else:
            self.print_map(self.printSolution(node.parent))
            return node

    def Solution(self,node):
        solution = ""
        temp = node
        while not temp.parent == None:
            if (temp.pos - temp.parent.pos == -1):
                solution = 'L' + solution
            elif (temp.pos - temp.parent.pos == 1):
                solution = 'R' + solution
            elif (temp.pos - temp.parent.pos < -1):
                solution = 'U' + solution
            elif (temp.pos - temp.parent.pos > 1):
                solution = 'D' + solution
            temp = temp.parent

        return solution




    def solve(self):
        #for n in self.TreeOfStates:
        i = 0
        while not self.TreeOfStates[0] == None:
            n = heapq.heappop(self.TreeOfStates)
           # print(len(self.TreeOfStates), "\n")
           # print("Parent:")
            #self.print_map(n.parent)
           # print(" current:")
            if i%1000 == 0:
                self.print_map(n)
                print(n.heu, " - ", n.step)
            if(self.goal_check(n)):
                print(self.printSolution(n))
                self.print_map(n)
                break
            elif not(self.isdead(n)) and self.stateCheck(n):
                self.get_available_states(n)
                i = i + 1

        #print("Couldn't solve map")



