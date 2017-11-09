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

num = 6
def main():
    L = []
    for i in xrange(0,num):
        L.append([randint(0,2*num), randint(0,2*num)])

    G = point(L, color = 'red', size = 10)
    DCEL = graham_triangulation_dcel(L)

    Points = DCEL[0]
    Hull = DCEL[1]
    Edges = DCEL[2]
    Faces = DCEL[3]

    print("DCEL Start")
    print("Points")
    for Point in Points:
        print(Point)
    print("Edges")
    for Edge in Edges:
        print(Edge)
    print("Faces")
    for Face in Faces:
        print(Face)
    print("DCEL End")

    for Face in Faces:
        Green = random()
        Blue = random()
        PointsIdList = Face[2]
        PointsList = list(map(lambda PointId : Points[PointId], PointsIdList))
        PointsCoordinatesList = list(map(lambda Point : Point[1], PointsList))
        G += polygon(PointsCoordinatesList, rgbcolor = (0, Green, Blue))
        EdgeIdList = Face[1]
        for Index in xrange(0, len(EdgeIdList)):
            EdgeId = EdgeIdList[Index-1]
            # (id, start point id, end point id, mirror edge id, next edge id, previous edge id, face id that includes it)
            Edge = Edges[EdgeId]

            NextEdgeId = Edge[4]
            assert NextEdgeId == EdgeIdList[Index]
            NextEdgeStartPointId = Edges[NextEdgeId][1]
            assert NextEdgeStartPointId == Edge[2]

            PreviousEdgeId = Edge[5]
            assert PreviousEdgeId == EdgeIdList[Index-2]
            PreviousEdgeEndPointId = Edges[PreviousEdgeId][2]
            assert PreviousEdgeEndPointId == Edge[1]

            MirrorEdgeId = Edge[3]
            MirrorEdge = Edges[MirrorEdgeId]
            assert MirrorEdge[1] == Edge[2]
            assert MirrorEdge[2] == Edge[1]

            assert Edge[6] == Face[0] # Edge is in polygon

            G += arrow(Points[Edge[1]][1], Points[Edge[2]][1], rgbcolor=(1,0,0))

    for EdgeId in Hull:
        Edge = Edges[EdgeId]
        G += arrow(Points[Edge[1]][1], Points[Edge[2]][1], rgbcolor=(0,0,0))

    save(G,'/tmp/dom.png',aspect_ratio=True)
    os.system('feh /tmp/dom.png')

if __name__ == "__main__":
    main()

