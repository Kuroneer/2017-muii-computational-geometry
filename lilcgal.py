

from functools import reduce
from math import *


# Distances

def dist2_generic( PointA, PointB ):
    return reduce(lambda a,b : a+b, list(map(lambda a, b: (a-b)**2, PointA, PointB)))

def dist2_dim2( PointA, PointB ):
    return (PointA[0] - PointB[0])**2 + (PointA[1] - PointB[1])**2

def dist2(PointA, PointB):
    return dist2_dim2(PointA, PointB)

def dist(PointA, PointB):
    return sqrt(dist2(PointA, PointB))



# Triangle area

def area_trig(PointA, PointB, PointC):
    lengthB = dist(PointA, PointB)
    lengthC = dist(PointA, PointC)

    if (lengthB * lengthC) == 0:
        return 0 # Triangle with one side 0 has no area

    # Move A to origin (Avoid modifying given points, as they are passed as
    # reference)
    B0 = PointB[0] - PointA[0]
    B1 = PointB[1] - PointA[1]
    C0 = PointC[0] - PointA[0]
    C1 = PointC[1] - PointA[1]

    # angle A with dot product (Segments go from A to B and from A to C)
    AngleA = acos((B0 * C0 + B1 * C1) / (lengthB * lengthC))

    # traditional triangle area
    return lengthB * (sin(AngleA) * lengthC) * .5

def sangle_trig(PointA, PointB, PointC):
    # Move A to origin (Avoid modifying given points, as they are passed as
    # reference)
    B0 = PointB[0] - PointA[0]
    B1 = PointB[1] - PointA[1]
    C0 = PointC[0] - PointA[0]
    C1 = PointC[1] - PointA[1]
    return atan2(B1, B0) - atan2(C1, C0)

def sarea_trig(PointA, PointB, PointC):
    lengthB = dist(PointA, PointB)
    lengthC = dist(PointA, PointC)

    # get signed angle A with atan2
    AngleA = sangle_trig(PointA, PointB, PointC)

    # traditional triangle area
    return lengthB * (sin(AngleA) * lengthC) * .5

def sarea_crossvector(PointA, PointB, PointC):
    # Move A to origin (Avoid modifying given points, as they are passed as
    # reference)
    B0 = PointB[0] - PointA[0]
    B1 = PointB[1] - PointA[1]
    C0 = PointC[0] - PointA[0]
    C1 = PointC[1] - PointA[1]
    # Since All points are on the Z = 0 plane, the cross vector only has z
    # component, which is
    z = B0 * C1 - C0 * B1
    return z * -.5 # triangle area and consistent sign

def sarea(PointA, PointB, PointC):
    return sarea_crossvector(PointA, PointB, PointC)

def orientation(PointA, PointB, PointC):
    area = sarea_crossvector(PointA, PointB, PointC)
    if area > 0:
        return 1
    elif area < 0:
        return -1
    else:
        return 0

def midPoint(PointA, PointB):
    return [(PointA[0] + PointB[0])*.5, (PointA[1] + PointB[1])*.5]

def inSegment(PointO, Segment):
    # a point in a segment if the triangle area is 0 and its coordinates
    # are between each segment end point
    PointA = Segment[0]
    PointB = Segment[1]
    return (sarea(PointO, PointA, PointB) == 0) \
            and ((PointA[0] <= PointO[0] <= PointB[0]) or (PointB[0] <= PointO[0] <= PointA[0])) \
            and ((PointA[1] <= PointO[1] <= PointB[1]) or (PointB[1] <= PointO[1] <= PointA[1]))

def inConvexPolygon(PointO, ConvexPolygon):
    # A point is in a convex polygon if while we follow the polygon, it's always on
    # the same side
    vertexIterator = iter(ConvexPolygon)
    PreviousVertex = next(vertexIterator)
    side = sarea(PointO, ConvexPolygon[-1], PreviousVertex)
    for Vertex in vertexIterator:
        currentSide = sarea(PointO, PreviousVertex, Vertex)
        PreviousVertex = Vertex
        if side == 0:
            side = currentSide
        elif side * currentSide < 0:
            return False

    return True

def inTriangle(Point0, Triangle):
    return inConvexPolygon(Point0, Triangle)

def segmentIntersectionTest(Segment0, Segment1):
    # Two segments croos each other if both ends of one are at different sides
    # of the other
    return ((sarea(Segment0[0], Segment0[1], Segment1[0]) \
            * sarea(Segment0[0], Segment0[1], Segment1[1])) <= 0) \
            and ((sarea(Segment1[0], Segment1[1], Segment0[0]) \
            * sarea(Segment1[0], Segment1[1], Segment0[1])) <= 0)

def segmentIntersectionTest_orientations(Segment0, Segment1):
    # Same as above but with orientations
    return ((orientation(Segment0[0], Segment0[1], Segment1[0]) \
            * orientation(Segment0[0], Segment0[1], Segment1[1])) <= 0) \
            and ((orientation(Segment1[0], Segment1[1], Segment0[0]) \
            * orientation(Segment1[0], Segment1[1], Segment0[1])) <= 0)

def lineIntersection(Line0, Line1):
    # The intersection point solves both line equatons, and also, the sarea of
    # the resulting point and both line points is 0

    # ResX, ResY

    # Area from Line0
    A0x = Line0[0][0]
    A0y = Line0[0][1]
    A1x = Line0[1][0]
    A1y = Line0[1][1]
    ax = A1x - A0x
    ay = A1y - A0y
    # cx = ResX - A0x
    # cy = ResY - A0y
    # ax * cy = cx * ay
    # Doing the same with Line1 and combining both to extract ResX:

    B0x = Line1[0][0]
    B0y = Line1[0][1]
    B1x = Line1[1][0]
    B1y = Line1[1][1]
    bx = B1x - B0x
    by = B1y - B0y

    D = ax * by - bx * ay
    if (D == 0): # Both lines have the same slope
        return None

    # ResX = (ax * bx * A0y - ax * bx * B0y - ay * bx * A0x + ax * by * B0x) / D
    ResX = (ax * (bx * (A0y - B0y) + by * B0x) - ay * bx * A0x) / D

    if (bx == 0):
        ResY = (ay / ax) * (ResX - A0x) + A0y
    else:
        ResY = (by / bx) * (ResX - B0x) + B0y

    return [ResX, ResY]

