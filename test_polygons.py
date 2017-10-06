#!/usr/bin/sage -python

##!/usr/bin/env python2

from lilcgal_polygons import *
from sage.all import *
from random import randint, random
import time

def main():
    L = []
    for i in xrange(0,10):
        L.append([randint(0,10), randint(0,10)])

    print(L)
    G = point(L, color = 'red', size = 10)

    # Polygon = build_polygon_rotsort(L)
    Polygon = build_polygon_direction(L, [randint(0,10), randint(0,10)])
    print(Polygon)
    for Line in Polygon:
        G += line(Line)

    save(G,'/tmp/dom.png',aspect_ratio=True)
    os.system('feh /tmp/dom.png')

if __name__ == "__main__":
    main()

