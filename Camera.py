import Vector
import Matrix

class Camera:
    # sets initial values
    # -r = coordinate of camera
    # -n = direction camera is looking
    # -v = 'upwards' direction, doesnt have to be exact, program will approximate
    # -e = position of eye relative to camera
    # -width / height are width and height in virtual screen
    # -F and B are the eye Front and Back clipping planes distances
    # -Vl/Vr/Vt/Vb are left/right/top/bottom of window coordinates. virtual
    #  screen coordinates are mapped to window coordinates
    def __init__ (self, r, n, v, e, width = 2, height = 2, F = 1, B = 999, Vl = 0, Vr = 600, Vb = 0, Vt = 600):
        self.pos = r
        self.lookDir = n.normal ()
        self.setUpDir (v)
        self.u = n.cross (self.up)
        self.e = e * 1.0
        self.Mp = Matrix.Matrix ([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -1.0 / self.e.z ()], [0, 0, 0, 1]])
        self.Ms = Matrix.Matrix ([[1, 0, 0, 0], [0, 1, 0, 0], [-self.e.x () / self.e.z (), -self.e.y () / self.e.z (), 1, 0], [0, 0, 0, 1]])
        self.Wr = 1
        self.Wl = -1
        self.Wt = 1
        self.Wb = -1
        self.F = F
        self.B = B
        self.Vl = Vl
        self.Vr = Vr
        self.Vb = Vb
        self.Vt = Vt
        Su = 1.0 * (self.Vl - self.Vr) / (self.Wl - self.Wr)
        Sv = 1.0 * (self.Vt - self.Vb) / (self.Wt - self.Wb)
        Sn = 1.0 * ((self.e.z () - self.B) * (self.e.z () - self.F)) / (self.e.z () * self.e.z () * (self.B - self.F))
        ru = 1.0 * ((self.Vr * self.Wl) - (self.Vl * self.Wr)) / (self.Wl - self.Wr)
        rv = 1.0 * ((self.Vb * self.Wt) - (self.Vt * self.Wb)) / (self.Wt - self.Wb)
        rn = 1.0 * (self.F * (self.e.z () - self.B)) / (self.e.z () * (self.F - self.B))
        self.N = Matrix.Matrix ([[Su, 0, 0, 0], [0, Sv, 0, 0], [0, 0, Sn, 0], [ru, rv, rn, 1]])
        self.Mconst = self.Ms * self.Mp * self.N
        self.calcTransMatrix ()

    # calculates the transformation matrix based of camera looking direction/
    # position/ rotation
    def calcTransMatrix (self):
        self.u = self.lookDir.cross (self.up)
        rp = Vector.Vector ([-self.pos * self.u, -self.pos * self.up, -self.pos * self.lookDir])
        self.M = Matrix.Matrix ([[self.u.x (), self.up.x (), self.lookDir.x (), 0], [self.u.y (), self.up.y (), self.lookDir.y (), 0], [self.u.z (), self.up.z (), self.lookDir.z (), 0], [rp.x (), rp.y (), rp.z (), 1]])
        self.Mtot = self.M * self.Mconst
        self.recalc = False

    # translates the camera
    def translate (self, x, y, z):
        self.setPosition (self.pos + Vector.Vector ([x, y, z]))

    # rotates the camera
    def rotate (self, H, A, R):
        m = Matrix.rotate (H, A, R)
        self.setLookingDir (Vector.Vector ((Matrix.Matrix ([self.lookDir.toList () + [0]]) * m).vectorRow (1).toList () [:3]))
        self.setUpDir (Vector.Vector ((Matrix.Matrix ([self.up.toList () + [0]]) * m).vectorRow (1).toList () [:3]))

    # sets camera to Vector pos
    def setPosition (self, pos):
        self.pos = pos
        self.recalc = True
        self.setUpDir (self.up)

    # sets camera looking direction to Vector ldir
    def setLookingDir (self, ldir):
        self.lookDir = ldir.normal ()
        self.recalc = True

    # sets the 'up' direction of the camera (for rotation) to close
    # approximation of Vector udir
    def setUpDir (self, udir):
        self.up = (udir - (udir * self.lookDir) * self.lookDir).normal ()
        self.recalc = True

    # returns the position of the camera
    def position (self):
        return self.pos
    
    # returns the looking direction of the camera
    def lookingDir (self):
        return self.lookDir

    # returns the 'up' direction of the camera
    def upDir (self):
        return self.up

    # takes in 3 dimensional Vector q and returns the 4D projection
    # [u, v, n]
    def persp (self, q):
        if self.recalc:
            self.calcTransMatrix ()
        return (Matrix.Matrix ([q.toList()]) * self.Mtot).vectorRow (1)

    # returns camera as a string
    def __str__ (self):
        r = "Camera at position " + str (self.r) + "\n"
        r += "Looking in direction " + str (self.n) + "\n"
        r += "With 'up' in direction " + str (self.v)
        return r
        

