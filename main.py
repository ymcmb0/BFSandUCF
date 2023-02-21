from os import system, name


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


class Queue:
    list__ = []

    def enqueue(self, item):
        self.list__.append(item)

    def dequeue(self):
        self.list__.pop(0)  # Popping 1st element

    def display(self):
        print(self.list__)

    def front(self):
        return (self.list__[0])

    def empty(self):
        if (len(self.list__) == 0):
            return True
        else:
            return False

    def clear(self):
        if (not self.empty()):
            while (not self.empty()):
                self.dequeue()


class Stack:
    list__ = []

    def push(self, item):
        self.list__.insert(0, item)  # Inserting in top position

    def pop(self):
        self.list__.pop(0)  # Popping the recent element

    def display(self):
        print(self.list__)

    def top(self):
        return self.list__[0]

    def empty(self):
        if (len(self.list__) == 0):
            return True
        else:
            return False

    def clear(self):
        if (not self.empty()):
            while (not self.empty()):
                self.pop()

    def getStackItemsInList(self):
        return self.list__

    def remove(self, value):
        self.list__.pop(self.list__.index(value))


gridSize = 0
grid = []
vis = []
level = []
helpingMarkLevel = []
dist = []
path = []
exlist = []
moves = []
movesCost = {}
backTrackPath = []
movCosts = [2, 2, 3]  # Up, Right, Right Diagonal Costs
resultantStack = Stack()
resultantQueue = Queue()


def prRed(skk): print("\033[91m {}\033[00m".format(skk), end="")


def prGreen(skk): print("\033[92m {}\033[00m".format(skk), end="")


def prYellow(skk): print("\033[93m {}\033[00m".format(skk), end="")


def prLightPurple(skk): print("\033[94m {}\033[00m".format(skk), end="")


def prPurple(skk): print("\033[95m {}\033[00m".format(skk), end="")


def prCyan(skk): print("\033[96m {}\033[00m".format(skk), end="")


def prLightGray(skk): print("\033[97m {}\033[00m".format(skk), end="")


def prBlack(skk): print("\033[98m {}\033[00m".format(skk), end="")


def displayGrid():
    i = 15
    j = 0
    grid.reverse()
    for row in grid:
        printRow = ""
        if (i < 10):
            print('\n' + str(i) + ":  ", end="")
        else:
            print('\n' + str(i) + ": ", end="")

        for char in row:
            if (char == 'S'):
                prGreen('S ')
            elif (char == 'E'):
                prRed('E ')
            elif (char == '*'):
                prCyan('* ')
            elif (char == '#'):
                prYellow('# ')
            else:
                prLightGray(char + ' ')
        i -= 1


def minCostNode(pathStack):  # g(n) function gives minimum cost
    cost = []
    treeCoordinates = []
    while (not pathStack.empty()):
        treeCoordinates.append(pathStack.top())
        pathStack.pop()
    treeCoordinates.reverse()
    for node in treeCoordinates:
        cost.append(movesCost[tuple(node)])
    mincost = min(cost)
    for coordinates in movesCost.keys():
        if (movesCost[coordinates] == mincost):
            if coordinates in exlist:
                continue
            for node in treeCoordinates:
                pathStack.push(node)
            return coordinates[0], coordinates[1]


def isValid(srcX, srcY):
    if (srcX < 0 or srcX >= gridSize or srcY < 0 or srcY >= gridSize):
        return False
    if (vis[srcX][srcY] == True):
        return False
    return True


def extractDataFromText():
    f = open('Grid.txt', 'r')
    for line in f.readlines():
        grid.append(list(line.strip()))
    f.close()

    return grid


def initializeVariables():
    grid = extractDataFromText()
    gridSize = len(grid)
    vis = [[False for i in range(gridSize)] for j in range(gridSize)]
    backTrackPath = [[[0, 0] for i in range(gridSize)] for j in range(gridSize)]
    dist = [[0 for i in range(gridSize)] for j in range(gridSize)]
    for i in range(gridSize):
        for j in range(gridSize):
            if (grid[i][j] == '1'):
                vis[i][j] = True
    return grid, gridSize, vis, backTrackPath, dist


