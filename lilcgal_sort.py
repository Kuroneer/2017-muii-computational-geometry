

from lilcgal_basic import *
from math import *

def sort_x(L):
    return sorted(L)


def sort_vectorDir_dot(L, Vector):
    X = Vector[0]
    Y = Vector[1]

    L_wDotProduct = list(map(lambda Point: [Point[0]*X + Point[1]*Y, Point], L))
    L_sorted = sorted(L_wDotProduct)
    return list(map(lambda DotProduct: DotProduct[1], L_sorted))

def sort_vectorDir_dot_tuple(L, Vector):
    X = Vector[0]
    Y = Vector[1]

    L_wDotProduct = list(map(lambda Point: (Point[0]*X + Point[1]*Y, Point), L))
    L_sorted = sorted(L_wDotProduct)
    return list(map(lambda DotProduct: DotProduct[1], L_sorted))

def sort_vectorDir_dot2(L, Vector):
    X = Vector[0]
    Y = Vector[1]

    L_wDotProduct = list(map(lambda Point: [Point[0]*X + Point[1]*Y, Point[0], Point[1]], L))
    L_sorted = sorted(L_wDotProduct)
    return list(map(lambda DotProduct: [DotProduct[1], DotProduct[2]], L_sorted))

def sort_vectorDir_dot_customfun(L, Vector):
    X = Vector[0]
    Y = Vector[1]
    def cmp(PointA, PointB):
        R = PointA[0]*X + PointA[1]*Y - PointB[0]*X + PointB[1]*Y
        if R >0:
            return 1;
        elif R <0:
            return -1;
        else:
            R = PointA[0] - PointB[0]
            if R == 0:
                return PointA[1] - PointB[1]
            else:
                return R

    return sorted(L, cmp )

def sort_vectorDir_dot_customlambda(L, Vector):
    # Do not use, it's wrong (int(-0.5) = 0) and does not account for ties
    X = Vector[0]
    Y = Vector[1]
    return sorted(L, lambda PointA, PointB: int(PointA[0]*X + PointA[1]*Y - PointB[0]*X + PointB[1]*Y))

def sort_vectorDir_matrixTurn(L, Vector):
    X = Vector[0]
    Y = Vector[1]
    Angle = atan2(Y, X)
    s = sin(Angle)
    c = cos(Angle)

    L_wDotProduct = list(map(lambda Point: (X*c - Y*s, X*s + Y*c, Point), L))
    L_sorted = sorted(L_wDotProduct)
    return list(map(lambda DotProduct: DotProduct[2], L_sorted))

def sort_vectorDir(L, V):
    return sort_vectorDir_dot_tuple(L, V)

