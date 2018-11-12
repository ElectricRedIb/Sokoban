class sokobanSolver():
    #TreeOfStates = []
    #goalpos = []
    #state = []
    #cols = []
    #rows = []
    #jewels
    def __init__(self):
        self.TreeOfStates = []
        map = ""
        self.goalpos = []

        with open("../Information/2017-competation-map", 'r') as file:
            setting = file.readline()
            lines = file.readlines()[1:]
        lines = [line.strip() for line in lines]
        for line in lines:
            map += line

        self.state = map
        cols, rows, jewels = setting.split()
        self.cols = int(cols)
        self.rows = int(rows)
        self.jewels = int(jewels)
        print(map)

        for idx, c in enumerate(map):
            if c == "G":
                self.goalpos.append(idx)


    def goal_check(self, state):
        for pos in self.goalpos:
            if state[pos] != 'G':
                return False
        return True

    def get_available_states(self, state , pos):
        tempPos = [pos+self.cols, pos+1, pos-self.cols, pos-1]
        for idx, x in  enumerate(tempPos):
            #print(tempPos[idx])
            if state[x] != 'X':
                if state[x] == 'J':
                    if idx == 0:
                        if state[x + self.cols] == '.' or state[x + self.cols] == 'G':
                            string = state[:pos -1] + '.' + state[pos:x - 1] + 'M' + state[x:]
                            #string[x] = 'M'
                            #string[pos] = '.'
                            #string[x+self.cols] = 'J'
                            self.TreeOfStates.append(string)
                    elif idx == 1:
                        if state[x +1] == '.' or state[x +1] == 'G' :
                            string = state[:x - 1] + '.M' + state[x:]
                            #string = state
                            #string[x] = 'M'
                            #string[pos] = '.'
                            #string[x + 1] = 'J'
                            self.TreeOfStates.append(string)

                    elif idx == 2:
                        if state[x - self.cols] == '.' or state[x - self.cols] == 'G':
                            string  = state[:x - self.cols] + "J" + state[x - self.cols + 1:x] + 'M' + state[x + 1:pos] + '.' + state[pos + 1:]
                            #string[x] = 'M'
                            #string[pos] = '.'
                            #string[x - self.cols] = 'J'
                            self.TreeOfStates.append(string)
                    elif idx == 3:
                        if state[x - 1] == '.' or state[x - 1] == 'G':
                            string = state[:x - 1] +'JM.' + state[x + 2:]
                            #string[x] = 'M'
                            #string[pos] = '.'
                            #string[x - 1] = 'J'
                            self.TreeOfStates.append(string)
                elif state[x] == '.' or state[x] == 'G':
                    if idx == 0:
                        string = state[:pos] + '.' + state[pos + 1:x] + 'M' + state[x + 1:]
                    elif idx == 1:
                        string = state[:x - 1] + '.M' + state[x + 1:]
                    elif idx == 2:
                        string = state[:x] + 'M' + state[x + 1:pos - 1] + '.' + state[pos:]
                    elif idx == 3:
                        string = state[:x - 1] + 'M.' + state[x + 1:]
                    #string[x] = 'M'
                    #string[pos] = '.'
                    self.TreeOfStates.append(string)

    def test(self):
        for idx, c in enumerate(self.state):
            if c == 'M':
                self.get_available_states(self.state, idx)

        for stt in self.TreeOfStates:
            print(stt)



