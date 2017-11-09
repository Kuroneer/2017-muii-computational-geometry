#!/usr/bin/sage -python

##!/usr/bin/env python2

from lilcgal_polygons import *
from sage.all import *
from random import randint, random
import time


def baricenter(Point0, Point1, Point2):
    Intersection = lineIntersection([Point0, midPoint(Point1, Point2)], [Point1, midPoint(Point0, Point2)])
    if Intersection != None: # sarea != 0
        return Intersection
    if pointCoordinatesBetween(Point0, [Point1, Point2]):
        return Point0
    elif pointCoordinatesBetween(Point1, [Point0, Point2]):
        return Point1
    else:
        return Point2

num = 10
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

    Relations = Ret[3]
    for Relation in Relations:
        Triangle = Relation[1]
        TriangleCenter = baricenter(Triangle[0], Triangle[1], Triangle[2])
        print("Relation {}, Triangle {}, Center {}".format(Relation, Triangle, TriangleCenter))
        for NeighbourIndex in Relation[2]:
            NeighbourTriangle = Relations[NeighbourIndex][1]
            NeighbourCenter = baricenter(NeighbourTriangle[0], NeighbourTriangle[1], NeighbourTriangle[2])
            print("Neighbour {}, Center {}".format(NeighbourTriangle, NeighbourCenter))
            G+= line([TriangleCenter, NeighbourCenter], color = 'white')

    save(G,'/tmp/dom.png',aspect_ratio=True)
    os.system('feh /tmp/dom.png')

if __name__ == "__main__":
    main()

