import pygame
import sys
import math
from random import randrange
import copy
import solve
import os

class Game:
    #initializing
    def __init__(self, moves, board, difficulty):
        self.listOfBlocks = board   # string of the initial board configuration
        self.blocks = []
        self.board = [
            ['o', 'o', 'o', 'o', 'o', 'o'] ,
            ['o', 'o', 'o', 'o', 'o', 'o'] ,
            ['o', 'o', 'o', 'o', 'o', 'o'] ,
            ['o', 'o', 'o', 'o', 'o', 'o'] ,
            ['o', 'o', 'o', 'o', 'o', 'o'] ,
            ['o', 'o', 'o', 'o', 'o', 'o']
        ]
        # colors
        self.color_blocks = 106, 141, 115
        self.color_blocks_selected = 86, 121, 95
        self.color_start_block = 240, 101, 67
        self.color_start_block_selected = 211, 54, 48
        self.color_tile1 = 255, 252, 232
        self.color_tile2 = 62, 54, 63
        self.color_tile_finish = 76, 131, 85
        self.color_button = 106, 141, 115
        self.color_button_selected = 240, 101, 67
        self.color_background = 255, 255, 255
        self.color_font = 0, 0, 0
        self.color_arrow = 0, 0, 0

        self.size = int(100)
        self.boardSide = self.size * 6
        self.screen = pygame.display.set_mode((1000, 600))
        self.marked = []    # which block is currently selected
        self.moves = 0      # moves done
        self.min_moves = int(moves) # minimum required moves for a solution
        self.last_moves = [] # [block , x, y]
        self.difficulty = difficulty # current difficulty
        self.sol = None # list of the moves for the solution
        self.step = 0 # at which step of the solution
        self.arrow = None # currently shown arrow
        # buttons
        self.button_next = pygame.Rect(870, 200, 100, 50)
        self.button_reset = pygame.Rect(750, 200, 100, 50)
        self.button_back = pygame.Rect(630, 200, 100, 50)
        self.button_solve = pygame.Rect(750, 450, 100, 50)
        self.buttons_diff = [pygame.Rect(635 + i*70, 350, 50, 50) for i in range(5)]
       
    # restart the game with the same configuration
    def reset(self):
        RetteDenBlock = Game(self.min_moves, self.listOfBlocks, self.difficulty)
        RetteDenBlock.play()
    # set to initial configuration
    def softReset(self):
        self.setupBoard()
        self.last_moves = []
        self.moves = 0
        self.setup()
    # changes the board to the initial configuration
    def setupBoard(self):
        for i, val in enumerate(self.listOfBlocks):
            self.board[i//6][i%6] = val
    # returns bool if the game is over
    def isGameOver(self):
        return self.board[2][5] == "A"
    # manages clicks
    def click(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.button_next.collidepoint(pos):
                        nextGame(self.difficulty)
                    elif self.button_reset.collidepoint(pos):
                        self.reset()
                    elif self.button_back.collidepoint(pos):
                        if self.last_moves:
                            x1, y1, move = self.last_moves.pop()
                            self.moveBlock(x1, y1, 0, 0, move=move) # x2 and y2 are irrelevant when move is given
                            self.last_moves.pop()
                            self.moves -= 2
                            self.marked = []
                            return None
                    elif self.button_solve.collidepoint(pos):
                        if not self.sol:
                            self.sol = solve.solve(self.listOfBlocks)
                        self.softReset()
                        self.addArrow(self.sol[0])
                        return None
                    elif pos[0] <= 600 and pos[1] <= 600:
                        ret = self.clickOnBoard(pos)
                        if ret != None:
                            x1, y1, x2, y2 = ret
                            if self.isLegal(x1, y1, x2, y2):
                                self.moveBlock(x1, y1, x2, y2, move=[7,7]) 
                                return None
                    elif self.buttons_diff[0].collidepoint(pos): return self.clickOnDifficulty(0)
                    elif self.buttons_diff[1].collidepoint(pos): return self.clickOnDifficulty(1)
                    elif self.buttons_diff[2].collidepoint(pos): return self.clickOnDifficulty(2)
                    elif self.buttons_diff[3].collidepoint(pos): return self.clickOnDifficulty(3)
                    elif self.buttons_diff[4].collidepoint(pos): return self.clickOnDifficulty(4)
    # returns the position of the cell of a block which is the nearest to the end position
    def getStartBlock(self, move):
        if move[1] < 0 or move[2] < 0:
            for x in range(6):
                for y in range(6):
                    if self.board[y][x] == move[0]:
                        return [x, y]
        else:
            for x in reversed(range(6)):
                for y in reversed(range(6)):
                    if self.board[y][x] == move[0]:
                        return [x, y]
    # modifies self.arrow to a polygon given a move
    def addArrow(self, move):
        sb = self.getStartBlock(move)   # start_block
        eb = [sb[0] + move[1], sb[1] + move[2]] # end_block
        s = self.size
        if move[1] > 0:
            self.arrow = ((s*sb[0]+40, s*sb[1]+40), (s*sb[0]+40, s*sb[1]+60), (s*sb[0]+move[1]*s, s*sb[1]+60), (s*sb[0]+move[1]*s, s*sb[1]+70), (s*eb[0]+50, s*eb[1]+50), (s*sb[0]+move[1]*s, s*sb[1]+30), (s*sb[0]+move[1]*s, s*sb[1]+40))
        elif move[1] < 0:
            self.arrow = ((s*sb[0]+60, s*sb[1]+40), (s*sb[0]+60, s*sb[1]+60), (s*sb[0]+100+move[1]*s, s*sb[1]+60), (s*sb[0]+100+move[1]*s, s*sb[1]+70), (s*eb[0]+50, s*eb[1]+50), (s*sb[0]+100+move[1]*s, s*sb[1]+30), (s*sb[0]+100+move[1]*s, s*sb[1]+40))
        elif move[2] > 0:
            self.arrow = ((s*sb[0]+40, s*sb[1]+40), (s*sb[0]+60, s*sb[1]+40), (s*sb[0]+60, s*sb[1]+move[2]*s), (s*sb[0]+70, s*sb[1]+move[2]*s), (s*eb[0]+50, s*eb[1]+50), (s*sb[0]+30, s*sb[1]+move[2]*s), (s*sb[0]+40, s*sb[1]+move[2]*s))
        else:
            self.arrow = ((s*sb[0]+40, s*sb[1]+60), (s*sb[0]+60, s*sb[1]+60), (s*sb[0]+60, s*sb[1]+100+move[2]*s), (s*sb[0]+70, s*sb[1]+100+move[2]*s), (s*eb[0]+50, s*eb[1]+50), (s*sb[0]+30, s*sb[1]+100+move[2]*s), (s*sb[0]+40, s*sb[1]+100+move[2]*s))
    
    def clickOnDifficulty(self, difficulty):
        self.difficulty = difficulty
    # manages clicks on the board
    # returns x1, y1, x2, y2 when its the second click on the board
    def clickOnBoard(self, pos):
        if len(self.marked) == 0:
            x1 = pos[0] // 100
            y1 = pos[1] // 100
            if self.board[y1][x1] != "o":
                block = self.board[y1][x1]
                self.marked.append((block, x1, y1))
                self.setup()
        elif len(self.marked):
            x2 = pos[0] // 100
            y2 = pos[1] // 100
            block, x1, y1 = self.marked.pop()
            # change marked block if another block was clicked
            if self.board[y2][x2] != "o":
                if self.board[y2][x2] != block:
                    block = self.board[y2][x2]
                    self.marked.append((block, x2, y2))
                self.setup()
            else:
                return x1,y1,x2,y2
    # moves a block given x1, y1, x2, y2 or a move and x1, y1
    # for example self.moveBlock(x1, y1, x2, y2) or self.moveBlock(x1, y1, 0, 0, move=[0, 1])
    def moveBlock(self, x1, y1, x2, y2, move = [7,7]):
        block = self.board[y1][x1]
        
        # list of all cells of the selected block
        cells = []
        for y in range(6): # TODO ob x oder y vorne
            for x in range(6):
                if self.board[y][x] == block:
                    cells.append((x, y))
        # move describes the change of the y and x coordinate of the nearest cell of the block to the target cell
        if move == [7, 7]:
            for x, y in cells:
                move_x = x2-x
                move_y = y2-y
                if abs(move_x) < abs(move[0]):
                    move[0] = move_x
                if abs(move_y) < abs(move[1]):
                    move[1] = move_y
        # add the move to last_moves
        self.last_moves.append([x2, y2, [-move[0],-move[1]]])
        # check if its the same move the arrow describes
        if self.arrow:
            if move[0] == self.sol[self.step][1] and move[1] == self.sol[self.step][2]:
                # add next arrow
                self.step += 1
                if self.step < self.min_moves:
                    self.addArrow(self.sol[self.step])
            else:
                # remove arrow
                self.step = 0
                self.arrow = None
        self.moves += 1
        # modify board
        for x, y in cells:
            self.board[y][x] = 'o'
        for x, y in cells:
            self.board[y+move[1]][x+move[0]] = block
    # returns True when the move is legal else False
    def isLegal(self, x1, y1, x2, y2):
        if x1-x2 != 0 and y1-y2 != 0:
            return False
        if x1 == x2 and y1 == y2:
            return False
        if self.board[y1][x1] == "o":
            return False
        if self.board[y1][x1] == self.board[y2][x2]:
            return False
        block = self.board[y1][x1]
        # horizontal
        if x1-x2 != 0:
            isHorizontalBlock = False
            if x1 > 0:
                if self.board[y1][x1-1] == block:
                    isHorizontalBlock = True
            if x1 < 5:
                if self.board[y1][x1+1] == block:
                    isHorizontalBlock = True
            if not isHorizontalBlock:
                return False

            # check if there are blocks between the end and start position of the block
            if x1 < x2:
                for i in range(x1+1, x2+1):
                    if self.board[y1][i] != 'o' and self.board[y1][i] != block:
                        return False
            else:
                for i in range(x2, x1):
                    if self.board[y1][i] != 'o' and self.board[y1][i] != block:
                        return False
        # vertical
        else:
            isVerticalBlock = False
            if y1 > 0:
                if self.board[y1-1][x1] == block:
                    isVerticalBlock = True
            if y1 < 5:
                if self.board[y1+1][x1] == block:
                    isVerticalBlock = True
            if not isVerticalBlock:
                return False
            # check if there are blocks between the end and start position of the block
            if y1 < y2:
                for i in range(y1+1, y2+1):
                    if self.board[i][x1] != 'o' and self.board[i][x1] != block:
                        return False
            else:
                for i in range(y2, y1):
                    if self.board[i][x1] != 'o' and self.board[i][x1] != block:
                        return False
        return True
    # setups board
    def setup(self):
        pygame.init()
        screen = self.screen
        screen.fill(self.color_background)
        count = 0
        # how fine the tiles should be
        size = self.size//4
        for i in range(24):
            for x in range(24):
                #check if current loop value is even
                if count % 2 == 0:
                    pygame.draw.rect(screen, self.color_tile1,[size*x,size*i,size,size])
                else:
                    pygame.draw.rect(screen, self.color_tile2,[size*x,size*i,size,size])
                count +=1
            count-=1
        pygame.draw.rect(screen,self.color_tile_finish,[500,200,100,100])
        # add blocks
        for i in range(6):
            for j in range(6):
                if self.board[i][j] == "o":
                    continue
                block = self.board[i][j]
                color = self.color_blocks
                # fill inner of the cells
                if block == "A":
                    color = self.color_start_block
                if block in [i[0] for i in self.marked]:
                    if block != "A":
                        color = self.color_blocks_selected
                    else:
                        color = self.color_start_block_selected
                # fill spaces between cells if cells are of the same block
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
                pygame.draw.rect(image, color, (0,0,length,height))
                
                screen.blit(image, (j*self.size+hor, i*self.size+ver))
        # draw arrow
        if self.arrow:
            pygame.draw.polygon(screen, self.color_arrow, self.arrow)

        # number of moves
        font = pygame.font.SysFont('Arial Bold', 50)
        movessurface = font.render(str(self.moves)+" / "+str(self.min_moves), False, self.color_font)
        screen.blit(movessurface,(765,70))
        # Difficulty text
        movessurface = font.render("Difficulty:", False, self.color_font)
        screen.blit(movessurface,(720, 290))
        # Next button
        pygame.draw.rect(screen, self.color_button, self.button_next)
        movessurface = font.render("Next", False, self.color_font)
        screen.blit(movessurface, (882, 210))
        # Reset button
        pygame.draw.rect(screen, self.color_button, self.button_reset)
        movessurface = font.render("Reset", False, self.color_font)
        screen.blit(movessurface, (753, 210))
        # Back button
        pygame.draw.rect(screen, self.color_button, self.button_back)
        movessurface = font.render("Back", False, self.color_font)
        screen.blit(movessurface, (638, 210))
        # Solve button
        pygame.draw.rect(screen, self.color_button, self.button_solve)
        movessurface = font.render("Solve", False, self.color_font)
        screen.blit(movessurface, (755, 458))
        # difficulty buttons
        for i in range(5):
            if i == self.difficulty:
                color = self.color_button_selected
            else: 
                color = self.color_button
            pygame.draw.rect(screen, color, self.buttons_diff[i])
            movessurface = font.render(str(i+1), False, self.color_font)
            screen.blit(movessurface, (651 + i*70, 358))

        pygame.display.update()
        
    def play(self):
        self.setupBoard()
        self.setup()
        while self.isGameOver() == 0:
            #self.printBoard()
            self.click()
            self.setup()
        nextGame(self.difficulty)

with open("data.txt", "r") as f:
    games = [line.replace("\n", "").split(" ") for line in f.readlines()][::-1]

# returns highest index where the min number of moves is higher or equal to target
def binary_search_games(l, target):
    lo=0
    hi = len(l)
    while lo < hi:
        mid = (lo+hi)//2
        if int(l[mid][0]) < target: lo = mid+1
        else: hi = mid
    return lo

# list with 5 sublists of all games where the min_number of moves is 1-9, 10-19, 20-29, 30-39, 40-51
games_difficulties = []
last = len(games)
for i in reversed(range(5)):
    low = binary_search_games(games, i*10)
    games_difficulties.append(games[low:last])
    last = low
games_difficulties = games_difficulties[::-1]

def nextGame(difficulty):
    rand = randrange(len(games_difficulties[difficulty]))
    min_number_of_moves = games_difficulties[difficulty][rand][0]
    board = games_difficulties[difficulty][rand][1]

    RetteDenBlock = Game(min_number_of_moves, board, difficulty)
    RetteDenBlock.play()


#main
if __name__ == "__main__":
    nextGame(1)