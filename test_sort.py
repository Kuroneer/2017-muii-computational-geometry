#!/usr/bin/env python2

from lilcgal_sort import *
from random import randint, random

def main():
    L = []
    for i in xrange(0,10):
        L.append([randint(0,10), randint(0,10)])

    print(L)
    print(sort_x(L))

    print
    print(sort_vectorDir_dot(L, [1,0]))
    print(sort_vectorDir_dot2(L, [1,0]))
    print(sort_vectorDir_dot_customfun(L, [1,0]))
    print(sort_vectorDir_dot_customlambda(L, [1,0]))
    print(sort_vectorDir_matrixTurn(L, [1,0]))

    print
    print(sort_vectorDir(L, [1, 0]))
    print(sort_vectorDir(L, [0, 1]))

if __name__ == "__main__":
    main()

