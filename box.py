import pygame

class Box:
    
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content
        # Booby Trapped or BOOBED
        self.boobed = False
        self.isRevealed = False
        self.isFlagged = False
        self.beenChecked = False