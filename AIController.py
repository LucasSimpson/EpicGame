import Vector, Player, math, random

# handles all the enemies
class AIController:
    # sets up all the evil robots set to make your game experience miserable
    def __init__ (self, maze, human):
        self.maze = maze
        self.target = human #muhahahaha
        self.robots = []
        self.turnSpeed = []

    # sets up for new game
    def setUpRobots (self, numAI, pygame):
        self.robots = []
        for a in range (numAI):
            while (True):
                x = random.random () * self.maze.size * self.maze.scale
                y = random.random () * self.maze.size * self.maze.scale
                if self.maze.validPosition (Vector.Vector ([x, y])):
                    self.robots += [Player.Player (self.maze, 'robot')]
                    self.robots [-1].setUpPlayer (Vector.Vector ([x, y]), pygame.colorRGB (random.randint (0, 255), random.randint (0, 255), random.randint (0, 255)), pygame.colorRGB (random.randint (0, 255), random.randint (0, 255), random.randint (0, 255)))
                    self.robots [-1].bulletSpeed = 2
                    self.turnSpeed += [0]
                    break

    # load all the robots into the 3D world
    def addRobotsToRender (self, world):
        for a in self.robots:
            if a.alive:
                world.newTempObject (a.graphicsObjects ())

    # do all the artificial intelligence for movement. its shitty AI, good thing these robots are cheap as hell...
    def move (self):
        # actual artificial intelligence
        for a in range (len (self.robots)):
            if self.robots [a].alive:
                # rotate to face target
                t = Player.rotationDirection (self.robots [a].turretAngle (), angle (self.target.position () - self.robots [a].position ()), self.robots [a].turretRotationSpeed ())
                self.robots [a].setTurretRotation (t)
                # rotates robot randomly, stupid robots
                self.turnSpeed [a] += (random.random () - 0.5) * 0.01
                self.robots [a].setRotation (self.turnSpeed [a])
                # move robot forward with no knowledge of whats ahead
                self.robots [a].setMovement (1)
                # shoot
                self.robots [a].shoot ()
                # move
                self.robots [a].move ()

    # returns true if at least 1 robot is alive
    def notAllDead (self):
        for a in self.robots:
            if a.alive:
                return True
        return False

# returns the angle of a vector
def angle (v):
    if v.x () >= 0:
        if v.y () >= 0:
            return math.atan (v.x () / v.y ())
        else:
            return math.atan (-v.y () / v.x ()) + math.pi / 2
    else:
        if v.y () >= 0:
            return math.atan (v.y () / -v.x ()) + math.pi * 1.5
        else:
            return math.atan (-v.x () / -v.y ()) + math.pi
                        
