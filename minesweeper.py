import pygame
from game import Game
from box import Box
from random import randint

# Init pygame
pygame.init()

# GAME
game = Game(10, 10, 25)

# Settings
screenSize = game.screenSize
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Minesweeeeep")
grid = game.generateGrid()
game.generateBoxes(grid)
game.generateMines(10, grid)
game.generateNumbers(grid)

clock = pygame.time.Clock()

while not game.GAMEOVER:
    # FPS
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.GAMEOVER = True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                game.GAMEOVER = game.reveal(event.pos, grid)
            elif event.button == 3:
                game.flag(event.pos, grid)

    # Draw stuff
    game.mainLoop(grid, screen)

    pygame.display.flip()

