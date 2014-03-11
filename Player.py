import Maze, Vector, Matrix, Graphics, math



# handles player variables
class Player:
    # sets initial values
    def __init__ (self, maze, side):
        self.maze = maze
        self.side = side
        self.resetPlayer ()
        if self.side == 'robot':
            self.maze.addRobot (self)

    # sets up player for new round
    def setUpPlayer (self, pos, clrBase = None, clrTurret = None):
        if self.side == 'player':
            self.maze.addPlayer (self)
        self.pos = pos
        self.vel = 0
        self.cooldownTimer = 0
        self.viewTheta = math.pi / 8
        self.base = Graphics.cube (clrBase)
        self.base.transform (Matrix.scale (7.5, 7.5, 3.75))
        self.base.translate (self.pos.x (), self.pos.y(), 10)
        self.turretp1 = Graphics.icosahedron (clrTurret)
        self.turretp1.transform (Matrix.scale (5, 5, 5))
        self.turretp2 = Graphics.cube (clrTurret)
        self.turretp2.transform (Matrix.scale (1, 7.5, 1))
        self.turretp2.translate (0, 3.5, 0)
        self.turret = self.turretp1.union (self.turretp2)
        self.turret.translate (self.pos.x (), self.pos.y(), 0)
        self.theta = 0
        self.turretTheta = 0
        self.changeAngle (math.pi / 4)
        self.alive = True

    # resets any upgrades
    def resetPlayer (self):
        self.movementSpeed = 1.8275
        self.rotspeed = math.pi / 30
        self.turretrotspeed = self.rotspeed / 4
        self.cooldown = 30
        self.bulletSpeed = 3

    # returns position
    def position (self):
        return self.pos

    # returns the angle of player
    def angle (self):
        return self.theta

    # returns the turret angle of player
    def turretAngle (self):
        return self.turretTheta

    # returns the rotation speed of player
    def rotationSpeed (self):
        return self.rotspeed

    # returns the turret rotation speed of player
    def turretRotationSpeed (self):
        return self.turretrotspeed

    # returns the view angle of player
    def viewingAngle (self):
        return self.viewTheta

    # returns the Object of the player (graphics)
    def graphicsObjects (self):
        return self.base.union (self.turret)

    # returns true if player is at the end of the maze
    def doneMaze (self):
        return self.finishedMaze

    # sets Vector position of player
    def setPos (self, pos):
        self.pos = pos

    # sets the value of if the player is alive
    def setAlive (self, alive):
        self.alive = alive

    # rotates the turret towards direction player is facing
    def rotateTurret (self):
        t = rotationDirection (self.turretTheta, self.theta, self.turretrotspeed)
        if t != 0:
            self.turretTheta += t
            m = Matrix.translate (-self.pos.x (), -self.pos.y (), 0) * Matrix.rotate (0, -t, 0) * Matrix.translate (self.pos.x (), self.pos.y (), 0)
            self.turret.transform (m)
            
    # changes player angle and rotates object
    def changeAngle (self, dt):
        self.theta += dt
        m = Matrix.translate (-self.pos.x (), -self.pos.y (), 0) * Matrix.rotate (0, -dt, 0) * Matrix.translate (self.pos.x (), self.pos.y (), 0)
        self.base.transform (m)
        
    # changes the viewing angle, and limits it
    def changeViewTheta (self, dt):
        self.viewTheta += dt
        if self.viewTheta < 0:
            self.viewTheta = 0
        elif self.viewTheta > math.pi / 4:
            self.viewTheta = math.pi / 4

    # sets the player to move
    def setMovement (self, d_):
        d = d_
        if abs (d) > self.movementSpeed:
            d = self.movementSpeed * d / abs (d)
        self.vel += d

    # sets the player to rotate
    def setRotation (self, r_):
        r = r_
        if abs (r) > self.rotspeed:
            r = self.rotspeed * r / abs (r)
        self.changeAngle (r)

    # sets the player to rotate the turret
    def setTurretRotation (self, t_):
        t = t_
        if abs (t) > self.turretrotspeed:
            t = self.turretrotspeed * t / abs (t)
        self.turretTheta += t
        m = Matrix.translate (-self.pos.x (), -self.pos.y (), 0) * Matrix.rotate (0, -t, 0) * Matrix.translate (self.pos.x (), self.pos.y (), 0)
        self.turret.transform (m)

    # shoots the gun
    def shoot (self):
        if self.cooldownTimer == 0:
            self.maze.newBullet (Vector.Vector ([self.pos.x (), self.pos.y ()]), Vector.Vector ([self.bulletSpeed * math.sin (self.turretTheta), self.bulletSpeed * math.cos (self.turretTheta)]), self.side)
            self.cooldownTimer = self.cooldown

    # check pygame keyboard through Pygame pygame inputs
    # and set player movement variables accordingly.
    def getInput (self, pygame):
        keys = pygame.keyboardInput ()
        if keys [273]:
            self.setMovement (1)
        elif keys [274]:
            self.setMovement (-1)
        if keys [275]:
            self.setRotation (1)
        elif keys [276]:
            self.setRotation (-1)
        if keys [264] or keys [122]:
            self.changeViewTheta (-self.rotspeed / 5)
        elif keys [261] or keys [120]:
            self.changeViewTheta (self.rotspeed / 5)
        elif keys [32]:
            self.shoot ()

    # checks Maze maze to see if legible movement, moves if so, doesnt if not. also rotates turret
    def move (self):
        self.cooldownTimer -= 1
        if self.cooldownTimer < 0:
            self.cooldownTimer = 0
        dis = self.vel * Vector.Vector ([math.sin (self.theta), math.cos (self.theta)])
        if self.maze.canMove (self.pos, dis):
            self.pos += dis
            self.base.translate (dis.x (), dis.y (), 0)
            self.turret.translate (dis.x (), dis.y (), 0)
        self.vel = 0

# t1 is angle you are facing, t2 is where you want to be facing. s is the speed, returns rotation amount
def rotationDirection (t1_, t2_, s):
    t1 = t1_ % (math.pi * 2) + math.pi * 2
    t2 = t2_ % (math.pi * 2) + math.pi * 2
    if t2 != t1:
        dt = t2 - t1
        if abs (dt) > math.pi:
            dt = math.pi - dt
        dt = s * dt / abs (dt)
        if abs (t2 - t1) <= s:
            dt *= abs (t2 - t1) / s
        return dt
    return 0









        
