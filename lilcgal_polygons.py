
from lilcgal_sort import *
import random
from itertools import tee, izip
from math import atan2

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def remove_duplicated_points(Points):
    return list(set(Points))

def createPolygonFromSortedPoints(Points, polygons_as_segments = False):
    if polygons_as_segments:
        return [[X, Y] for X,Y in pairwise(Points) if X != Y]+[[Points[-1],Points[0]]]
    else:
        return Points

def sort_angleFromPoint(L, Point):
    X = Point[0]
    Y = Point[1]

    L_wAngle = list(map(lambda Point: (atan2(Point[1] - Y, Point[0] - X) % (2*pi), (Point[1]-Y)**2 + (Point[0]-X)**2, Point), L))
    return list(map(lambda AngleTuple: AngleTuple[2], sorted(L_wAngle)))

def build_polygon_rotsort(Points, Vertex = None):
    if Vertex == None:
        Vertex = midPoint(Points[0], midPoint(Points[1], Points[2]))
    Points = sort_angleFromPoint(Points, Vertex)
    return createPolygonFromSortedPoints(Points)

def build_polygon_direction(Points, Vector):
    SortedPoints = sort_vectorDir(Points, Vector)

    Max = SortedPoints.pop(-1)
    Min = SortedPoints.pop(1)

    Lup   = filter(lambda Point: sarea(Point, Max, Min) >  0, SortedPoints)
    Ldown = filter(lambda Point: sarea(Point, Max, Min) <= 0, SortedPoints)

    return createPolygonFromSortedPoints([Min] + Lup + [Max] + list(reversed(Ldown)))


# def build_polygon_shuffle_and_fix(Points):
#     SuffledPoints = random.shuffle(Points)
#     CandidatePolygon = createPolygonFromSortedPoints(ShuffledPoints)
#     finished = False
#     while not finished:
#         finished = True
#         for Segment1 in CandidatePolygon:
#             for Segment2 in CandidatePolygon:
#                 if Segment1 != Segment2:
#                     # Check if segments intersect in middle
#                     if segmentIntersectionTest(Segment1, Segment2) \
#                             and not (Seg


#     return

def clipping_line(Polygon, Line):
    if len(Polygon) == 0:
        return []

    AddedLast = Polygon[0] != Polygon[-1]
    if AddedLast:
        Polygon.append(Polygon[0])

    Clipping = []
    A = Line[0]
    B = Line[1]
    PreviousPoint = None
    PreviousSign = None

    for Point in Polygon:
        # print("Checking point {}".format(Point))
        SArea = sarea(A, B, Point)

        if PreviousPoint != None:
            if SArea * PreviousSign < 0:
                Intersection = lineIntersection(Line, [PreviousPoint, Point])
                # print("Added intersection from {} and {}: {} (PreviousSign is {}".format(PreviousPoint, Point, Intersection, PreviousSign))
                Clipping.append(Intersection)
            if SArea >= 0:
                # print("Added point {}".format(Point))
                Clipping.append(Point)

        PreviousPoint = Point
        PreviousSign = SArea

    if AddedLast:
        Polygon.pop(-1)

    return Clipping

def clipping_polygon(PolygonBase, PolygonClipper):
    PolygonCopy = list(PolygonBase)

    AddedLast = PolygonClipper[0] != PolygonClipper[-1]
    if AddedLast:
        PolygonClipper.append(PolygonClipper[0])

    for X,Y in pairwise(PolygonClipper):
        PolygonCopy = clipping_line(PolygonCopy, [Y,X])

    if AddedLast:
        PolygonClipper.pop(-1)

    return PolygonCopy

def core(Polygon):
    return clipping_polygon(Polygon, Polygon)


# Hull:

def modIncrement(Value, Modulus, Increment = 1):
    return (Value + Increment) % Modulus

def convex_hull(Polygon): # Polygon must be monotonic or radial
    Hull = []

    StartIndex = Polygon.index(min(Polygon, key = lambda P: P[1]))
    Hull.append(Polygon[StartIndex])

    CurrentIndex = modIncrement(StartIndex, len(Polygon))
    while True:
        Current = Polygon[CurrentIndex]

        if len(Hull) >= 2 and sarea(Hull[-2], Hull[-1], Current) > 0:
            Hull.pop()
        else:
            if CurrentIndex == StartIndex:
                break
            Hull.append(Current)
            CurrentIndex = modIncrement(CurrentIndex, len(Polygon))

    return Hull

def slow_convex_hull(PolygonBase):
    Polygon = list(PolygonBase)
    Hull = []

    Start = min(Polygon, key = lambda P: P[1])
    Hull.append(Start)
    Angle = 0

    while True:
        Vertex = Hull[-1]
        NextValue = None

        for Point in Polygon:
            PointValue = ((atan2(Point[1] - Vertex[1], Point[0] - Vertex[0]) - Angle) % (2*pi), (Point[1]-Vertex[1])**2 + (Point[0]-Vertex[0])**2, Point)
            if Point != Vertex and (NextValue == None or PointValue < NextValue):
                NextValue = PointValue

        Angle = NextValue[0]
        Next = NextValue[2]

        if Next == Start:
            break

        Hull.append(Next);

    return Hull


