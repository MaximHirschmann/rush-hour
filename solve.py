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

def getCells(board, block):
    return [(x,y) for x in range(6) for y in range(6) if board[y][x] == block]

def moveBlock(board, x1, y1, x2, y2):
    block = board[y1][x1]
    cells = getCells(board, block)
    move = [7, 7]
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
    if board[y1][x1] == board[y2][x2]:
        return False
    block = board[y1][x1]
    # horizontal
    if x1 != x2:
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
    for i, val in enumerate(boards):
        board = val[0]
        blocks = {"o":1}
        for x1 in range(6):
            for y1 in range(6):
                if board[y1][x1] not in blocks:
                    blocks[board[y1][x1]] = 1
                    for x2 in range(6):
                        y2 = y1
                        if isLegal(board, x1, y1, x2, y2):
                            newBoard = moveBlock(copy.deepcopy(board), x1, y1, x2, y2)
                            s = boardToString(newBoard)
                            if s not in save:
                                save[s] = 1
                                if newBoard[2][5] == "A":
                                    return (newBoard, i)
                                new.append((newBoard, i))
                    for y2 in range(6):
                        x2 = x1
                        if isLegal(board, x1, y1, x2, y2):
                            newBoard = moveBlock(copy.deepcopy(board), x1, y1, x2, y2)
                            s = boardToString(newBoard)
                            if s not in save:
                                save[s] = 1
                                if newBoard[2][5] == "A":
                                    return (newBoard, i)
                                new.append((newBoard, i))
    return new

def getMove(board1, board2):
    block = ""
    for y in range(6):
        for x in range(6):
            if board1[y][x] != board2[y][x]:
                if board1[y][x] != "o":
                    block = board1[y][x]
                else:
                    block = board2[y][x]
    cells1 = getCells(board1, block)
    cells2 = getCells(board2, block)
    move_x = sum(cells2[pos][0] - cells1[pos][0] for pos in range(len(cells1)))//len(cells1)
    move_y = sum(cells2[pos][1] - cells1[pos][1] for pos in range(len(cells1)))//len(cells1)
    return (block, move_x, move_y)

def solve(conf):
    start = time()
    global save
    save = {conf:0}
    board = stringToBoard(conf)
    allBoards = [[(board, 0, (0,2,0,2))]]
    depth = 1
    for _ in range(52):
        res = nextDepth(allBoards[depth-1])
        allBoards.append(res)
        if type(res) == tuple:
            last_board = res[0]
            last_pos = res[1]
            moves_path = []
            while depth > 0:
                depth -= 1
                new = allBoards[depth][last_pos]
                moves_path.append(getMove(new[0], last_board))
                last_board = new[0]
                last_pos = new[1]
            moves_path = moves_path[::-1]
            print("Solution found in ", time()-start, "s")
            return moves_path
        depth += 1

if __name__ == "__main__":
    conf = "GBBoLoGHIoLMGHIAAMCCCKoMooJKDDEEJFFo" # 51      1,4s
    #conf = "ooooBoooooBoAAooBooooooooooooooooooo" # 2
    #conf = "ooEBBBooEooFooEAAFoCCCDDoooooooooooo" # 4
    solve(conf)
