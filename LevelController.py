import Vector

# controls level progression
class LevelController:
    # dem starting values
    def __init__ (self, maze, player, AI, world):
        self.maze = maze
        self.player = player
        self.AI = AI
        self.world = world
        self.level = 1
        self.mazeSizes = [3, 4, 4, 5, 5, 5, 6]
        self.numRobots = [1, 2, 3, 5, 7, 9, 13] 

    # set the level
    def setLevel (self, lvl):
        self.level = lvl

    # returns current level
    def currentLevel (self):
        return self.level

    # loads stuff for level to run
    def loadLevel (self, pygame):
        print "\n\n\n\n*** LEVEL " + str (self.level) + " ***"
        self.player.setUpPlayer (Vector.Vector ([25, 25]), pygame.colorRGB (54, 114, 255), pygame.colorRGB (54, 114, 0))
        self.world.newObject (self.player.graphicsObjects ())
        self.maze.loadMaze (self.mazeSizes [self.level - 1])
        self.world.loadMaze (self.maze, pygame)
        self.AI.setUpRobots (self.numRobots [self.level - 1], pygame)

    # resets after level is over
    def reset (self):
        self.inLevel = False
        self.maze.reset ()
        self.world.reset ()
