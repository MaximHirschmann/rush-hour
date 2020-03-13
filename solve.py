import copy
import sys
from time import time

def stringToBoard(s):
    board = [
        ['o', 'o', 'o', 'o', 'o', 'o'] ,
        ['o', 'o', 'o', 'o', 'o', 'o'] ,
        ['o', 'o', 'o', 'o', 'o', 'o'] ,
        ['o', 'o', 'o', 'o', 'o', 'o'] ,
        ['o', 'o', 'o', 'o', 'o', 'o'] ,
        ['o', 'o', 'o', 'o', 'o', 'o']
    ]
    for i, val in enumerate(s):
        board[i//6][i%6] = val
    return board

def boardToString(board):
    return ''.join(''.join(i) for i in board)

def printBoard(board):
    for i in board:
        print(i)

def moveBlock(board, x1, y1, x2, y2):
    block = board[y1][x1]
    cells = []
    move = [7, 7]
    for x in range(6):
        for y in range(6):
            if board[y][x] == block:
                cells.append((x, y))
    for x, y in cells:
        move_x = x2-x
        move_y = y2-y
        if abs(move_x) < abs(move[0]):
            move[0] = move_x
        if abs(move_y) < abs(move[1]):
            move[1] = move_y
    for x, y in cells:
        board[y][x] = 'o'
    for x, y in cells:
        board[y+move[1]][x+move[0]] = block
    return board
    
def isLegal(board, x1, y1, x2, y2):
    if x1-x2 != 0 and y1-y2 != 0:
        return False
    if x1 == x2 and y1 == y2:
        return False
    if board[y1][x1] == "o":
        return False
    if board[y1][x1] == board[y2][x2]:
        return False
    block = board[y1][x1]
    # horizontal
    if x1-x2 != 0:
        isHorizontalBlock = False
        if x1 > 0:
            if board[y1][x1-1] == block:
                isHorizontalBlock = True
        if x1 < 5:
            if board[y1][x1+1] == block:
                isHorizontalBlock = True
        if not isHorizontalBlock:
            return False
        if x1 < x2:
            for i in range(x1+1, x2+1):
                if board[y1][i] != 'o' and board[y1][i] != block:
                    return False
        else:
            for i in range(x2, x1):
                if board[y1][i] != 'o' and board[y1][i] != block:
                    return False
    # vertical
    else:
        isVerticalBlock = False
        if y1 > 0:
            if board[y1-1][x1] == block:
                isVerticalBlock = True
        if y1 < 5:
            if board[y1+1][x1] == block:
                isVerticalBlock = True
        if not isVerticalBlock:
            return False
        
        if y1 < y2:
            for i in range(y1+1, y2+1):
                if board[i][x1] != 'o' and board[i][x1] != block:
                    return False
        else:
            for i in range(y2, y1):
                if board[i][x1] != 'o' and board[i][x1] != block:
                    return False
    return True

def nextDepth(boards):
    new = []
    for i in boards:
        board = i[0]
        for x1 in range(6):
            for y1 in range(6):
                for x2 in range(6):
                    for y2 in range(6):
                        if isLegal(board, x1, y1, x2, y2):
                            newBoard = moveBlock(copy.deepcopy(board), x1, y1, x2, y2)
                            s = boardToString(newBoard)
                            if s not in save:
                                save[s] = 1
                                if newBoard[2][5] == "A":
                                    return (newBoard, board)
                                new.append((newBoard, board))
    return new

def solve(conf):
    global save
    save = {conf:0}
    board = stringToBoard(conf)
    allBoards = [[(board, None)]]
    depth = 1
    while True:
        res = nextDepth(allBoards[depth-1])
        allBoards.append(res)
        if type(res) == tuple:
            path = [res[0]]
            last = res[1]
            while depth > 0:
                depth -= 1
                for i in allBoards[depth]:
                    if last == i[0]:
                        path.append(i[0])
                        last = i[1]
            path = path[::-1]
            for depth, i in enumerate(path):
                print(depth)
                printBoard(i)
            return path
        depth += 1

if __name__ == "__main__":
    start = time()
    conf = "GBBoLoGHIoLMGHIAAMCCCKoMooJKDDEEJFFo" # 51      3,3s
    #conf = "ooooBoooooBoAAooBooooooooooooooooooo" # 2
    #conf = "ooEBBBooEooFooEAAFoCCCDDoooooooooooo" # 4
    solve(conf)
    print(time()-start, "s")
