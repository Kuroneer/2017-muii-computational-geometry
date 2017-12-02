#!/usr/bin/sage -python

##!/usr/bin/env python2

from lilcgal_polygons import *
from sage.all import *
from random import randint, random
import time

num = 30
def print_dcel(DCEL, Context = [], DrawArrows = False, SavePNG = True):
    Points = DCEL[0]
    Hull = DCEL[1]
    Edges = DCEL[2]
    Faces = DCEL[3]

    if len(Context) == 0:
        Context.append(-1) # iteration
        Context.append([None]*len(Faces)) # colors
    Context[0] += 1
    Iteration = Context[0]
    Colors = Context[1]

    PointsCoordinatesList = list(map(lambda Point : Point[1], Points))
    G = point(PointsCoordinatesList, color='red',  size = 10)

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
        FaceId = Face[0]
        FaceColors = Colors[FaceId]
        if FaceColors == None:
            Green = random() * 0.8 + 0.2
            Blue = random() * 0.8 + 0.2
            Colors[FaceId]= [Green, Blue]
        else:
            Green = FaceColors[0]
            Blue = FaceColors[1]

        PointsIdList = Face[2]
        PointsList = list(map(lambda PointId : Points[PointId], PointsIdList))
        PointsCoordinatesList = list(map(lambda Point : Point[1], PointsList))
        PolygonGreen = 0
        if not DrawArrows:
            PolygonGreen = Green
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

            if DrawArrows:
                G += arrow(Points[Edge[1]][1], Points[Edge[2]][1], rgbcolor=(0,Green,0), width=1)

    if DrawArrows:
        for EdgeId in Hull:
            Edge = Edges[EdgeId]
            G += arrow(Points[Edge[1]][1], Points[Edge[2]][1], rgbcolor=(0,0,0))

    if SavePNG:
        Name = '/tmp/dom{0:03d}.png'.format(Iteration)
        save(G,Name,aspect_ratio=True, xmin=-1, ymin=-1, xmax = num+1, ymax = num+1)
        print(Name)

def print_voronoi(DCEL):
    Points = DCEL[0]

    PointsCoordinatesList = list(map(lambda Point : Point[1], Points))
    G = point(PointsCoordinatesList, color='red',  size = 10, zorder = 10)

    VoronoiPolygons = voronoi_polygons(DCEL)
    for Polygon in VoronoiPolygons:
        G += polygon(Polygon, rgbcolor = (0, random(), random()), zorder = 0)

    Name = '/tmp/domvoronoi.png'
    save(G,Name,aspect_ratio=True, xmin=-1, ymin=-1, xmax = num+1, ymax = num+1)
    print(Name)

def main():
    L = []
    for i in xrange(0,num):
        L.append([randint(0,num), randint(0,num)])

    DCEL = graham_triangulation_dcel(L)

    print_dcel(DCEL)

    print("Improving DCEL")
    while improve_triangulation(DCEL, False):
        print_dcel(DCEL, SavePNG = False)

    print("Improved")
    print_dcel(DCEL)

    print_voronoi(DCEL)

if __name__ == "__main__":
    main()

