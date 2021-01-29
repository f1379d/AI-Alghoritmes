# Initialize Maze and walls
# Also assigns Heuristic to every node
def Maze_init(x, y, goal, walls):
    Maze = [[None]*y for i in range(x)]
    blocked = []
    parent = []
    cost = 0
    fx = 0
    for i in range(x):
        for j in range(y):
            h_manhattan = abs(goal[0] - i) + abs(goal[1] - j)
            Maze[i][j] = [i, j, parent, h_manhattan, cost, fx]
    for i in walls:
        blocked.append([Maze[i[0][0]][i[0][1]], Maze[i[1][0]][i[1][1]]])

    return Maze, blocked

# Get successor


def Successor(Maze, node, blocked):
    succ_nodes = []
    possible = []
    # for i in Maze:
    #     for j in i:
    #         if j[0] == node[0] and (j[1] == node[1]-1 or j[1] == node[1]-1):
    #             temp.append(j)
    #         if j[1] == node[1] and (j[0] == node[0]-1 or j[0] == node[0]-1):
    #             temp.append(j)
    # for i in temp:
    #     if not ([node, i] in blocked or [i, node] in blocked):
    #         succ_nodes.append(i)
    # return succ_nodes
    if node[0] == 0 and node[1] == 0:
        possible.append(Maze[node[0]][node[1]+1])
        possible.append(Maze[node[0]+1][node[1]])
    elif node[0] == len(Maze)-1 and node[1] == len(Maze[0])-1:
        possible.append(Maze[node[0]][node[1]-1])
        possible.append(Maze[node[0]-1][node[1]])
    elif node[0] == len(Maze)-1 and node[1] == 0:
        possible.append(Maze[node[0]][node[1]+1])
        possible.append(Maze[node[0]-1][node[1]])
    elif node[0] == 0 and node[1] == len(Maze[0])-1:
        possible.append(Maze[node[0]][node[1]-1])
        possible.append(Maze[node[0]+1][node[1]])
    elif node[0] == 0:
        possible.append(Maze[node[0]][node[1]+1])
        possible.append(Maze[node[0]+1][node[1]])
        possible.append(Maze[node[0]][node[1]-1])
    elif node[0] == len(Maze)-1:
        possible.append(Maze[node[0]][node[1]-1])
        possible.append(Maze[node[0]-1][node[1]])
        possible.append(Maze[node[0]][node[1]+1])
    elif node[1] == len(Maze[0])-1:
        possible.append(Maze[node[0]][node[1]-1])
        possible.append(Maze[node[0]-1][node[1]])
        possible.append(Maze[node[0]+1][node[1]])
    elif node[1] == 0:
        possible.append(Maze[node[0]][node[1]+1])
        possible.append(Maze[node[0]-1][node[1]])
        possible.append(Maze[node[0]+1][node[1]])
    else:
        possible.append(Maze[node[0]][node[1]+1])
        possible.append(Maze[node[0]-1][node[1]])
        possible.append(Maze[node[0]+1][node[1]])
        possible.append(Maze[node[0]][node[1]-1])

    for i in possible:
        if not ([node, i] in blocked or [i, node] in blocked):
            succ_nodes.append(i)
    return succ_nodes


def A_star(maze, blocked, start, goal):
    fringe = []
    closed = []
    current = start
    reached_goal = []
    path = []
    fringe.append(current)
    while True:
        if fringe == []:
            break
        current = fringe[0]
        for i in fringe:
            if i[5] <= current[5]:
                current = i
        closed.append([current[0], current[1]])
        if current in fringe:
            fringe.remove(current)
        if current[0] == goal[0] and current[1] == goal[1]:
            reached_goal = current
            break
        nodes = Successor(maze, current, blocked)

        for i in nodes:
            if [i[0], i[1]] in closed:
                continue
            elif i not in fringe:
                i[2] = [current[0], current[1]]
                i[4] = current[4] + 1
                i[5] = i[4] + i[3]
                maze[i[0]][i[1]] = i
                fringe.append(i)
            elif i[0] in [j[0] for j in fringe] and i[1] in [j[1] for j in fringe]:
                pre = fringe.pop(fringe.index(i))
                i[2] = [current[0], current[1]]
                i[4] = current[4] + 1
                i[5] = i[4] + i[3]
                if pre[4] > i[4]:
                    maze[i[0]][i[1]] = i
                    fringe.append(i)
                else:
                    fringe.append(pre)

    if reached_goal == []:
        print("No Path found")
        return False
    else:
        path.append([reached_goal[0], reached_goal[1]])
        closed.reverse()
        maze.reverse()
        for i in closed:
            if i == reached_goal[2]:
                path.append(i)
                for j in maze:
                    if j[0][0] < i[0]:
                        break
                    for k in j:
                        if i[0] == k[0] and i[1] == k[1]:
                            reached_goal = k
                            break
        path.reverse()
        direction = []
        for i in range(len(path)):
            if i == 0:
                direction.append("start")
            elif path[i][0] == path[i-1][0] - 1:
                direction.append("up")
            elif path[i][0] == path[i-1][0] + 1:
                direction.append("down")
            elif path[i][1] == path[i-1][1] - 1:
                direction.append("left")
            elif path[i][1] == path[i-1][1] + 1:
                direction.append("right")
            if i == len(path) - 1:
                direction.append("goal")
        for i in path:
            if direction == []:
                direction.append
            if not i == closed[0]:
                print("{} => ".format(i), end="")
            else:
                print("{} = Goal ".format(i), end="\n\n")
        print(direction)
        return True


def main():

    # INPUT
    walls = []
    goal = [0, 0]
    start = [0, 0]
    x = int(input("please enter number of rows => "))
    y = int(input("please enter number of columns => "))
    start[0] = int(input("please enter the row number of Starting state => "))
    start[1] = int(
        input("please enter the column number of Starting state => "))
    goal[0] = int(input("please enter the row number of Goal state => "))
    goal[1] = int(input("please enter the column number of Goal state => "))
    sure = input(
        "Before you continue, make sure you have added the walls position in walls.txt file in CWP")

    # Read walls
    f = open("walls1.txt", "r")
    Lines = f.readlines()
    for line in Lines:
        wall_loc = line.strip().split(" | ")
        wall_loc[0] = wall_loc[0].split(',')
        wall_loc[1] = wall_loc[1].split(',')
        wall_loc[0][0] = int(wall_loc[0][0])
        wall_loc[0][1] = int(wall_loc[0][1])
        wall_loc[1][0] = int(wall_loc[1][0])
        wall_loc[1][1] = int(wall_loc[1][1])
        walls.append(wall_loc)
    f.close()
    # Get Maze
    init = Maze_init(x, y, goal, walls)
    maze = init[0]
    block = init[1]
    A_star(maze, block, [start[0], start[1], [], 0, 0, 0], goal)


if __name__ == '__main__':
    main()
