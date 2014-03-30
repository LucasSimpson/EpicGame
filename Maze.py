import Vector, Graphics, random, math

# bullet class yeaaaa
class Bullet:
    # initial position and velocity as Vectors
    def __init__ (self):
        self.pos = None
        self.vel = None
        self.alive = False

    # set position and velocity
    def setPositionVelocity (self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.bulletObject = Graphics.icosahedron ()
        self.bulletObject.translate (pos.x (), pos.y (), 5)

    # set alive status
    def setAlive (self, alive):
        self.alive = alive

    # returns the object for 3D viewing
    def graphicsObject (self):
        return self.bulletObject

    # moves the bullet
    def move (self):
        self.bulletObject.translate (self.vel.x (), self.vel.y (), 0)
        self.pos += self.vel

# bullet system class woot
class BulletSystem:
    # initial values
    def __init__ (self):
        self.enemies = []
        self.bullets = [Bullet () for a in range (20)]

    # add an enemy to hit list
    def addEnemy (self, enemy):
        self.enemies += [enemy]
        self.bullets += [Bullet () for a in range (20)]

    # adds a new Bullet
    def newBullet (self, pos, vel):
        for a in self.bullets:
            if a.alive == False:
                a.setAlive (True)
                a.setPositionVelocity (pos, vel)
                break

    # moves the bullets:
    def moveBullets (self, maze):
        for a in self.bullets:
            if a.alive:
                if maze.canMove (a.pos, a.vel):
                    a.move ()
                    for b in self.enemies:
                        if b.alive and (a.pos - b.pos).magSquared () <= 100:
                            a.setAlive (False)
                            b.setAlive (False)
                            break
                else:
                    a.setAlive (False)

    # returns list of polygons for 3D viewing
    def addBulletsToRender (self, world):
        for a in self.bullets:
            if a.alive:
                world.newTempObject (a.graphicsObject ())

    # resets for maze Load
    def reset (self):
        self.enemies = []
        self.bullets = [Bullet () for a in range (5)]

# class for a line, or wall, in the maze
class Line:
    # set vector locations of end points
    def __init__ (self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    # scale the line
    def scale (self, scale):
        self.p1 *= scale
        self.p2 *= scale

    # returns true if endpoint vectors of both line instances point to same set of
    # vector classes, doesnt necessarily check if coordinates of end points are the same
    def __eq__ (self, other):
        return (self.p1 is other.p1 and self.p2 is other.p2) or (self.p1 is other.p2 and self.p2 is other.p1)

    # returns line data as string
    def __str__ (self):
        return "Line from " + str (self.p1) + " to " + str (self.p2)

# maze class. Creates a random maze upon initialization
class Maze:
    # sets initial values
    def __init__ (self):
        self.size = 0
        self.scale = 50
        self.lines = None
        self.robotBulletSystem = BulletSystem ()
        self.playerBulletSystem = BulletSystem ()

    # loads maze for round
    def loadMaze (self, size):
        self.size = size
        self.lines = self.createMaze ()
        
    # resets variables for next round
    def reset (self):
        self.robotBulletSystem.reset ()
        self.playerBulletSystem.reset ()
        
    ##direction values
    ##  0
    ##3   1
    ##  2
    # creates a random maze
    def createMaze (self):
        # set up initial walls
        canWalk = [[[False for c in range (4)] for b in range (self.size)] for a in range (self.size)]
        self.recursiveMaze ([[False for b in range (self.size)] for a in range (self.size)], canWalk, 0, 0, 0, 0)
        # delete some walls at random so that the maze isn't so linear
        for a in range (len (canWalk)):
            for b in range (len (canWalk [a])):
                if a != 0 and a != len (canWalk) - 1 and b != 0 and b != len (canWalk [a]) - 1 and sum (canWalk [a][b]) != 4 and random.random () <= 0.2:
                    d = random.randint (0, 3)
                    while (canWalk [a][b][d]):
                        d = random.randint (0, 3)
                    canWalk [a][b][d] = True
                    if d == 0:
                        canWalk [a][b + 1][(d + 2) % 4] = True
                    elif d == 1:
                        canWalk [a + 1][b][(d + 2) % 4] = True
                    elif d == 2:
                        canWalk [a][b - 1][(d + 2) % 4] = True
                    elif d == 3:
                        canWalk [a - 1][b][(d + 2) % 4] = True
        self.canWalk = canWalk
        # set up instance lines []
        lines = []
        points = [[Vector.Vector ([1.0 * a / self.size, 1.0 * b / self.size]) for b in range (self.size + 1)] for a in range (self.size + 1)]
        for a in range (len (canWalk)):
            for b in range (len (canWalk [a])):
                if canWalk [a][b][0] == False:
                    lines += [Line (points [a][b + 1], points [a + 1][b + 1])]
                if canWalk [a][b][1] == False:
                    lines += [Line (points [a + 1][b + 1], points [a + 1][b])]
                if canWalk [a][b][2] == False:
                    lines += [Line (points [a + 1][b], points [a][b])]
                if canWalk [a][b][3] == False:
                    lines += [Line (points [a][b], points [a][b + 1])]
        # delete duplicate lines
        changed = True
        while (changed):
            changed = False
            for a in range (len (lines)):
                for b in range (len (lines)):
                    if lines [a] == lines [b] and a != b:
                        lines = lines [:a] + lines [a + 1:]
                        changed = True
                        break
                if changed:
                    break
        # scale maze
        for a in lines:
            a.scale (self.scale * self.size)
        return lines

    # recursive function to create a random maze
    def recursiveMaze (self, beenTo, canWalk, fx, fy, nx, ny):
        if beenTo [nx][ny] == False:
            beenTo [nx][ny] = True
            if nx - fx == 1:
                canWalk [nx][ny][3] = True
                canWalk [fx][fy][1] = True
            if nx - fx == -1:
                canWalk [nx][ny][1] = True
                canWalk [fx][fy][3] = True
            if ny - fy == 1:
                canWalk [nx][ny][2] = True
                canWalk [fx][fy][0] = True
            if ny - fy == -1:
                canWalk [nx][ny][0] = True
                canWalk [fx][fy][2] = True
            calls = []
            if nx != 0:
                calls += [[-1, 0]]
            if nx != len (beenTo) - 1:
                calls += [[1, 0]]
            if ny != 0:
                calls += [[0, -1]]
            if ny != len (beenTo [0]) - 1:
                calls += [[0, 1]]
            for a in range (len (calls)):
                for b in range (len (calls)):
                    id = random.randint (0, len (calls) - 1)
                    calls [a], calls [id] = calls [id], calls [a]
            for a in calls:
                self.recursiveMaze (beenTo, canWalk, nx, ny, nx + a [0], ny + a [1])

    # returns a list of lines
    def toList (self):
        return self.lines

    # takes in a position Vecotor pos and distance Vector dis, returns true if legal movement
    def canMove (self, pos, dis):
        # old hit detection
##        for a in self.lines:
##            if lineSweptCircleIntersection (a.p1, a.p2, pos, dis, self.playerRadius):
##                return False
##        return True
        # new hit detection, faster
        newPos = pos + dis
        if newPos.x () < 0 or newPos.x () > self.scale * self.size or newPos.y () < 0 or newPos.y () > self.scale * self.size:
            return False
        id1x = int (pos.x () / self.scale)
        id1y = int (pos.y () / self.scale)
        id2x = int (newPos.x () / self.scale)
        id2y = int (newPos.y () / self.scale)
        if id1x == id2x and id1y == id2y:
            return True
        else:
            if id2x > id1x: # crossing right
                return self.canWalk [id1x][id1y][1]
            elif id2x < id1x: # crossing left
                return self.canWalk [id1x][id1y][3]
            elif id2y > id1y: # crossing top
                return self.canWalk [id1x][id1y][0]
            elif id2y < id1y: # crossing bottom
                return self.canWalk [id1x][id1y][2]
            else:
                print "Well fuck, this isn't supposed to happen"
                return True

    # returns true if the Vector pos is a valid positon
    def validPosition (self, pos):
        # for better hit detection
##        for a in self.lines:
##            if lineCircleIntersection (a.p1, a.p2, pos, self.playerRadius):
##                return False
##        return True
        # new hit detection
        return True

    # adds a new player for bullet hit detection
    def addPlayer (self, player):
        self.robotBulletSystem.addEnemy (player)

    # add a robot for bullet hit detection
    def addRobot (self, robot):
        self.playerBulletSystem.addEnemy (robot)
        
    # makes a new bullet
    def newBullet (self, pos, vel, side):
        if side == 'robot':
            self.robotBulletSystem.newBullet (pos, vel)
        elif side == 'player':
            self.playerBulletSystem.newBullet (pos, vel)

    # moves bullets and calc collisions
    def moveBullets (self):
        self.playerBulletSystem.moveBullets (self)
        self.robotBulletSystem.moveBullets (self)
                    
    # adds the bullets to the render
    def addBulletsToRender (self, world):
        self.playerBulletSystem.addBulletsToRender (world)
        self.robotBulletSystem.addBulletsToRender (world)

# technically don't need any of these functions with the faster hit detection but fuck it im keeping em
# takes in Vectors p1, p2, q1, q2 and returns the hit times if line segments
# from p1 to p2 and q1 to q2 intersect
def lineIntersectionTime (p1, p2, q1, q2):
    u = p2 - p1
    v = q2 - q1
    if u.perp () * v == 0:
        return None
    den = u.perp () * v
    w = p1 - q1
    s = v.perp () * w / den
    t = u.perp () * w / den
    return [s, t]

# returns true if lines p1-p2 and q1-q2 intersect
def lineIntersection (p1, p2, q1, q2):
    t = lineIntersectionTime (p1, p2, q1, q2)
    if t == None:
        return False
    return t [0] >= 0 and t [0] <= 1 and t [1] >= 0 and t [1] <= 1

# returns true if line segment defined by position Vectors p1 and p2 intersect
# with circle defined by position Vector cpos and radius r
def lineCircleIntersection (p1, p2, cpos, r):
    l = p2 - p1
    n = l.perp ()
    if abs ((n * (p1 - cpos)) / (n.mag ())) > r:
        return False
    if (cpos - p1) * l >= 0 and (cpos - p2) * l <= 0:
        return True
    if ((cpos - p1).mag () <= r) or ((cpos - p2).mag () <= r):
        return True
    return False

# returns true if movement of direction Vector dis of circle defined by position
# Vector cpos and radius r intersect with line segment defined by position
# Vectors p1 and p2
def lineSweptCircleIntersection (p1, p2, cpos, dis, r):
    l = p2 - p1
    if lineCircleIntersection (p1, p2, cpos, r) or lineCircleIntersection (p1, p2, cpos + dis, r):
        return True
    offset = l.perp ().setMag (r)
    return lineIntersection (cpos + offset, cpos + offset + dis, p1, p2) or lineIntersection (cpos - offset, cpos - offset + dis, p1, p2)
