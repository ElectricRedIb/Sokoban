import sys
import heapq
import math

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
        return self.heu <= other.heu




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

        self.pyth = self.pythoMap(map)
        self.heuristics = self.heuristicsMap(map)
        self.print_maplist(self.heuristics)
        self.print_maplist(self.pyth)

    def goal_check(self, node):
        for pos in self.goalpos:
            if node.state[pos] != 'J':
                return False
        return True

    def pythoMap(self,string):
        heuMap = []
        for idx,c in enumerate(string):
            if c == 'X':
                heuMap.append(-1)
            elif c == 'G':
                heuMap.append(0)
            else:
                heuMap.append(self.getPyth(idx))
               # print(heuMap)
        return heuMap
    def heuristicsMap(self,string):
        heuMap = []
        for idx,c in enumerate(string):
            if c == 'X':
                heuMap.append(-1)
            elif c == 'G':
                heuMap.append(0)
            else:
                heuMap.append(self.getHeur(idx,string))
               # print(heuMap)
        return heuMap


    def getHeur(self,pos ,string):
        openlist = [(pos,0)]
        closedlist = []

        heuristic = 0
        while len(openlist) > 0:
            restart = False
            idx = openlist.pop(0)
            for c in closedlist:
                if idx[0] == c:
                    #print(idx, " TRUE ", len(openlist))
                    restart = True
            if not restart:
                if self.isAGoal(idx[0]):
                    return idx[1]
                else:
                    #print(idx, " - ")
                    tempPos = [idx[0] + self.cols, idx[0] + 1, idx[0] - self.cols, idx[0] - 1]
                    for x in tempPos:
                            if string[x] != 'X':
                                tup = (x,idx[1]+1)
                                openlist.append(tup)
                    closedlist.append(idx[0])

    def getHeurToJ(self,pos, j,string):
        openlist = [(pos,0)]
        closedlist = []

        heuristic = 0

        while len(openlist) > 0:
            restart = False
            idx = openlist.pop(0)
            for c in closedlist:
                if idx[0] == c:
                    #print(idx, " TRUE ", len(openlist))
                    restart = True
            if not restart:
                if idx[0] == j:
                    return idx[1]
                else:
                    #print(idx, " - ")
                    tempPos = [idx[0] + self.cols, idx[0] + 1, idx[0] - self.cols, idx[0] - 1]
                    for x in tempPos:
                            if string[x] != 'X':
                                tup = (x,idx[1]+1)
                                openlist.append(tup)
                    closedlist.append(idx[0])

    def getPyth(self,pos):
        retDist = 999
        for g in self.goalpos:
            x1 = pos % self.cols
            y1 = int(pos / self.cols)
            x2 = g % self.cols
            y2 = int(g / self.cols)
            temp = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
            if temp < retDist:
                retDist = temp
        return int(retDist)

    def getPythToGoal(self,pos,string):
        retDist = 999
        for g in self.goalpos:
            if string[g] != 'J':
                x1 = pos % self.cols
                y1 = int(pos / self.cols)
                x2 = g % self.cols
                y2 = int(g / self.cols)
                temp = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
                if temp < retDist:
                    retDist = temp
        return int(retDist)



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

    def print_maplist(self, list):
        printstring = "\n"
        i = 0
        for c in list:
            printstring += str(c)
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

        # availMoves = []
        # for g in self.goalpos:
        #     if string[g] != 'J':
        #         tempPos = [g + self.cols, g + 1, g - self.cols, g - 1]
        #         for idx in tempPos:
        #             if string[idx] != 'X':
        #                 if self.isClear(string, g - 2*(g-idx)):
        #                     availMoves.append(idx)
        # if len(availMoves) < 1:
        #     return True

        return False#self.checkPosMoves(string,j)

    def checkPosMoves(self,string,j):
        availMoves = []
        tempPos = [j + self.cols, j + 1, j - self.cols, j - 1]
        for idx, x in enumerate(tempPos):
            if self.isClear(string, x) and self.isClear(string,tempPos[(idx+2)%4]): #or self.isAGoal(x):
                availMoves.append(x)
        if len(availMoves) > 2:
            return True
        elif len(availMoves) == 0:
            return False
        else:
            for x in availMoves:
                if string[x] != 'M' and self.isDeadPixel(x):
                    return True
                    #if not(self.isClear(string,x-self.cols) and self.isClear(string,j-self.cols) or string[x + self.cols] != 'X' and string[j+self.cols] != 'X'):
            return False

    def deadPixelDead(self,string):
        for idx in self.deadPixel:
            tempPos = [idx + self.cols, idx + 1, idx - self.cols, idx - 1]
            count = 0
            for x in range(0, 4):
                if self.isClear(string,tempPos[x]):
                    if self.isDeadPixel(tempPos[x]):
                        if not self.clearPerimeter(string,tempPos[x]):
                            return True
        return False




    def clearPerimeter(self,string,idx):
        tempPos = [idx + self.cols, idx + 1, idx - self.cols, idx - 1]
        for x in range(0, 4):
            if self.isClear(string, tempPos[x]) and not self.isDeadPixel(tempPos[x]):
                return True
        return False

    def isClear(self,string,idx):
        if string[idx] == 'X' or string[idx] == 'J':
            return False
        return True

    def isDeadPixel(self,pix):
        for x in self.deadPixel:
            if pix == x:
                return True
        return False

    def isAGoal(self,pix):
        for x in self.goalpos:
            if pix == x:
                return True
        return False
    # def circleDeadlock(self,j,idx, dir,string):
    #     if idx == j:
    #         return True
    #
    #     if int(idx/self.cols) == 0 and dir == 0:     #first row
    #         dir = 2
    #     elif idx%self.cols == 0 and dir == :        #first col
    #         dir =
    #     elif dir == 0:  # up
    #         if string[idx - self.cols] == X:


    def calcManhatten(self, pos1, pos2):
        xdif = abs((pos1 % self.cols) - (pos2 % self.cols))
        ydif = abs(int(pos1 / self.cols) - int(pos2 / self.cols))
        return xdif + ydif

    def getHeuristic(self, string, step, robPos):
        dist = 0
        tempcandist = 99
        tempgoaldist = 0
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
            if c == "J" and not self.isAGoal(idx):
                for i in range(0, self.jewels):
                    tempdist = self.calcManhatten(idx, self.goalpos[i])
                    if tempdist > tempgoaldist:
                        tempgoaldist = tempdist
                #print("Distance from can to goal: " + str(tempgoaldist))
                dist += tempgoaldist
                tempgoaldist = 0

        goaldist = self.goalCount(string)
        return (dist + step)*goaldist


    def inputNode(self,node,string,pos):

        tempcandist = 99
        tempidx = 99
        for idx, c in enumerate(string):
            if c == "J" and not self.isAGoal(idx):
                tempdist = self.heuristics[idx]
                if tempdist < tempcandist:
                    tempidx = idx
                    tempcandist = tempdist
         #print("Dist from robot to can: " + str(tempcandist))
        #dist = self.calcManhatten(tempidx,pos)
        dist = self.getHeurToJ(pos,tempidx,string)

        heu = 0
        count = 0
        for idx, c in enumerate(string):
            if c == "J" and not self.isAGoal(idx):
                heu += (math.pow(self.getPythToGoal(idx,string)+ dist,2) )
                count += 1
        heapq.heappush(self.TreeOfStates, node.makeChild(string, pos, (heu + node.step)*self.goalCount(string)))
        #heu = self.getHeuristic(string,node.step,pos)
        #heapq.heappush(self.TreeOfStates, node.makeChild(string, pos, heu))
        # for idx , n in enumerate(self.TreeOfStates):
        #     if heu < n.heu:
        #         self.TreeOfStates.insert(idx,node.makeChild(string,pos,heu))
        #         return
        # self.TreeOfStates.append(node.makeChild(string,pos,heu + node.step))

    def isdead(self,node):
        for idx, c in enumerate(node.state):
            if c == 'J':
                for pix in self.deadPixel:
                    if idx == pix:
                        return True

        for g in self.goalpos:
             availMoves = []
             temp = True
             if node.state[g] != 'J':
                 tempPos = [g + self.cols, g + 1, g - self.cols, g - 1]
                 for idx in tempPos:
                     if node.state[idx] != 'X':
                         availMoves.append(idx)
                         #if self.isClear(node.state, g - 2 * (g - idx)):
                 if len(availMoves) < 1:
                     return True
                 else:
                     temp = 0
                     for x in availMoves:
                         if self.availableMoves(node.state,x):
                             temp +=1
                     if temp == 0:
                         #self.print_map(node)
                         #print(g, ": ", tempPos)
                         return True
        return False

    def availableMoves(self,string,idx):                # if available move return true else
       # availMoves = []
        tempPos = [idx + self.cols, idx + 1, idx - self.cols, idx - 1]
        for x in range(0,4):
            temp = False
            if string[tempPos[x]] != 'X' and string[tempPos[(x+2)%4]] != 'X':
                if self.isClear(string, tempPos[x]) and self.isClear(string,tempPos[(x+2)%4]):
                    return True
                elif string[tempPos[x]] == 'J':
                    if self.availableMoves(string,tempPos[x]):
                        return True
        return False

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
            #print(" current:")
            if i%1000 == 0:
                self.print_map(n)
                print(n.heu, " - ", n.step, " - ", self.goalCount(n.state))
            if(self.goal_check(n)):
                self.printSolution(n)
                self.print_map(n)
                print(n.step, " : ", self.Solution(n))
                break
            elif not(self.isdead(n)) and self.stateCheck(n):
                self.get_available_states(n)
                i = i + 1

        #print("Couldn't solve map")



