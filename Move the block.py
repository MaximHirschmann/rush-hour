import pygame
import sys
import math

class Game:
    #initializing
    def __init__(self):
        self.listOfBlocks = "oooooFoBBBoFooDAAGooDEoGoooECCoooEoo"
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
        self.screen = pygame.display.set_mode((self.boardSide,self.boardSide))
        self.listOfSprites = []
        self.marked = []

    def setupBoard(self):
        for i, val in enumerate(self.listOfBlocks):
            self.board[i//6][i%6] = val

    def endGame(self):
        return self.board[2][5] == "A"

    def movement(self):
        complete = False
        marker = 0
        while complete == False:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if marker == 0:
                        marker = 1
                        origin = pygame.mouse.get_pos()
                        origin_x = origin[0] // 100
                        origin_y = origin[1] // 100
                        print("Klick auf", origin_x, origin_y, self.board[origin_y][origin_x])
                        if self.board[origin_y][origin_x] != "o":
                            block = self.board[origin_y][origin_x]
                            self.marked.append(block)
                            self.updateBlocks()
                        else:
                            marker = 0
                            print("please click on a block")
                    elif marker == 1:
                        newPos = pygame.mouse.get_pos()
                        x = newPos[0] // 100
                        y = newPos[1] // 100
                        print("Klick2 auf", x, y, self.board[y][x])
                        self.marked.pop()
                        return block,x,y


    def moveCar(self):
        block, x, y = self.movement()
        # move describes the change of the y and x coordinate of the nearest cell of the block to the target cell
        move = [7,7]
        # list of all cells of the selected block
        cells = []
        for i in range(6):
            for j in range(6):
                if self.board[i][j] == block:
                    cells.append((i, j))
                    move_y = y-i
                    move_x = x-j
                    if abs(move_y) < abs(move[0]):
                        move[0] = move_y
                    if abs(move_x) < abs(move[1]):
                        move[1] = move_x
        if self.isLegal(block, move, cells):
            for i, j in cells:
                self.board[i][j] = 'o'
            for i, j in cells:
                self.board[i+move[0]][j+move[1]] = block
            print("Zug durchgeführt")
        else:
            print("Nicht möglicher Zug")
    
    def isLegal(self, block, move, cells):
        # nicht in bewegbarer Reihe
        horizontal = cells[0][0] == cells[1][0]
        if horizontal:
            if move[0] != 0:
                return False
        else:
            if move[1] != 0:
                return False
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
            print(min_row, max_row)
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
        for i in range(6*4**log):
            for x in range(6*4*log):
                #check if current loop value is even
                if count % 2 == 0:
                    pygame.draw.rect(screen, self.tile_color1,[size*x,size*i,size,size])
                else:
                    pygame.draw.rect(screen, self.tile_color2,[size*x,size*i,size,size])
                count +=1
            count-=1
        pygame.draw.rect(screen,self.green,[500,200,100,100])
        self.updateBlocks()

    def updateBlocks(self):
        screen = self.screen
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
        pygame.display.update()

    def play(self):
        self.setupBoard()
        self.setup()
        while self.endGame() != 1:
            self.printBoard()
            self.moveCar()
            self.setup()
            
#main
if __name__ == "__main__":
    RetteDenBlock = Game()
    RetteDenBlock.play()

# TODO beim falsch auswählen neu markieren
# kachelmuster kleiner
# anzahl an Zügen zählen