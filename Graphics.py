import Matrix, Vector, Pygame, Maze, Camera, math

# point class, for a single point in 3 space
class Point:
    # initial values
    def __init__ (self, pos, drawPoint = False):
        if drawPoint:
            self.pos = Vector.Vector (pos.toList () + [1])
            self.d4 = self.pos
            self.d3 = Vector.Vector (map (lambda x: x / self.d4.value (3), self.d4.toList ()) [:-1])
            self.d2 = Vector.Vector (map (lambda x: x / self.d3.value (2), self.d3.toList ()) [:-1])
        else:
            self.pos = Vector.Vector (pos.toList () + [1])
            self.d4 = None
            self.d3 = None
            self.d2 = None

    # transform point by Matrix m
    def transform (self, m):
        self.pos = (Matrix.Matrix ([self.pos.toList ()]) * m).vectorRow (1)

    # return the position
    def position (self):
        return self.pos

    # returns the x/y/z coordinate
    def x (self):
        return self.pos.x ()
    def y (self):
        return self.pos.y ()
    def z (self):
        return self.pos.z ()

    # returns the 4d/3d/2d coordinate
    def d4 (self):
        return self.d4
    def d3 (self):
        return self.d3
    def d2 (self):
        return self.d2

    # calculates 4 dimensional projection coordinate and extracts 3 and 2 dimensional projections
    def calcProjection (self, cam):
        self.d4 = cam.persp (self.pos)
        self.d3 = Vector.Vector (map (lambda x: x / self.d4.value (3), self.d4.toList ()) [:-1])
        self.d2 = Vector.Vector (map (lambda x: x / self.d3.value (2), self.d3.toList ()) [:-1])

    # return 2d screen position through Camera cam
    def drawPosition (self):
        return (int (self.d2.x ()), int (self.d2.y ()))

    # draw the point on screen through Pygame pygame
    def render (self, cam, pygame):
        self.dpos = self.drawPosition (cam)
        pygame.circle (dpos, 2)
        
    # return as string
    def __str__ (self):
        r = "World Coordinates: " + str (self.pos) + "\n"
        r += "4D Coordinates: " + str (self.d4) + "\n"
        r += "3D Coordinates: " + str (self.d3) + "\n"
        r += "2D Coordinates: " + str (self.d2) + "\n"
        return r

# collection of points
class Polygon:
    # set initial values
    def __init__ (self, points, clr = None):
        self.points = points
        self.drawPoints = None
        self.clr = clr
        self.calcNormal ()
        self.calcAveragePoint ()

    # calculate the normal vector
    def calcNormal (self):
        v1 = Vector.Vector ((self.points [2].pos - self.points [0].pos).toList () [:-1])
        v2 = Vector.Vector ((self.points [1].pos - self.points [0].pos).toList () [:-1])
        self.normal = v1.cross (v2)

    # calculates the average location of its vertices
    def calcAveragePoint (self):
        self.avePoint = sum ([a.position () for a in self.points])

    # set the color
    def setClr (self, clr):
        self.clr = clr

    # returns point i
    def point (self, i):
        return self.points [i]

    # returns the average location of its vertices
    def averagePoint (self):
        return self.avePoint

    # clips polygon to volume
    def clipToVolume (self, Vl, Vr, Vb, Vt):
        draw = False
        for a in self.drawPoints:
            if a.d2.x () > Vl and a.d2.x () < Vr and a.d2.y () > Vb and a.d2.y () < Vt:
                draw = True
                break
        if draw == False:
            self.drawPoints = []

    # calculates the projection coordinates
    def calcProjections (self, cam):
        self.drawPoints = self.points
        for a in self.drawPoints:
            a.calcProjection (cam)
             
    # calculates the draw positions through Camera cam and draws them to screen through Pygame pygame
    def render (self, cam, pygame):
        if self.drawPoints != []:
            dpos = []
            for a in self.drawPoints:
                dpos += [a.drawPosition ()]
            if self.clr == None:
                pygame.polygon (dpos, pygame.color ("white"))
            else:
                pygame.polygon (dpos, self.clr)
            pygame.polygon (dpos, pygame.color ("black"), 1)
            self.drawPoints = None

    # returns average depth of points for polygon
    def __float__ (self):
        return sum ([a.d3.value (2) for a in self.drawPoints]) / len (self.drawPoints)

# collection of polygons
class Object:
    # set initial values, a list of Points points, and list if indices points polyList
    def __init__ (self, points, polyList, clr = None):
        self.points = points
        self.polygons = []
        for a in polyList:
            self.polygons += [Polygon (map (lambda x: points [x], a), clr)]

    # transform object by Matrix m
    def transform (self, m):
        for a in self.points:
            a.transform (m)
        for a in self.polygons:
            a.calcNormal ()

    # translates object by x, y, z
    def translate (self, x, y, z):
        for a in self.points:
            a.pos += Vector.Vector ([x, y, z, 0])

    # calculates the projection of the points
    def calcProjections (self, cam):
        for a in self.points:
            a.calcProjection (cam)

    # returns list of polygons
    def polygonList (self):
        return self.polygons

    # combines two objects into a single object
    def union (ob1, ob2):
        ob = Object ([], [])
        ob.points = ob1.points + ob2.points
        ob.polygons = ob1.polygons + ob2.polygons
        return ob

