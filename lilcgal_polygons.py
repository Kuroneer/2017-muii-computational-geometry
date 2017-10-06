
from lilcgal_sort import *
import random
from itertools import tee, izip


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def remove_duplicated_points(Points):
    return list(set(Points))

def sort_angleFromPoint(L, Point):
    X = Point[0]
    Y = Point[1]

    L_wAngle = list(map(lambda Point: (atan2(Point[1] - Y, Point[0] - X) % (2*pi), (Point[1]-Y)**2 + (Point[0]-X)**2, Point), L))
    return list(map(lambda AngleTuple: AngleTuple[2], sorted(L_wAngle)))

def createPolygonFromSortedPoints(Points):
    print(Points)
    return [[X, Y] for X,Y in pairwise(Points) if X != Y]+[[Points[-1],Points[0]]]

def build_polygon_rotsort(Points, Vertex = None):
    if Vertex == None:
        Vertex = midPoint(Points[0], midPoint(Points[1], Points[2]))
    # print("Building around {}".format(Vertex))
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