def BFS(src, end):
    endFound = False
    srcX = src['x'] - 1
    srcY = src['y'] - 1
    endX = end['x'] - 1
    endY = end['y'] - 1
    if (isValid(srcX, srcY) and isValid(endX, endY)):
        resultantQueue.enqueue([srcX, srcY])
        vis[srcX][srcY] = True
        backTrackPath[srcX][srcY] = [srcX, srcY]
        while (not resultantQueue.empty()):
            currX = resultantQueue.front()[0]
            currY = resultantQueue.front()[1]
            resultantQueue.dequeue()
            if (currX == endX and currY == endY):
                endFound = True
                break
            for i in range(3):
                newX = currX
                newY = currY
                if (i == 0 and isValid(currX, currY + 1)):  # Up Movement
                    newY += 1
                elif (i == 1 and isValid(currX + 1, currY)):  # Right Movement
                    newX += 1
                elif (i == 2 and isValid(currX + 1, currY + 1)):  # Right Diagonal Movement
                    newX += 1
                    newY += 1
                if (currX != newX or currY != newY):
                    grid[newX][newY] = "#"
                    vis[newX][newY] = 1
                    backTrackPath[newX][newY] = [currX, currY]
                    # print("Parent: " + str((backTrackPath[currX][currY][0]+1, backTrackPath[currX][currY][1]+1)) + " backTrackPath: " + str([currX+1, currY+1]))
                    dist[newX][newY] = dist[currX][currY] + movCosts[i]
                    resultantQueue.enqueue([newX, newY])
        else:
            print("Vertices are out of bounds!")

        resultantQueue.clear()
        if (endFound):
            resultantQueue.enqueue([endX, endY])
            currX = resultantQueue.front()[0]
            currY = resultantQueue.front()[1]
            while (currX != srcX and currY != srcY):
                currX = resultantQueue.front()[0]
                currY = resultantQueue.front()[1]
                prevX = backTrackPath[currX][currY][0]
                prevY = backTrackPath[currX][currY][1]
                if (not resultantQueue.empty()):
                    resultantQueue.dequeue()
                if (currX != srcX and currY != srcY):
                    grid[prevX][prevY] = '*'
                    path.append((prevX, prevY))
                    resultantQueue.enqueue([prevX, prevY])
                if (prevX + 1 == currX and prevY == currY):
                    moves.append("🡱")
                elif (prevX == currX and prevY + 1 == currY):
                    moves.append("🡲")
                elif (prevX + 1 == currX and prevY + 1 == currY):
                    moves.append("🡵")
        else:
            print("End not found!")
        grid[srcX][srcY] = "S"
        grid[endX][endY] = "E"
    else:
        print("User Selected Obstactle!")
    return endFound, grid


def DFS(src, end):
    endFound = False
    srcX = src['x'] - 1
    srcY = src['y'] - 1
    endX = end['x'] - 1
    endY = end['y'] - 1
    if (isValid(srcX, srcY) and isValid(endX, endY)):
        resultantStack.push([srcX, srcY])
        vis[srcX][srcY] = True
        backTrackPath[srcX][srcY] = [srcX, srcY]
        while (not resultantStack.empty()):
            currX = resultantStack.top()[0]
            currY = resultantStack.top()[1]
            resultantStack.pop()
            if (currX == endX and currY == endY):
                endFound = True
                break
            for i in range(3):
                newX = currX
                newY = currY
                if (i == 0 and isValid(currX, currY + 1)):  # Up Movement
                    newY += 1
                elif (i == 1 and isValid(currX + 1, currY)):  # Right Movement
                    newX += 1
                elif (i == 2 and isValid(currX + 1, currY + 1)):  # Right Diagonal Movement
                    newX += 1
                    newY += 1
                if (currX != newX or currY != newY):
                    grid[newX][newY] = "#"
                    vis[newX][newY] = 1
                    backTrackPath[newX][newY] = [currX, currY]
                    dist[newX][newY] = dist[currX][currY] + movCosts[i]
                    resultantStack.push([newX, newY])

        else:
            print("Vertices are out of bounds!")

        resultantStack.clear()
        if (endFound):
            resultantStack.push([endX, endY])
            while (not resultantStack.empty()):
                currX = resultantStack.top()[0]
                currY = resultantStack.top()[1]
                prevX = backTrackPath[currX][currY][0]
                prevY = backTrackPath[currX][currY][1]
                resultantStack.pop()
                if (prevX != srcX and prevY != srcY):
                    grid[prevX][prevY] = '*'
                    path.append((prevX, prevY))
                    resultantStack.push([prevX, prevY])
                if (prevX + 1 == currX and prevY == currY):
                    moves.append("🡱")
                elif (prevX == currX and prevY + 1 == currY):
                    moves.append("🡲")
                elif (prevX + 1 == currX and prevY + 1 == currY):
                    moves.append("🡵")
                else:
                    break
        else:
            print("End not found!")
        grid[srcX][srcY] = "S"
        grid[endX][endY] = "E"
    else:
        print("User Selected Obstactle!")
    return endFound, grid


