from game import Game
from box import Box
import pygame

game = Game(16, 16, 25)
grid = game.generateGrid()
# print(grid)
grid = game.generateBoxes(grid)
# print(grid)
grid = game.generateMines(30, grid)
grid = game.generateNumbers(grid)
print([[box.content for box in row] for row in grid])
