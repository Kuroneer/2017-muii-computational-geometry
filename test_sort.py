#!/usr/bin/sage -python

##!/usr/bin/env python2

from lilcgal_sort import *
from sage.all import *
from random import randint, random
import time

def main():
    L = []
    for i in xrange(0,10):
        L.append([randint(0,10), randint(0,10)])

    print(L)
    G = point(L, color = 'red', size = 10)
    XSort = sort_x(L)
    print(XSort)
    # G += line(XSort)

    print
    print(sort_vectorDir_dot(L, [1,0]))
    print(sort_vectorDir_dot2(L, [1,0]))
    print(sort_vectorDir_dot_customfun(L, [1,0]))
    # print(sort_vectorDir_dot_customlambda(L, [1,0]))
    print(sort_vectorDir_matrixTurn(L, [1,0]))

    print
    VectorSort = sort_vectorDir(L, [1, 0])
    print(VectorSort)
    # G += line(VectorSort)
    VectorSort = sort_vectorDir(L, [0, 1])
    print(VectorSort)
    # G += line(VectorSort)

    print
    AngleSort = sort_angleFromPoint_atan2(L, [5,5])
    print(AngleSort)
    # G += line(AngleSort)
    AngleSort = sort_angleFromPoint_sarea(L, [5,5])
    print(AngleSort)
    # G += line(AngleSort)
    print(sort_angleFromPoint_atan2([[4,4],[3,3],[5,5],[6,6],[1,1],[2,2],[7,7],[0,8]], [5,5]))
    print(sort_angleFromPoint_sarea([[4,4],[3,3],[5,5],[6,6],[1,1],[2,2],[7,7],[0,8]], [5,5]))
    print(sort_angleFromPoint_sarea2([[4,4],[3,3],[5,5],[6,6],[1,1],[2,2],[7,7],[0,8]], [5,5]))

    print
    L.append([0,10])
    print(sort_angleFromPoint_atan2(L, [0,0]))
    LL = [[[0,0],X] for X in L]
    SlopeSort = sort_slope_tuple(LL)
    print(list(map(lambda Tuple: Tuple[1], SlopeSort)))
    SlopeSort = sort_slope_cmp(LL)
    print(list(map(lambda Tuple: Tuple[1], SlopeSort)))

    print
    ProyectionLine = [[0,6],[5,0]]
    # G += line(ProyectionLine, color= 'red')
    ProyectionSort = proyection_sort(L, ProyectionLine)
    # G += line(ProyectionSort)
    print(ProyectionSort)

    print
    DistanceLine = [[0,8],[8,0]]
    G += line(DistanceLine, color= 'red')
    DistanceSort = distance_sort(L, DistanceLine)
    G += line(DistanceSort)
    print(DistanceSort)

    save(G,'/tmp/dom.png',aspect_ratio=True)
    os.system('feh /tmp/dom.png')


if __name__ == "__main__":
    main()

