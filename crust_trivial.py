#!/usr/bin/sage -python

##!/usr/bin/env python2

from lilcgal_sort import *
import lilcgal_basic
from lilcgal_polygons import *
from sage.all import *
from random import randint, random, shuffle
import scipy.spatial as sp
import math

def crust(OriginalPointsCoordinatesList):
    Voronoi = sp.Voronoi(OriginalPointsCoordinatesList)
    AllPoints = list(OriginalPointsCoordinatesList)
    for Vertex in Voronoi.vertices:
        AllPoints.append([Vertex[0], Vertex[1]])
    AllDelaunay = sp.Delaunay(AllPoints)

    PointsCoordinatesList = AllDelaunay.points
    Crust= []
    NoCrust= []
    for PointId in xrange(len(PointsCoordinatesList)):
        PointCoordinates = PointsCoordinatesList[PointId]
        NeighboursIds = AllDelaunay.vertex_neighbor_vertices[1][AllDelaunay.vertex_neighbor_vertices[0][PointId]:AllDelaunay.vertex_neighbor_vertices[0][PointId+1]]
        for NeighbourId in NeighboursIds:
            if PointId < len(OriginalPointsCoordinatesList) and NeighbourId < len(OriginalPointsCoordinatesList):
                Crust.append([AllPoints[PointId], AllPoints[NeighbourId]])
            else:
                NoCrust.append([AllPoints[PointId], AllPoints[NeighbourId]])

    return (Crust, NoCrust)


def print_crust(Points, Crust, NoCrust):
    P = point(Points, color = 'red', zorder = 2)
    for Line in Crust:
      P += line(Line, color = 'black', zorder = 1)
    for Line in NoCrust:
      P += line(Line, color = 'cyan', zorder = 0)

    Name = '/tmp/crust.png'
    save(P,Name,aspect_ratio=True)
    print(Name)

def main():
    Points = [[cos(pi*i/10), sin(pi*i/10)] for i in xrange(20)]
    Points += [[.2*cos(pi*i/5)+.4, .15*sin(pi*i/5)+.4] for i in xrange(10)]
    Points += [[.2*cos(pi*i/5)-.4, .15*sin(pi*i/5)+.4] for i in xrange(10)]
    Points += [[.6*cos(pi*i/10), .7*sin(pi*i/10)] for i in xrange(12,19)]
    Crust = crust(Points)
    print_crust(Points, Crust[0], Crust[1])

if __name__ == "__main__":
    main()

