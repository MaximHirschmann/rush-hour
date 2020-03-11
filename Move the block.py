import pygame
import sys
import math
from random import randrange


class Game:
    #initializing
    def __init__(self, moves, board):
        self.listOfBlocks = board
        self.blocks = []
        self.board = [
            ['o', 'o', 'o', 'o', 'o', 'o'] ,
            ['o', 'o', 'o', 'o', 'o', 'o'] ,
            ['o', 'o', 'o', 'o', 'o', 'o'] ,
            ['o', 'o', 'o', 'o', 'o', 'o'] ,
            ['o', 'o', 'o', 'o', 'o', 'o'] ,
            ['o', 'o', 'o', 'o', 'o', 'o']
        ]
        self.red = 255,0,0
        self.green = 0,255,0
        self.blue = 0,0,255
        self.black = 0,0,0
        self.yellow = 255,255,0
        self.darkblue = 0,0,185
        self.darkred = 173,0,0
        self.size = int(100)
        self.tile_color1 = (220, 220, 220)
        self.tile_color2 = (100, 100, 100)
        self.boardSide = self.size * 6
        self.screen = pygame.display.set_mode((1000, 600))
        self.listOfSprites = []
        self.marked = []
        self.moves = 0
        self.min_moves = int(moves)
        self.button_next = pygame.Rect(880, 200, 100, 50)
        self.button_back = pygame.Rect(700, 200, 130, 50)
        self.last_move = [] # block , x, y

    def setupBoard(self):
        for i, val in enumerate(self.listOfBlocks):
            self.board[i//6][i%6] = val

    def endGame(self):
        return self.board[2][5] == "A"

    def click(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.button_next.collidepoint(pos):
                        print("Button")
                        nextGame()
                    elif self.button_back.collidepoint(pos):
                        block, x, y = self.last_move
                        self.doMove(block, (x, y), self.getCells(block))
                        self.moves -= 2
                        return None
                    elif pos[0] <= 600 and pos[1] <= 600:
                        ret = self.clickOnBoard(pos)
                        if ret != None:
                            self.moveBlock(ret[0], ret[1], ret[2])
                            return None

    def clickOnBoard(self, pos):
        if len(self.marked) == 0:
            x = pos[0] // 100
            y = pos[1] // 100
            print("Klick auf", x, y, self.board[y][x])
            if self.board[y][x] != "o":
                block = self.board[y][x]
                self.marked.append(block)
                self.setup()
            else:
                print("please click on a block")
        elif len(self.marked):
            x = pos[0] // 100
            y = pos[1] // 100
            block = self.marked.pop()
            if self.board[y][x] != "o":
                block = self.board[y][x]
                self.marked.append(block)
                self.setup()
            else:
                print("Klick2 auf", x, y, self.board[y][x])
                return block,x,y

    def moveBlock(self, block, x, y):
        print(block, x, y)
        # move describes the change of the y and x coordinate of the nearest cell of the block to the target cell
        move = [7,7]
        # list of all cells of the selected block
        cells = self.getCells(block)
        for i, j in cells:
            move_y = y-i
            move_x = x-j
            if abs(move_y) < abs(move[0]):
                move[0] = move_y
            if abs(move_x) < abs(move[1]):
                move[1] = move_x
        self.doMove(block, move, cells)
    
    def getCells(self, block):
        return [(i, j) for i in range(6) for j in range(6) if self.board[i][j] == block]

    def doMove(self, block, move, cells):
        if self.isLegal(block, move, cells):
            self.last_move = [block, -move[0], -move[1]]
            for i, j in cells:
                self.board[i][j] = 'o'
            for i, j in cells:
                self.board[i+move[0]][j+move[1]] = block
            self.moves += 1
            print("Zug durchgeführt")
        else:
            print("Nicht möglicher Zug")
    
    def isLegal(self, block, move, cells):
        # nicht in bewegbarer Reihe
        print("test ob reihe")
        horizontal = cells[0][0] == cells[1][0]
        if horizontal:
            if move[0] != 0:
                return False
        else:
            if move[1] != 0:
                return False
        print("Ist in einer Reihe")
        # außerhalb des boards
        # anderer Block zwischen oder auf den Postionen
        cells_after = [(i+move[0], j+move[1]) for i, j in cells]
        cells_combined = cells + cells_after
        if horizontal:
            row = cells[0][0]
            columns = [i[1] for i in cells_combined]
            min_column, max_column = min(columns), max(columns)
            if min_column < 0 or max_column > 5:
                return False
            for c in range(min_column, max_column+1):
                # all traversed cells
                if self.board[row][c] != block and self.board[row][c] != 'o':
                    return False 
        else:
            column = cells[0][1]
            rows = [i[0] for i in cells_combined]
            min_row, max_row = min(rows), max(rows)
            if min_row < 0 or max_row > 5:
                return False
            for r in range(min_row, max_row+1):
                # all traversed cells
                if self.board[r][column] != block and self.board[r][column] != 'o':
                    return False 
        return True

    def printBoard(self):
        for i in self.board:
            print(i)

    def setup(self):
        pygame.init()
        screen = self.screen
        screen.fill((255,255,255))
        count = 0
        factor = 4
        log = int(math.log(factor, 2))
        size = self.size//factor
        for i in range(6*4**(log-1)):
            for x in range(6*4*(log-1)):
                #check if current loop value is even
                if count % 2 == 0:
                    pygame.draw.rect(screen, self.tile_color1,[size*x,size*i,size,size])
                else:
                    pygame.draw.rect(screen, self.tile_color2,[size*x,size*i,size,size])
                count +=1
            count-=1
        pygame.draw.rect(screen,self.green,[500,200,100,100])

        for i in range(6):
            for j in range(6):
                if self.board[i][j] == "o":
                    continue
                block = self.board[i][j]
                color = self.blue
                if block == "A":
                    color = self.red
                if block in self.marked:
                    if color == self.blue:
                        color = self.darkblue
                    else:
                        color = self.darkred
                hor = 5
                ver = 5
                height = 90
                length = 90
                if i+1 < 6:
                    if self.board[i+1][j] == block:
                        height += 5
                if i-1 >= 0:
                    if self.board[i-1][j] == block:
                        height += 5
                        ver -= 5
                if j+1 < 6:
                    if self.board[i][j+1] == block:
                        length += 5
                if j-1 >= 0:
                    if self.board[i][j-1] == block:
                        length += 5
                        hor -= 5
                image = pygame.Surface((length,height))
                pygame.draw.rect(image, color, (0,0,length, height))
                
                screen.blit(image, (j*self.size+hor, i*self.size+ver))

        # number of moves
        font = pygame.font.SysFont('Arial Bold', 50)
        movessurface = font.render(str(self.moves)+" / "+str(self.min_moves), False, self.black)
        screen.blit(movessurface,(760,70))

        pygame.draw.rect(screen, [153, 51, 204], self.button_next)
        movessurface = font.render("Next", False, self.black)
        screen.blit(movessurface, (892, 210))

        pygame.draw.rect(screen, [153, 51, 204], self.button_back)
        movessurface = font.render("Zurück", False, self.black)
        screen.blit(movessurface, (706, 210))

        pygame.display.update()
        
    def play(self):
        self.setupBoard()
        self.setup()
        while self.endGame() != 1:
            self.printBoard()
            self.click()
            self.setup()
        nextGame()

with open("C://Users//Maxim//Documents//GitHub//rush-hour//data.txt", "r") as f:
    games = [line.replace("\n", "").split(" ") for line in f.readlines()]

def nextGame():
    rand = randrange(len(games))
    min_number_of_moves = games[rand][0]
    board = games[rand][1]
    RetteDenBlock = Game(min_number_of_moves, board)
    RetteDenBlock.play()

#main
if __name__ == "__main__":
    nextGame()

# TODO beim falsch auswählen neu markieren
# kachelmuster kleiner
# anzahl an Zügen zählen