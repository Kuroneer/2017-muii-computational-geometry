#!/usr/bin/sage -python

##!/usr/bin/env python2

from lilcgal_sort import *
import lilcgal_basic
from lilcgal_polygons import *
from sage.all import *
from random import randint, random, shuffle
import scipy.spatial as sp
import math

def voronoi_polygons(Delaunay):
    def external(StartPointCoordinates, EndPointCoordinates):
        Perpendicular = perpendicular(lilcgal_basic.diff(EndPointCoordinates, StartPointCoordinates))
        VectorLength = dist(StartPointCoordinates, EndPointCoordinates)
        Perpendicular100U = [100 * Perpendicular[0] / VectorLength, 100 * Perpendicular[1] / VectorLength]
        return sumV(midPoint(StartPointCoordinates, EndPointCoordinates), Perpendicular100U)

    PointsCoordinatesList = Delaunay.points
    VoronoiPolygons = []
    for PointId in xrange(len(PointsCoordinatesList)):
        PointCoordinates = PointsCoordinatesList[PointId]
        NeighboursIds = Delaunay.vertex_neighbor_vertices[1][Delaunay.vertex_neighbor_vertices[0][PointId]:Delaunay.vertex_neighbor_vertices[0][PointId+1]]
        NeighboursCoordinates = list(map(lambda PointId : PointsCoordinatesList[PointId], NeighboursIds))
        NeighboursCoordinatesSorted = sort_angleFromPoint(NeighboursCoordinates, PointCoordinates)

        VoronoiRegionCoordinates = []
        for NeighbourCoordinatesIndex in xrange(len(NeighboursCoordinatesSorted)):
            NeighbourCoordinates = NeighboursCoordinatesSorted[NeighbourCoordinatesIndex]
            PreviousNeighbourCoordinates = NeighboursCoordinatesSorted[NeighbourCoordinatesIndex-1]
            if sarea(NeighbourCoordinates, PointCoordinates, PreviousNeighbourCoordinates) < 0:
                VoronoiRegionCoordinates.append(circumcenter(PointCoordinates, NeighbourCoordinates, PreviousNeighbourCoordinates))
            else:
                VoronoiRegionCoordinates.append(external(PointCoordinates, PreviousNeighbourCoordinates))
                VoronoiRegionCoordinates.append(external(NeighbourCoordinates, PointCoordinates))

        VoronoiPolygons.append(VoronoiRegionCoordinates)

    return VoronoiPolygons

def generate_sub_voronoi(PointsCoordinates, boundingBoxCoordinates = None, Depth = 0, Rstart=.1, Rend=.9, Gstart=.1, Gend=.9, Bstart=.1, Bend=.9):
    Delaunay = sp.Delaunay(PointsCoordinates)
    VoronoiPolygons = voronoi_polygons(Delaunay)
    if boundingBoxCoordinates != None:
        VoronoiPolygons = [ clipping_polygon(Polygon, boundingBoxCoordinates) for Polygon in VoronoiPolygons ]
        VoronoiPolygons = [ Polygon for Polygon in VoronoiPolygons if Polygon != [] ]

    if len(VoronoiPolygons) == 0:
        return ([boundingBoxCoordinates], [[Rstart,Rend,Gstart,Gend,Bstart,Bend]],[Depth+1])

    ColorStep = (int) (math.ceil(len(VoronoiPolygons) ** (1./3.)))
    Rrange = (Rend -Rstart) / ColorStep
    Grange = (Gend -Gstart) / ColorStep
    Brange = (Bend -Bstart) / ColorStep
    PolygonColors = []
    for R in xrange(ColorStep):
        for G in xrange(ColorStep):
            for B in xrange(ColorStep):
                PolygonColors.append([ \
                        Rstart + R * Rrange, Rstart + (R+1) * Rrange, \
                        Gstart + G * Grange, Gstart + (G+1) * Grange, \
                        Bstart + B * Brange, Bstart + (B+1) * Brange])
    shuffle(PolygonColors)
    while len(PolygonColors) > len(VoronoiPolygons):
        PolygonColors.pop()
    return (VoronoiPolygons, PolygonColors, [Depth+1 for i in xrange(len(VoronoiPolygons))])

N=0
def print_voronoi(Polygons, PolygonColors = None, GeneratorCoordinates = None):
    global N
    G = None
    if GeneratorCoordinates != None:
        G = point(GeneratorCoordinates, color='black',  size = 10, zorder = 10)

    PolygonId = 0
    for Polygon in Polygons:
        Color = (random(), random(), random())
        if PolygonColors != None:
            Row = PolygonColors[PolygonId]
            Color = ((Row[0] + Row[1])/2, (Row[2] + Row[3])/2, (Row[4] + Row[5])/2)
        P = polygon(Polygon, rgbcolor = Color, zorder = 0)
        if G == None:
            G = P
        else:
            G +=P
        PolygonId += 1

    Name = '/tmp/domvoronoi{0:04d}.png'.format(N)
    N += 1
    save(G,Name,aspect_ratio=True)
    print(Name)


def art_step(CurrentPolygons, CurrentPolygonsColors, CurrentPolygonsDepth, PolygonIndex, NPoints):
    BoundingBoxCoordinates = CurrentPolygons[PolygonIndex]
    BoundingBoxColors = CurrentPolygonsColors[PolygonIndex]
    BoundingBoxDepth = CurrentPolygonsDepth[PolygonIndex]

    X = list(map(lambda Point: Point[0], BoundingBoxCoordinates))
    Y = list(map(lambda Point: Point[1], BoundingBoxCoordinates))
    maxX = max(X)
    maxY = max(Y)
    minX = min(X)
    minY = min(Y)
    L = [ [random()*(maxX-minX)+minX, random()*(maxY-minY)+minY] for i in xrange(NPoints) ]

    print_voronoi(CurrentPolygons, CurrentPolygonsColors, L)

    SubVoronoi = generate_sub_voronoi(\
            L,\
            BoundingBoxCoordinates,\
            BoundingBoxDepth,\
            BoundingBoxColors[0],\
            BoundingBoxColors[1],\
            BoundingBoxColors[2],\
            BoundingBoxColors[3],\
            BoundingBoxColors[4],\
            BoundingBoxColors[5])

    PolygonsInserted = len(SubVoronoi[0])

    CurrentPolygons.pop(PolygonIndex)
    CurrentPolygonsColors.pop(PolygonIndex)
    CurrentPolygonsDepth.pop(PolygonIndex)
    while len(SubVoronoi[0]) > 0:
        CurrentPolygons.append(SubVoronoi[0].pop())
        CurrentPolygonsColors.append(SubVoronoi[1].pop())
        CurrentPolygonsDepth.append(SubVoronoi[2].pop())

    print_voronoi(CurrentPolygons, CurrentPolygonsColors, L)
    print_voronoi(CurrentPolygons, CurrentPolygonsColors, [])
    return PolygonsInserted

Range = 8
WidthSearch = False
MaxDepth = 4
def main():
    Polygons = [[[0,Range],[0, 0],[Range,0],[Range, Range]]]
    Colors = [[.1,.9,.1,.9,.1,.9]]
    Depths = [0]

    if WidthSearch:
        while Depths[0] < MaxDepth:
            art_step(Polygons,Colors,Depths, 0,Range)
    else:
        Index = -1
        # TODO Improve this to avoid searching every time
        while -Index <= len(Polygons):
            if Depths[Index] < MaxDepth:
                art_step(Polygons,Colors,Depths, Index, Range)
                Index = -1
            else:
                Index -= 1

    return

if __name__ == "__main__":
    main()

