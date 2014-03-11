import Vector, math

# Matrix math functions
class Matrix:
##     ----Y---
##    |
##    |
##    X
##    |
##    |
## eg. input = [[1, 2, 3], [4, 5, 6]] results in the matrix
##       |1 2 3|
##       |4 5 6|
    # sets matrix values
    def __init__ (self, v):
        self.v = []
        for a in range (len (v)):
            t = []
            for b in range (len (v [a])):
                t.append (v [a][b])
            self.v.append (t)

    # print dimension compatibility issues
    def printError (self, other, m):
        print "CAN'T " + m + " MATRICES, NOT CORRECT DIMENSIONS (" + str (len (self.v)) + ", " + str (len (self.v [0])) + ") (" + str (len (other.v)) + ", " + str (len (other.v [0])) + ")"

    # return identity matrix of size s
    def identity (s):
        v = [[0 for b in range (s)]for a in range (s)]
        for a in range (s):
            v [a][a] = 1
        return Matrix (v)

    # set matrix value x, y equal to v
    def setValue (self, x, y, v):
        self.v [x - 1, y - 1] = v

    # return multiplication by a scalar
    def mult (self, n):
        x, y = len (self.v), len (self.v [0])
        v = []
        for a in range (x):
            t = []
            for b in range (y):
                t += [self.v [a][b] * n]
            v += [t]
        return Matrix (v)

    # return trace of matrix
    def trace (self):
        x = len (self.v)
        sum = 0
        if len (self.v [0]) < x:
            x = len (self.v [0])
        for a in range (x):
            sum += self.v [a][a]
        return sum

    # return the determinant
    def det (self):
        if len (self.v) != len (self.v [0]):
            return None
        if len (self.v) == 2:
            return self.v [0][0] * self.v [1][1] - self.v [0][1] * self.v [1][0]
        if len (self.v) == 3:
            d = 0
            for a in range (len (self.v [0])):
                n = 1
                for b in range (len (self.v)):
                    n *= self.v [b][(a + b) % (len (self.v [0]))]
                d += n
            for a in range (len (self.v [0])):
                n = 1
                for b in range (len (self.v)):
                    n *= self.v [b][(a - b) % (len (self.v [0]))]
                d -= n
            return d
        d = 0
        for a in range (len (self.v [0])):
            d += ((-1) ** (a)) * self.v [0][a] * (self.elementalCofactor (0, a)).det ()
        return d

    # return elemental cofactor matrix of index x, y
    def elementalCofactor (self, x, y):
        v = []
        for a in range (len (self.v)):
            t = []
            for b in range (len (self.v [0])):
                if a != x and b != y:
                    t += [self.v [a][b]]
            if t != []:
                v += [t]
        return Matrix (v)

    # return cofactor matrix
    def cofactor (self):
        v = []
        for a in range (len (self.v)):
            t = []
            for b in range (len (self.v [0])):
                t += [(-1) ** (a + b) * self.elementalCofactor (a, b).det ()]
            v += [t]

        return Matrix (v)
        
    # return the inverse
    def inverse (self):
        if self.det () == 0:
            return None
        return self.cofactor ().transpose ().mult (1.0 / self.det ())
            
    # return the transpose
    def transpose (self):
        v = [[0 for b in range (len (self.v))] for a in range (len (self.v [0]))]
        for a in range (len (self.v)):
            for b in range (len (self.v [0])):
                v [b][a] = self.v [a][b]
        return Matrix (v)

    # return a Vector from row i
    def vectorRow (self, i):
        return Vector.Vector (self.v [i - 1])

    # adds two matrices of same size together/ adds matrix with scalar
    def __add__ (self, other):
        if isinstance (other, Matrix):
            if (len (self.v) != len (other.v)) or (len (self.v [0]) != len (other.v [0])):
                self.printError (other, "ADD")
                return None
            v = []
            for a in range (len (self.v)):
                t = []
                for b in range (len (self.v [0])):
                    t.append (self.v [a][b] + other.v [a][b])
                v.append (t)
            return Matrix (v)
        elif isinstance (other, int) or isinstance (other, float):
            v = []
            for a in range (len (self.v)):
                t = []
                for b in range (len (self.v [0])):
                    t.append (self.v [a][b] + other)
                v.append (t)
            return Matrix (v)
        else:
            return NotImplemented

    def __radd__ (self, other):
        return self + other

    def __iadd__ (self, other):
        return self + other

    def __sub__ (self, other):
        return self + -1 * other

    def __rsub__ (self, other):
        return self * -1 + other

    def __isub__ (self, other):
        return self - other

    def __neg__ (self):
        return self * -1

    # multiplies two matrices if correct sizes/multiplies by a scalar
    def __mul__ (self, other):
        if isinstance (other, Matrix):
            if len (self.v [0]) != len (other.v):
                self.printError (other, "MULITPLY")
                return None
            v = []
            for a in range (len (self.v)):
                t = []
                for b in range (len (other.v [0])):
                    n = 0
                    for c in range (len (self.v [0])):
                        n += self.v [a][c] * other.v [c][b]
                    t += [n]
                v += [t]
            return Matrix (v)
        elif isinstance (other, int) or isinstance (other, float):
            return self.mult (other)
        else:
            return NotImplemented

    def __rmul__ (self, other):
        return self.__mul__ (other)

    def __imul__ (self, other):
        return self * other

    # return the matrix as a string
    def __str__ (self):
        r = ""
        for a in self.v:
            r += "|"
            for b in a:
                r += str (b) + " "
            r = r[:-1]
            r += "|\n"
        return r [:-1]

# returns 4x4 matrix of translation x, y, z
def translate (x, y, z):
    return Matrix ([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [x, y, z, 1]])

# returns 4x4 matrix of scaling in x, y, z
def scale (x, y, z):
    return Matrix ([[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]])

# returns 4x4 matrix of rotation H around y axis, A around z axis, and R around x axis
def rotate (H, A, R):
    return Matrix ([[math.cos (H), 0, -math.sin (H), 0], [0, 1, 0, 0], [math.sin (H), 0, math.cos (H), 0], [0, 0, 0, 1]]) * Matrix ([[math.cos (A), math.sin (A), 0, 0], [-math.sin (A), math.cos (A), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) * Matrix ([[1, 0, 0, 0], [0, math.cos (R), math.sin (R), 0], [0, -math.sin (R), math.cos (R), 0], [0, 0, 0, 1]])
    
# returns a 4x4 matrix of rotation by rad radians around the Vector axix
def rotateAboutAxis (axis, rad):
    p = 1 - math.cos (rad)
    l1 = [math.cos (rad) + axis.x()**2 * (p), axis.x()*axis.y()*(p) - axis.z()*math.sin(rad), axis.x()*axis.z()*(p) + axis.y()*math.sin(rad), 0]
    l2 = [axis.y()*axis.x()*(p) + axis.z()*math.sin(rad), math.cos (rad) + axis.y()**2 * (p), axis.y()*axis.z()*(p) - axis.x()*math.sin(rad), 0]
    l3 = [axis.z()*axis.x()*(p) - axis.y()*math.sin(rad), axis.z()*axis.y()*(p) + axis.x()*math.sin(rad), math.cos (rad) + axis.z()**2 * (p), 0]
    l4 = [0, 0, 0, 1]
    return Matrix ([l1, l2, l3, l4])




    
