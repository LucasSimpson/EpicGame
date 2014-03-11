# handles vector math
class Vector:
    # set initial values
    def __init__ (self, val):
        self.val = val

    # return the magnitude
    def mag (self):
        return self.magSquared () ** 0.5

    # returns the magnitude squared (faster, no square root operation)
    def magSquared (self):
        return sum (map (lambda x: x ** 2, self.val))

    # return vector of magnitude m in same direction
    def setMag (self, m):
        return self * (1.0 * m / self.mag ())

    # return normal vector
    def normal (self):
        return self.setMag (1)

    # return the perpendicular vector if 2 dimensional vector
    def perp (self):
        if len (self.val) == 2:
            return Vector ([-self.y (), self.x ()])
        return NotImplemented

    # return cross product
    def cross (self, other):
        if len (self.val) == 2:
            return self.x () * other.y () - self.y () * other.x ()
        elif len (self.val) == 3:
            return Vector ([self.val [1] * other.val [2], self.val [2] * other.val [0], self.val [0] * other.val [1]]) - Vector ([self.val [2] * other.val [1], self.val [0] * other.val [2], self.val [1] * other.val [0]])
        return NotImplemented

    # return vector as a list
    def toList (self):
        return self.val

    # return the first component of vector
    def x (self):
        return self.val [0]

    # return the second component of vector
    def y (self):
        return self.val [1]

    # returns the third component of vector
    def z (self):
        return self.val [2]

    # returns the i'th component
    def value (self, i):
        return self.val [i]

    # adds two vectors/ adds vector with scalar
    def __add__ (self, other):
        if isinstance (other, Vector) and len (self.val) == len (other):
            return Vector ([self.val [a] + other.val [a] for a in range (len (self))])
        elif isinstance (other, int) or isinstance (other, float):
            return Vector ([self.val [a] + other for a in range (len (self))])
        else:
            return NotImplemented

    def __radd__ (self, other):
        return self + other

    def __iadd__ (self, other):
        return self + other

    def __sub__ (self, other):
        return self + -1 * other

    def __rsub__ (self, other):
        return self - other

    def __isub__ (self, other):
        return self - other

    def __neg__ (self):
        return self * -1

    # returns dot product if two vectors / scalar multiplication if scalar
    def __mul__ (self, other):
        if isinstance (other, Vector) and len (self) == len (other):
            return sum ([self.val [a] * other.val [a] for a in range (len (self))])
        elif isinstance (other, int) or isinstance (other, float):
            return Vector ([self.val [a] * other for a in range (len (self))])
        else:
            return NotImplemented

    def __rmul__ (self, other):
        return self * other

    def __imul__ (self, other):
        return self * other

    # return the dimension of vector
    def __len__ (self):
        return len (self.val)

    # returns true if dimension and coordinates of both vectors are equal
    def __eq__ (self, other):
        if len (self) != len (other):
            return False
        for a in range (len (self.val)):
            if self.val [a] != other.val [a]:
                return False
        return True

    # return the vectors as a string
    def __str__ (self):
        return "Vector " + str (self.val)