class World:
    # sets starting values
    def __init__ (self, camera):
        self.camera = camera
        self.objects = []
        self.tempObjects = []
        self.changed = False

    # resets world for new round
    def reset (self):
        self.objects = []

    # loads a maze and player for 3d gameplay
    def loadMaze (self, maze, pygame):
        # set camera position
        self.camera.setPosition (Vector.Vector ([maze.scale / 2.0, maze.scale / 2.0, -500]))
        self.camera.setLookingDir (Vector.Vector ([0, 0, 1]))
        self.camera.setUpDir (Vector.Vector ([0, 1, 0]))
        # load maze
        for a in maze.toList ():
            p = [Point (Vector.Vector (a.p1.toList () + [0]))]
            p += [Point (Vector.Vector (a.p1.toList () + [20]))]
            p += [Point (Vector.Vector (a.p2.toList () + [20]))]
            p += [Point (Vector.Vector (a.p2.toList () + [0]))]
            self.objects += [Object (p, [[0, 1, 2, 3], [3, 2, 1, 0]], pygame.colorRGB (225, 225, 225))]

    # adds a new object
    def newObject (self, ob):
        self.objects += [ob]

    # adds an object for 1 frame only
    def newTempObject (self, obj):
        self.tempObjects += [obj]

    # loads a test polygon
    def loadPolygon (self):
        points += [Point (Vector.Vector ([1, 1, 1]))]
        points += [Point (Vector.Vector ([-1, 1, 1]))]
        points += [Point (Vector.Vector ([1, -1, 1]))]
        points += [Point (Vector.Vector ([-1, -1, 1]))]
        self.objects += [Object (points, [[2, 0, 1, 3]])]

    # translates the world by x, y, z units
    def translateWorld (self, x, y, z):
        self.changed = True
        m = Matrix.translate (x, y, z)
        for a in self.objects:
            a.transform (m)

    # rotates the world by H, A, and R radians around the y, z, and x axies
    def rotateWorld (self, H, A, R):
        m = Matrix.rotate (H, A, R)
        for a in self.objects:
            a.transform (m)

    # translates the camera by x, y, z units
    def translateCamera (self, x, y, z):
        self.camera.translate (x, y, z)

    # rotates the world by H, A, and R radians around the y, z, and x axies
    def rotateCamera (self, H, A, R):
        self.camera.rotate (H, A, R)

    # rotates/moves world depending on keyboard input
    def keyboardInput (self, pygame):
        keys = pygame.keyboardInput ()
        t = 0.015707963267948967 # pi/200
        v = 2.5
        # translating world
        if keys [119]:
            self.translateWorld (0, -v, 0)
        elif keys [115]:
            self.translateWorld (0, v, 0)
        if keys [100]:
            self.translateWorld (-v, 0, 0)
        elif keys [97]:
            self.translateWorld (v, 0, 0)
        if keys [113]:
            self.translateWorld (0, 0, -v)
        elif keys [101]:
            self.translateWorld (0, 0, v)
        # rotating world
        if keys [121]:
            self.rotateWorld (0, -t, 0)
        elif keys [114]:
            self.rotateWorld (0, t, 0)
        if keys [116]:
            self.rotateWorld (0, 0, t)
        elif keys [103]:
            self.rotateWorld (0, 0, -t)
        if keys [102]:
            self.rotateWorld (t, 0, 0)
        elif keys [104]:
            self.rotateWorld (-t, 0, 0)
        # translate camera
        if keys [107]:
            self.translateCamera (0, v, 0)
        elif keys [105]:
            self.translateCamera (0, -v, 0)
        if keys [108]:
            self.translateCamera (-v, 0, 0)
        elif keys [106]:
            self.translateCamera (v, 0, 0)
        if keys [111]:
            self.translateCamera (0, 0, v)
        elif keys [117]:
            self.translateCamera (0, 0, -v)
        # rotate camera
        if keys [263]:
            self.rotateCamera (0, -t, 0)
        elif keys [265]:
            self.rotateCamera (0, t, 0)
        if keys [264]:
            self.rotateCamera (0, 0, t)
        elif keys [261]:
            self.rotateCamera (0, 0, -t)
        if keys [262]:
            self.rotateCamera (t, 0, 0)
        elif keys [260]:
            self.rotateCamera (-t, 0, 0)
    
    # calculates the draw positions through Camera cam and draws them to screen through Pygame pygame 
    def render (self, pygame):
        # get all polygons from all Objects into a single list, calculates projections of points
        toRender = []
        for a in self.objects:
            toRender += a.polygonList ()
        for a in self.tempObjects:
            toRender += a.polygonList ()
        self.tempObjects = []
        totalNum = len (toRender)
        # sort out all polygons facing outward
        temp = []
        for a in toRender:
            if self.camera.lookingDir () * a.normal <= 0:
                temp += [a]
        toRender = temp
        # calculate projections
        for a in toRender:
            a.calcProjections (self.camera)
        # clip polygons to viewing volume
        for a in toRender:
            a.clipToVolume (0, 600, 0, 600)
        temp = []
        for a in toRender:
            if a.drawPoints != []:
                temp += [a]
        toRender = temp
        # sort polygons (painters algorithm)
        toRender = mergeSort (toRender)
        # draw polygons
        for a in toRender:
            a.render (self.camera, pygame)


