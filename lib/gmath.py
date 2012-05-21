"""
gmath.py defines functions used for transformations that are
used for graph objects.
"""
import math

def Distance(p1, p2):
    """Return the distance between Points a and b.
    Args:
    a: First Point
    b: Second Point
    Returns:
    Distance between points.
    """
    a = p1[0] - p2[0]
    b = p1[1] - p2[1]
    c_sq = a*a + b*b
    c = math.sqrt(c_sq)
    return c

def PointOnLine(a, b, dist):
    """ Return the point on the line, @dist from Point @b.
    
    Equation used to find new Point @dist from Point @b
    is C = { B - k(A - B) | k = dist_desired/distance(A, B) }
    Args:
    a: First point in the equation
    b: Point from which resulting Point is calculated
    dist: Distance from Point @b to desired Point
    Returns:
    Point on the line as a tuple in form (x, y)
    """
    dist_a2b = Distance(a, b)
    k = dist / dist_a2b
    a_b = (a[0]-b[0], a[1]-b[1])
    c = (b[0]-(k*a_b[0]), b[1]-(k*a_b[1]))
    return c
