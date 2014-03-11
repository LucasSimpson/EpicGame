import Vector

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
