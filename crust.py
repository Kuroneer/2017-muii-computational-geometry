#!/usr/bin/sage -python

##!/usr/bin/env python2

from lilcgal_sort import *
import lilcgal_basic
from lilcgal_polygons import *
from sage.all import *
from random import randint, random, shuffle
import scipy.spatial as sp
import math

def fast_crust(Points):
    Delaunay = sp.Delaunay(Points)

    PointsCoordinatesList = Delaunay.points
    Neighbors = Delaunay.neighbors
    Triangles = Delaunay.simplices

    def coordinates(PointId):
        return Points[PointId]

    Crust= []
    NoCrust= []
    for TriangleId in xrange(len(Triangles)):
        for NeighbourTriangleIdPosition in xrange(3):
            NeighborTriangleId = Neighbors[TriangleId][NeighbourTriangleIdPosition]

            EdgeIds = list(Triangles[TriangleId])
            TriangleVertexPointId = EdgeIds.pop(NeighbourTriangleIdPosition)
            EdgeStartPointId = EdgeIds[0]
            EdgeEndPointId = EdgeIds[1]
            TriangleVertexPointCoordinates = coordinates(TriangleVertexPointId)
            EdgeStartCoordinates = coordinates(EdgeStartPointId)
            EdgeEndCoordinates = coordinates(EdgeEndPointId)

            if NeighborTriangleId < 0:
                Crust.append([EdgeStartCoordinates, EdgeEndCoordinates])
                continue

            CandidatePointId = [PointId for PointId in Triangles[NeighborTriangleId] if PointId not in EdgeIds]
            assert len(CandidatePointId) == 1
            CandidatePointId = CandidatePointId.pop()
            CandidatePointCoordinates = coordinates(CandidatePointId)


            # Christopher Gold, Jack Snoeyink: A One-Step Crust and Skeleton Extraction Algorithm.
            # Suppose that (p, q, r) and (r, q, s) are the two triangles incident on Delaunay edge
            # (q, r), and let v be the vector 90 degrees clockwise from (r-q). Then the test
            # (s-q).(s-r) * (p-q).(p-r) >= - (s-r).v * (p-q).v
            # will be true if and only if the edge (q, r) should be in the crust.

            P = TriangleVertexPointCoordinates
            Q = EdgeStartCoordinates
            R = EdgeEndCoordinates
            S = CandidatePointCoordinates

            SQ = lilcgal_basic.diff(Q, S)
            SR = lilcgal_basic.diff(R, S)
            PQ = lilcgal_basic.diff(Q, P)
            PR = lilcgal_basic.diff(R, P)
            Left = (SQ[0] * SR[0] + SQ[1] * SR[1]) * (PQ[0] * PR[0] + PQ[1] * PR[1])
            V = lilcgal_basic.perpendicular(lilcgal_basic.diff(Q,R))
            Right = (SR[0] * V[0] + SR[1] * V[1]) * (PQ[0] * V[0] + PQ[1] * V[1])

            if Left >= - Right:
                Crust.append([EdgeStartCoordinates, EdgeEndCoordinates])
            else:
                NoCrust.append([EdgeStartCoordinates, EdgeEndCoordinates])

    return (Crust, NoCrust)

def print_crust(Points, Crust, NoCrust, Name):
    P = point(Points, color = 'red', zorder = 2)
    for Line in Crust:
      P += line(Line, color = 'black', zorder = 1)
    for Line in NoCrust:
      P += line(Line, color = 'cyan', zorder = 0)

    save(P,Name,aspect_ratio=True)
    print(Name)

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

def main():
    Points = [[cos(pi*i/10), sin(pi*i/10)] for i in xrange(20)]
    Points += [[.2*cos(pi*i/5)+.4, .15*sin(pi*i/5)+.4] for i in xrange(10)]
    Points += [[.2*cos(pi*i/5)-.4, .15*sin(pi*i/5)+.4] for i in xrange(10)]
    Points += [[.6*cos(pi*i/10), .7*sin(pi*i/10)] for i in xrange(12,19)]

    Crust = crust(Points)
    print_crust(Points, Crust[0], Crust[1], '/tmp/crust_trivial.png')
    Crust = fast_crust(Points)
    print_crust(Points, Crust[0], Crust[1], '/tmp/crust_fast.png')

if __name__ == "__main__":
    main()