def UCS(src, end):
    endFound = False
    srcX = src['x'] - 1
    srcY = src['y'] - 1
    endX = end['x'] - 1
    endY = end['y'] - 1
    if (isValid(srcX, srcY) and isValid(endX, endY)):
        resultantStack.push([srcX, srcY])
        vis[srcX][srcY] = True
        dist[srcX][srcY] = 0
        movesCost[(srcX, srcY)] = 0
        while (not resultantStack.empty()):
            currX, currY = minCostNode(resultantStack)
            resultantStack.remove([currX, currY])
            exlist.append((currX, currY))
            if (currX == endX and currY == endY):
                endFound = True
                break
            for i in range(3):
                newX = currX
                newY = currY
                if (i == 0 and isValid(currX, currY + 1)):  # Up Movement
                    newY += 1
                elif (i == 1 and isValid(currX + 1, currY)):  # Right Movement
                    newX += 1
                elif (i == 2 and isValid(currX + 1, currY + 1)):  # Right Diagonal Movement
                    newX += 1
                    newY += 1
                if (currX != newX or currY != newY):
                    grid[newX][newY] = "#"
                    vis[newX][newY] = 1
                    backTrackPath[newX][newY] = [currX, currY]
                    dist[newX][newY] = dist[currX][currY] + movCosts[i]
                    movesCost[(newX, newY)] = dist[newX][newY]
                    resultantStack.push([newX, newY])
        else:
            print("Vertices are out of bounds!")
            restartProgram()

        resultantStack.clear()
        if (endFound):
            resultantStack.push([endX, endY])
            while (not resultantStack.empty()):
                currX = resultantStack.top()[0]
                currY = resultantStack.top()[1]
                prevX = backTrackPath[currX][currY][0]
                prevY = backTrackPath[currX][currY][1]
                resultantStack.pop()
                if (prevX != srcX and prevY != srcY):
                    grid[prevX][prevY] = '*'
                    path.append((prevX, prevY))
                    resultantStack.push([prevX, prevY])
                if (prevX + 1 == currX and prevY == currY):
                    moves.append("🡱")
                elif (prevX == currX and prevY + 1 == currY):
                    moves.append("🡲")
                elif (prevX + 1 == currX and prevY + 1 == currY):
                    moves.append("🡵")
                else:
                    break
        else:
            print("End not found!")
        grid[srcX][srcY] = "S"
        grid[endX][endY] = "E"
    else:
        print("User Selected Obstactle!")
    return endFound, grid


def IDDFS(src, end, limit):
    global grid
    endFound = False
    srcX = src['x'] - 1
    srcY = src['y'] - 1
    endX = end['x'] - 1
    endY = end['y'] - 1
    if (isValid(srcX, srcY) and isValid(endX, endY)):
        resultantStack.push([srcX, srcY])
        vis[srcX][srcY] = True
        helpingMarkLevel.append((srcX, srcY))  # For DFS
        level.append([(srcX, srcY), 0])  # For BFS
        while (not resultantStack.empty()):
            currX = resultantStack.top()[0]
            currY = resultantStack.top()[1]
            resultantStack.pop()
            exlist.append((currX, currY))
            if (currX == endX and currY == endY):
                endFound = True
                break
            dfsTraversalLevel = int(helpingMarkLevel.index((currX, currY)))
            if (level[dfsTraversalLevel][1] + 1) <= limit:
                for i in range(3):
                    newX = currX
                    newY = currY
                    if (i == 0 and isValid(currX, currY + 1)):  # Up Movement
                        newY += 1
                    elif (i == 1 and isValid(currX + 1, currY)):  # Right Movement
                        newX += 1
                    elif (i == 2 and isValid(currX + 1, currY + 1)):  # Right Diagonal Movement
                        newX += 1
                        newY += 1
                    if (currX != newX or currY != newY):
                        grid[newX][newY] = "#"
                        vis[newX][newY] = 1
                        backTrackPath[newX][newY] = [currX, currY]
                        dist[newX][newY] = dist[currX][currY] + movCosts[i]
                        level.append([(newX, newY), level[dfsTraversalLevel][1] + 1])
                        helpingMarkLevel.append((newX, newY))
                        resultantStack.push([newX, newY])
        else:
            print("Vertices are out of bounds!")

        resultantStack.clear()
        resultantStack.push([endX, endY])
        while (not resultantStack.empty()):
            currX = resultantStack.top()[0]
            currY = resultantStack.top()[1]
            prevX = backTrackPath[currX][currY][0]
            prevY = backTrackPath[currX][currY][1]
            resultantStack.pop()
            if (prevX != srcX and prevY != srcY):
                grid[prevX][prevY] = '*'
                path.append((prevX, prevY))
                resultantStack.push([prevX, prevY])
            if (prevX + 1 == currX and prevY == currY):
                moves.append("🡱")
            elif (prevX == currX and prevY + 1 == currY):
                moves.append("🡲")
            elif (prevX + 1 == currX and prevY + 1 == currY):
                moves.append("🡵")
            else:
                break
        grid[srcX][srcY] = "S"
        grid[endX][endY] = "E"
        if (not endFound):
            print("Goal not reached!")
    else:
        print("User Selected Obstactle!")
    return endFound, grid


