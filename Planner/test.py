from sokobanSolver import sokobanSolver


map = ""
with open("../Information/2018-competation-map", 'r') as file:
    setting = file.readline()
    lines = file.readlines()[0:]
lines = [line.strip() for line in lines]
for line in lines:
    map += line

pos = 0
for idx, c in enumerate(map):
    if c == 'M':
        pos = idx

Scols, Srows, Sjewels = setting.split()
cols = int(Scols)
rows = int(Srows)
jewels = int(Sjewels)

#ss = sokobanSolver.sokobanSolver()
#ss = sokobanSolver()
#ss.solve()
solution = "LDLLLUUUURRDRUUURULDDDLLLDDRULURRLDDLDDRUUURRUUUULLULDRRDRDDLDLLURRDRUUURULDDDLLDDDDRRULDLUUULURRDRUUURUULLLRDRURD"
glueSolution = ""
state = map
pushingCan = False
temp = False
direction = "L"

def makeMobe(string,pos,direction):
    global pushingCan
    state = string
    if direction == 'L':
         tempPos = pos - 1
    elif direction == 'R':
        tempPos = pos + 1
    elif direction == 'U':
        tempPos = pos - cols
    elif direction == 'D':
        tempPos = pos + cols
    x = tempPos
    print(x)
    if state[x] == 'J':
        if direction == 'D':
            if state[x + cols] == '.' or state[x + cols] == 'G':
                string = state[:pos] + '.' + state[pos + 1:x] + 'M' + state[x + 1:x + cols] + 'J' + state[x + cols + 1:]
                pushingCan = True
        elif direction == 'R':
            if state[x + 1] == '.' or state[x + 1] == 'G':
                string = state[:x - 1] + '.MJ' + state[x + 2:]
                pushingCan = True
        elif direction == 'U':
            if state[x - cols] == '.' or state[x - cols] == 'G':
                string = state[:x - cols] + "J" + state[x - cols + 1:x] + 'M' + state[x + 1:pos] + '.' + state[pos + 1:]
                pushingCan = True
        elif direction == 'L':
            if state[x - 1] == '.' or state[x - 1] == 'G':
                string = state[:x - 1] + 'JM.' + state[x + 2:]
                pushingCan = True
    elif state[x] == '.' or state[x] == 'G':
        if direction == 'D':
            string = state[:pos] + '.' + state[pos + 1:x] + 'M' + state[x + 1:]
            pushingCan = False
        elif direction == 'R':
            string = state[:pos] + '.M' + state[x + 1:]
            pushingCan = False
        elif direction == 'U':
            string = state[:x] + 'M' + state[x + 1:pos] + '.' + state[pos + 1:]
            pushingCan = False
        elif direction == 'L':
            string = state[:x] + 'M.' + state[pos + 1:]
            pushingCan = False
    return string
        # self.TreeOfStates.append(node.makeChild(string,tempPos[idx]))


for idx, c in enumerate(solution):
    if direction == c:
        glueSolution = glueSolution + "F"
        state = makeMobe(state,pos,direction)
        if temp == True and pushingCan == False:
            glueSolution = glueSolution + 'D'
            temp = pushingCan
        else:
            temp = pushingCan
    elif direction == "L" and c == 'U' or direction == "U" and c == 'R' or  direction == "R" and c == 'D' or  direction == "D" and c == 'L': #Turn Right
        direction = c
        state = makeMobe(state, pos, direction)
        if temp == True and pushingCan == False:
            glueSolution = glueSolution + 'D'
            temp = pushingCan
        else:
            temp = pushingCan
        glueSolution = glueSolution + 'R'
        glueSolution = glueSolution + "F"
    elif direction == "L" and c == 'D' or direction == "U" and c == 'L' or  direction == "R" and c == 'U' or  direction == "D" and c == 'R': #Turn Left
        direction = c
        state = makeMobe(state, pos, direction)
        if temp == True and pushingCan == False:
            glueSolution = glueSolution + 'D'
            temp = pushingCan
        else:
            temp = pushingCan
        glueSolution = glueSolution + 'L'
        glueSolution = glueSolution + "F"
    elif direction == "L" and c == 'R' or direction == "R" and c == 'L' or  direction == "U" and c == 'D' or  direction == "D" and c == 'U': #Turn Back
        direction = c
        state = makeMobe(state, pos, direction)
        if temp == True and pushingCan == False:
            glueSolution = glueSolution + 'D'
            temp = pushingCan
        else:
            temp = pushingCan
        glueSolution = glueSolution + 'RR'
        glueSolution = glueSolution + "F"
    if direction == 'L':
        pos = pos - 1
    elif direction == 'R':
        pos = pos + 1
    elif direction == 'U':
        pos = pos - cols
    elif direction == 'D':
        pos = pos + cols

print(len(glueSolution))
print(glueSolution)



#sokobanSolver.get_available_states()

