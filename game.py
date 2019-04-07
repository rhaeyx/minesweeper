import pygame
import random
from box import Box

class Game:
    FLAG_COUNTER = 0
    MINE_COUNTER = 0
    GAMEOVER = False
    BG_COLOR = (255, 255, 255)
    BORDER_COLOR = (50,50 ,50)
    BOX_COLOR = (125, 125, 125)
    SAFE_COLOR = (128, 128, 128)
    FLAG_COLOR = (255, 255, 0)
    MINE_COLOR = (185, 122, 87)
    ONE_COLOR = (0, 60, 150)
    TWO_COLOR = (0, 150, 60)
    THREE_COLOR = (180, 0, 60)
    FOUR_COLOR = (128, 0, 128)
    FIVE_COLOR = (255, 128, 0)

    def __init__(self, rows, cols, pixels):
        pixels = 25
        self.rows = rows
        self.cols = cols
        self.pixels = pixels
        self.screenWidth = rows * pixels
        self.screenHeight = cols * pixels
        self.screenSize = (self.screenWidth, self.screenHeight)

    def generateGrid(self):
        # Generate 2 dimensional matrix.
        grid = [["COLUMN" for col in range(self.cols)] for row in range(self.rows)]
        return grid

    def generateBoxes(self, grid):
        y = 0
        for row in grid:
            x = 0
            for col in range(len(row)):
                row[col] = Box(x, y, '0')
                x += self.pixels   
            y += self.pixels

        return grid
        
    # BEYOND THIS LINE DOES NOT WORK
    def generateMines(self, mines, grid):
        while mines > 0:
            row = random.randint(0, self.rows - 1)
            box = random.randint(0, self.cols - 1)
            if random.randint(0, 1):
                grid[row][box].content = 'X' 
                grid[row][box].boobed = True 
                mines -= 1

        self.MINE_COUNTER = mines
        return grid

    def getSurroundingBoxes(self, box, grid):
            i = box.y // 25
            j = box.x // 25
            topExists = True if i > 0 else False
            leftSideExists = True if j > 0 else False
            rightSideExists = True if j < (self.cols - 1) else False
            botExists = True if i < (self.rows - 1) else False

            surroundingBoxes = []

            # TOPLEFT - TOP - TOPRIGHT
            # LEFT    -  X  - RIGHT
            # BOTLEFT - BOT - BOTRIGHT

            if topExists:
                top = grid[i - 1][j]
                surroundingBoxes.append(top)

                if leftSideExists:
                    topLeft = grid[i - 1][j - 1]
                    surroundingBoxes.append(topLeft)

                if rightSideExists:
                    topRight = grid[i - 1][j + 1]
                    surroundingBoxes.append(topRight)

            if leftSideExists:
                left = grid[i][j - 1]
                surroundingBoxes.append(left)

            if rightSideExists:
                right = grid[i][j + 1]
                surroundingBoxes.append(right)

            if botExists:
                bot = grid[i + 1][j]
                surroundingBoxes.append(bot)

                if leftSideExists:
                    botLeft = grid[i + 1][j - 1]
                    surroundingBoxes.append(botLeft)

                if rightSideExists:
                    botRight = grid[i + 1][j + 1]
                    surroundingBoxes.append(botRight)

            return surroundingBoxes

    def generateNumbers(self, grid):
        for i, row in enumerate(grid):
            for j, box in enumerate(row):
                if box.content == 'X':
                    surroundingBoxes = self.getSurroundingBoxes(box, grid)
                    for boxx in surroundingBoxes:
                        if boxx.content != 'X':
                            boxx.content = str(int(boxx.content) + 1)

        return grid

    def drawBoard(self, grid, screen):
        colors_dict = {
            'X': self.MINE_COLOR,
            '0': self.SAFE_COLOR,
            '1': self.ONE_COLOR,
            '2': self.TWO_COLOR,
            '3': self.THREE_COLOR,
            '4': self.FOUR_COLOR,
            '5': self.FIVE_COLOR         
        }        
        for row in grid:
            for box in row:
                if box.isFlagged:
                    color = self.FLAG_COLOR
                    pygame.draw.rect(screen, color, [box.x, box.y, self.pixels, self.pixels])

                elif box.isRevealed:
                    color = colors_dict[box.content]
                    pygame.draw.rect(screen, color, [box.x, box.y, self.pixels, self.pixels])
                pygame.draw.rect(screen, self.BORDER_COLOR, [box.x, box.y, self.pixels, self.pixels], 2)

    def revealBoard(self, grid):
        for row in grid:
            for box in row:
                box.isRevealed = True

    def revealSurroundingBoxes(self, box, grid):
        surroundingBoxes = self.getSurroundingBoxes(box, grid)
        for boxx in surroundingBoxes:
            if boxx.content == '0' and not boxx.beenChecked:
                boxx.isRevealed = True
                boxx.beenChecked = True
                self.revealSurroundingBoxes(boxx, grid)
            else:
                continue

    def reveal(self, pos, grid):
        row = pos[1] // self.pixels
        col = pos[0] // self.pixels
        box = grid[row][col]
        if box.content != 'X':
            box.isRevealed = True
            self.revealSurroundingBoxes(box, grid)
            return False
        else: 
            self.revealBoard(grid)
            # Value will be assigned to gameOver, to end game.
            return True

    def flag(self, pos, grid):
        row = pos[1] // self.pixels
        col = pos[0] // self.pixels
        box = grid[row][col]
        # box.isFlagged = not box.isFlagged would work but i cant inc the counters
        if box.isFlagged:
            box.isFlagged = False
            self.FLAG_COUNTER -= 1
        else: 
            box.isFlagged = True
            self.FLAG_COUNTER += 1

    def checkWin(self, grid, screen):
        for row in grid:
            for box in row:
                if not box.isFlagged:
                    if not box.isRevealed:
                        return

        for row in grid:
            for box in row:
                if box.content == 'X':
                    if box.isFlagged:
                        continue
                else:
                    if box.isFlagged:
                        return
        print("WINNNNNN")
        
    def mainLoop(self, grid, screen):
        screen.fill(self.BG_COLOR)
        self.drawBoard(grid, screen)
        self.checkWin(grid, screen)



