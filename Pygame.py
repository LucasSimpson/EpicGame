import math
import os, sys
import pygame
import Vector

# check for font and sound ability
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# handles drawing to window
class Pygame:
    # set initial values
    def __init__(self, width = 600, height = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock ()
        self.frameCount = 0

    # takes in the game loop as parameter, runs each frame.
    # clears the screen each frame, updates the window each frame
    def MainLoop(self, programLoop = None):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()
            if programLoop != None:
                programLoop (self.frameCount)
            pygame.display.update ()
            self.clock.tick (30)
            self.frameCount += 1

    # set the keyboard input
    def keyboardInput (self):
        if pygame.key.get_focused ():
            return pygame.key.get_pressed ()
        return pygame.key.get_pressed ()

    # returns color object
    def color (self, s = "white"):
        return pygame.color.Color (s)
    def colorRGB (self, r, g, b):
        return pygame.color.Color (r, g, b)

    # draws a line from tuples p1 to p2 of color clr and width width
    def line (self, p1, p2, clr = color (None), width = 1):
        pygame.draw.line (self.screen, clr, p1, p2, width)

    # draws a rectangle from tuples corners p1 and p2 of color clr and width width
    def rect (self, p1, p2, clr = color (None), width = 0):
        pygame.draw.rect (self.screen, clr, pygame.Rect (int (p1.x ()), int (p1.y ()), int (p2.x () - p1.x ()), int (p2.y () - p1.y ())), width)

    # draws a circle at tuples pos or radius r of color clr and width width
    def circle (self, pos, r, clr = color (None), width = 0):
        pygame.draw.circle (self.screen, clr, pos, r, width)

    # takes in a list of tuples and draws a polygon connecting them of clr color and width width
    def polygon (self, pos, clr = color (None), width = 0):
        pygame.draw.polygon (self.screen, clr, pos, width)

    # updates the window
    def update (self):
        pygame.display.update ()


