#!/usr/bin/sage -python

##!/usr/bin/env python2

from lilcgal_polygons import *
from sage.all import *
from random import randint, random
import time

num =  10
def main():
    L = []
    for i in xrange(0,num):
        L.append([randint(0,num), randint(0,num)])

    G = point(L, color = 'red', size = 10)
    Ret = graham_triangulation(L)

    Triangles = Ret[1]
    for Triangle in Triangles:
        G += polygon(Triangle, rgbcolor = (0, random(), random()) )

    Hull = Ret[0]
    G += line(Hull+[Hull[0]], color = 'purple')

    Polygon = Ret[2]
    G += line(Polygon + [Polygon[0]], color = 'red')

    save(G,'/tmp/dom.png',aspect_ratio=True)
    os.system('feh /tmp/dom.png')

if __name__ == "__main__":
    main()