# merge method for mergeSort ()
def merge (a, b):
    aid, bid = 0, 0
    r = []
    while (True):
        if float (a [aid]) > float (b [bid]):
            r += [a [aid]]
            aid += 1
            if aid == len (a):
                for i in range (bid, len (b)):
                    r += [b [i]]
                return r
        else:
            r += [b [bid]]
            bid += 1
            if bid == len (b):
                for i in range (aid, len (a)):
                    r += [a [i]]
                return r

# sorts any list of objects support the float () command, farthest first
def mergeSort (n): 
    if len (n) <= 1:
        return n
    return merge (mergeSort (n [:len (n) / 2]), mergeSort (n [len (n) / 2:]))

# takes in a point and list of points defining a convex polygon, returns
# true if the point is inside. polygon is assume to be defined clockwise
def insidePolygon (point, polygon):
    for a in range (len (polygon) - 1):
        v2 = point.position () - polygon [a].position ()
        v1 = polygon [a + 1].position () - polygon [a].position ()
        if v1.x () * v2.y () - v1.y () * v2.x () < 0:
            return False
    return True

# returns a icosahedron object
def icosahedron (clr = None):
    gr = (1 + math.sqrt (5)) / 2
    pointList = []
    pointList += [Vector.Vector ([0, gr, -1])]
    pointList += [Vector.Vector ([0, gr, 1])]
    pointList += [Vector.Vector ([0, -gr, 1])]
    pointList += [Vector.Vector ([0, -gr, -1])]
    pointList += [Vector.Vector ([-1, 0, gr])]
    pointList += [Vector.Vector ([1, 0, gr])]
    pointList += [Vector.Vector ([1, 0, -gr])]
    pointList += [Vector.Vector ([-1, 0, -gr])]
    pointList += [Vector.Vector ([-gr, 1, 0])]
    pointList += [Vector.Vector ([gr, 1, 0])]
    pointList += [Vector.Vector ([gr, -1, 0])]
    pointList += [Vector.Vector ([-gr, -1, 0])]
    s = 1.0 / (math.sqrt (1 + gr ** 2))
    points = [Point (s * a) for a in pointList]
    polyList = []
    polyList += [[0, 9, 6]]
    polyList += [[1, 8, 4]]
    polyList += [[0, 6, 7]]
    polyList += [[1, 4, 5]]
    polyList += [[0, 7, 8]]
    polyList += [[1, 5, 9]]
    polyList += [[3, 6, 10]]
    polyList += [[2, 4, 11]]
    polyList += [[3, 7, 6]]
    polyList += [[2, 5, 4]]
    polyList += [[3, 11, 7]]
    polyList += [[2, 10, 5]]
    polyList += [[0, 1, 9]]
    polyList += [[1, 0, 8]]
    polyList += [[2, 3, 10]]
    polyList += [[3, 2, 11]]
    polyList += [[9, 10, 6]]
    polyList += [[10, 9, 5]]
    polyList += [[11, 8, 7]]
    polyList += [[8, 11, 4]]
    return Object (points, polyList, clr)

# returns a cube object
def cube (clr = None):
    pointList = []
    pointList += [Vector.Vector ([1, 1, 1])]
    pointList += [Vector.Vector ([-1, 1, 1])]
    pointList += [Vector.Vector ([1, -1, 1])]
    pointList += [Vector.Vector ([-1, -1, 1])]
    pointList += [Vector.Vector ([1, 1, -1])]
    pointList += [Vector.Vector ([-1, 1, -1])]
    pointList += [Vector.Vector ([1, -1, -1])]
    pointList += [Vector.Vector ([-1, -1, -1])]
    pointList = [Point (a) for a in pointList]
    polyList = []
    polyList += [[3, 1, 0, 2]]
    polyList += [[2, 0, 4, 6]]
    polyList += [[6, 4, 5, 7]]
    polyList += [[7, 5, 1, 3]]
    polyList += [[4, 0, 1, 5]]
    polyList += [[2, 6, 7, 3]]
    return Object (pointList, polyList, clr)

        








        
        
