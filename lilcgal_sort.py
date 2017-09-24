

from lilcgal_basic import *
from math import *

def sort_x(L):
    return sorted(L)

# Vector dir

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

        R = PointA[0] - PointB[0]
        if R == 0:
            return PointA[1] - PointB[1]
        else:
            return R

    return sorted(L, cmp)

def sort_vectorDir_dot_customlambda(L, Vector):
    print("Do not use this function: sort_vectorDir_dot_customlambda")
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
    if len(L) < 20000:
        return sort_vectorDir_dot_tuple(L, V)
    else:
        return sort_vectorDir_dot_customfun(L, V)

# Angle dir

def sort_angleFromPoint_atan2(L, Point):
    X = Point[0]
    Y = Point[1]

    L_wAngle = list(map(lambda Point: (atan2(Point[1] - Y, Point[0] - X) % (2*pi), Point), L))
    L_sorted = sorted(L_wAngle)
    return list(map(lambda AngleTuple: AngleTuple[1], L_sorted))

def sort_angleFromPoint_sarea(L, PointO):
    def cmp(PointA, PointB):
        R = sarea(PointO, PointA, PointB)
        if R >0:
            return 1;
        elif R <0:
            return -1;

        R = PointA[0] - PointB[0]
        if R == 0:
            return PointA[1] - PointB[1]
        else:
            return R

    Lup   = filter(lambda Point: Point[1] >= PointO[1], L)
    Ldown = filter(lambda Point: Point[1] <  PointO[1], L)

    return sorted(Lup, cmp) + sorted(Ldown, cmp)

def sort_angleFromPoint_sarea2(L, PointO):
    def cmp(PointA, PointB):
        RelYA = PointA[1] - PointO[1]
        RelYB = PointB[1] - PointO[1]
        if RelYA * RelYB < 0: #different semis
            if RelYA > 0:
                return -1
            else:
                return 1
        elif RelYA * RelYB == 0: # At least one is 0
            if RelYA < 0:
                return 1
            elif RelYB < 0:
                return -1

        R = sarea(PointO, PointA, PointB)
        if R >0:
            return 1;
        elif R <0:
            return -1;

        R = PointA[0] - PointB[0]
        if R == 0:
            return PointA[1] - PointB[1]
        else:
            return R

    return sorted(L, cmp)

def sort_angleFromPoint(L, P):
    return sort_angleFromPoint_atan2(L, P) # seems to be always faster


# Slope sort
def sort_slope_tuple(L):
    inf = float('inf')
    L_wSlope = list(map(lambda Line: ((Line[1][1] - Line[0][1]) / float(Line[1][0] - Line[0][0]) if (Line[1][0] - Line[0][0]) else inf, Line), L))
    L_sorted = sorted(L_wSlope)
    return list(map(lambda Tuple: Tuple[1], L_sorted))

def sort_slope_cmp(L):
    def cmp(LineA, LineB):
        VectorA = diff(LineA[1], LineA[0])
        VectorB = diff(LineB[1], LineB[0])
        R = VectorB[0] * VectorA[1] - VectorA[0] * VectorB[1]
        if R >0:
            return 1;
        elif R <0:
            return -1;

        if LineA < LineB:
            return -1
        elif LineA > LineB:
            return 1
        else:
            return 0

    return sorted(L, cmp)

def sort_slope(L):
    return sort_slope_tuple(L)

# Proyection sort
def proyection_sort(L, Line):
    return sort_vectorDir(L, diff(Line[1], Line[0]))

# Distance sort
def distance_sort(L, Line):
    A = Line[0]
    B = Line[1]
    L_sorted = sorted(list(map(lambda Point: (abs(sarea(A, B, Point)), Point), L)))
    return list(map(lambda Tuple: Tuple[1], L_sorted))