def resetValues():
    exlist.clear()
    path.clear()
    resultantStack.clear()
    backTrackPath.clear()
    dist.clear()
    vis.clear()
    grid.clear()
    moves.clear()
    movesCost.clear()
    return exlist, path, resultantStack, backTrackPath, dist, vis, grid, moves, movesCost


def restartProgram():
    global exlist, path, resultantStack, backTrackPath, dist, vis, grid, moves, movesCost, gridSize
    exlist, path, resultantStack, backTrackPath, dist, vis, grid, moves, movesCost = resetValues()
    main()


def showResults(end):
    path.reverse()
    moves.reverse()
    print("Path: ", end="")
    for coordinates in path:
        print("[" + str((coordinates[0] + 1, coordinates[1] + 1)) + "], ", end="")
    print("\nMoves: " + str(moves))
    print("Total Cost: " + str(dist[end['x'] - 1][end['y'] - 1]))
    displayGrid()


def isInputCorrect(input, expectedOutput):
    for output in expectedOutput:
        if (input == output):
            return True
    return False


def showMenu():
    prYellow("\n1. Breadth First Search\n")
    prGreen("2. Depth First Search\n")
    prPurple("3. Uniform Cost Search\n")
    prCyan("4. Iterative Deepening Search\n")
    opt = int(input("Enter Option: "))
    if (isInputCorrect(opt, [1, 2, 3, 4])):
        return opt
    else:
        print("Invalid Input!")
        clear()
        showMenu()


def main():
    endFound = False
    global exlist, path, resultantStack, backTrackPath, dist, vis, grid, moves, movesCost, gridSize
    opt = showMenu()
    grid, gridSize, vis, backTrackPath, dist = initializeVariables()
    src = {'x': 1, 'y': 3}
    end = {'x': 15, 'y': 15}
    src['x'] = int(input("Enter X-Coordinates for Source Node: "))
    src['y'] = int(input("Enter Y-Coordinates for Source Node: "))
    end['x'] = int(input("Enter X-Coordinates for End Node: "))
    end['y'] = int(input("Enter Y-Coordinates for End Node: "))
    if (opt == 1):
        endFound, grid = BFS(src, end)
    elif (opt == 2):
        endFound, grid = DFS(src, end)
    elif (opt == 3):
        endFound, grid = UCS(src, end)
    elif (opt == 4):
        maxLimit = int(input("Enter MaxLimit: "))
        for limit in range(maxLimit):
            print("Level: " + str(limit + 1))
            endFound, grid = IDDFS(src, end, limit + 1)
            if (endFound):
                break
            else:
                exlist, path, resultantStack, backTrackPath, dist, vis, grid, moves, movesCost = resetValues()
                grid, gridSize, vis, backTrackPath, dist = initializeVariables()
    if (endFound):
        print("End Reached!")
        showResults(end)
        restartProgram()
    else:
        print("End Not Reached!")
        exlist, path, resultantStack, backTrackPath, dist, vis, grid, moves, movesCost = resetValues()
        grid, gridSize, vis, backTrackPath, dist = initializeVariables()
    conclusionQuestion = input("\nDo you want to exit the program?(Enter 'y' for yes or 'n' for no)")
    if (isInputCorrect(conclusionQuestion, ['y', 'n'])):
        if (conclusionQuestion == 'y'):
            exit(0)
        else:
            clear()
            restartProgram()


main()
