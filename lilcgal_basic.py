

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
    return (sarea(PointO, PointA, PointB) == 0) and pointCoordinatesBetween(PointO, Segment)

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

def pointCoordinatesBetween(PointO, Segment):
    PointA = Segment[0]
    PointB = Segment[1]
    return ((PointA[0] <= PointO[0] <= PointB[0]) or (PointB[0] <= PointO[0] <= PointA[0])) \
            and ((PointA[1] <= PointO[1] <= PointB[1]) or (PointB[1] <= PointO[1] <= PointA[1]))

def segmentIntersectionTest(Segment0, Segment1):
    # Two segments cross each other if both ends of one are at different sides
    # of the other
    A1 = sarea(Segment0[0], Segment0[1], Segment1[0])
    A2 = sarea(Segment0[0], Segment0[1], Segment1[1])
    A3 = sarea(Segment1[0], Segment1[1], Segment0[0])
    A4 = sarea(Segment1[0], Segment1[1], Segment0[1])

    if A1 or A2 or A3 or A4:
        return (A1 * A2 <= 0) and (A3 * A4 <= 0)

    # Segments are in the same line
    return pointCoordinatesBetween(Segment0[0], Segment1) \
            or pointCoordinatesBetween(Segment0[1], Segment1) \
            or pointCoordinatesBetween(Segment1[0], Segment0) \
            or pointCoordinatesBetween(Segment1[1], Segment0)


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

def diff(Point0, Point1):
    return [Point1[0] - Point0[0], Point1[1] - Point0[1]]
def sumV(Point0, Point1):
    return [Point1[0] + Point0[0], Point1[1] + Point0[1]]
def perpendicular(Vector):
    return [Vector[1], -Vector[0]]
def mediatriz(Segment):
    Point0 = Segment[0]
    Point1 = Segment[1]
    Vector = diff(Point0, Point1)
    Perpend = perpendicular(Vector)
    MidPoint = midPoint(Point0, Point1)
    return [MidPoint, sumV(MidPoint, Perpend)]

def circumcenter(Point0, Point1, Point2):
    M0 = mediatriz([Point2, Point0])
    M1 = mediatriz([Point2, Point1])
    return lineIntersection(M0, M1)

def inCircle_dist2(Point0, Point1, Point2, PointO):
    Circumcenter = circumcenter(Point0, Point1, Point2)
    if Circumcenter == None:
        return None
    return dist2(Point0, Circumcenter) - dist2(PointO, Circumcenter)

def inCircle_det(Point0, Point1, Point2, PointO):
    SArea = sarea(Point0, Point1, Point2)
    if not SArea:
        return None
    # |  1  1  1  1 |
    # | x0 x1 x2 xO |
    # | y0 y1 y2 yO | =
    # | z0 z1 z2 zO |
    #
    # With Z = x^2 + y^2
    #
    # |  1     0     0     0 |
    # | x0 x1-x0 x2-x0 xO-x0 |
    # | y0 y1-y0 y2-y0 yO-y0 | =
    # | z0 z1-z0 z2-z0 zO-z0 |
    #
    # | x1-x0 x2-x0 xO-x0 |
    # | y1-y0 y2-y0 yO-y0 |
    # | z1-z0 z2-z0 zO-z0 |

    def getZ(Point):
        return Point[0] * Point[0] + Point[1] * Point[1]

    x0 = Point0[0]
    y0 = Point0[1]
    z0 = getZ(Point0)
    x1 = Point1[0]
    y1 = Point1[1]
    z1 = getZ(Point1)
    x2 = Point2[0]
    y2 = Point2[1]
    z2 = getZ(Point2)
    xO = PointO[0]
    yO = PointO[1]
    zO = getZ(PointO)

    e11 = x1-x0
    e12 = x2-x0
    e13 = xO-x0
    e21 = y1-y0
    e22 = y2-y0
    e23 = yO-y0
    e31 = z1-z0
    e32 = z2-z0
    e33 = zO-z0

    det = e11 * e22 * e33 + e12 * e23 * e31 + e13 * e21 * e32 - e13 * e22 * e31 - e12 * e21 * e33 - e11 * e23 * e32

    return (SArea * det)

def inCircle(Point0, Point1, Point2, PointO):
    return inCircle_det(Point0, Point1, Point2, PointO)

