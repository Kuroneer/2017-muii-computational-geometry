#!/usr/bin/sage -python

##!/usr/bin/env python2

from lilcgal_polygons import *
from sage.all import *
from random import randint, random
import time

num = 20
def main():
    L = []
    for i in xrange(0,num):
        L.append([randint(0,num), randint(0,num)])

    G = point(L, color = 'red', size = 10)

    Polygon = build_polygon_rotsort(L)
    # Polygon = build_polygon_direction(L, [randint(0,10), randint(0,10)])

    G += line(Polygon + [Polygon[0]])

    Partition = [[0, num/2], [num, num/2]]
    G += line(Partition, color='black')

    Clipping = clipping_line(Polygon, Partition)
    G+= polygon(Clipping, color = 'green')

    Core = core(Polygon)
    G += point(Core, color = 'cyan', size = 10)
    G += polygon(Core, color = 'cyan')

    save(G,'/tmp/dom.png',aspect_ratio=True)
    os.system('feh /tmp/dom.png')

if __name__ == "__main__":
    main()

