
from lilcgal_sort import *
import random
from itertools import tee, izip
from math import atan2

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

def createPolygonFromSortedPoints(Points, polygons_as_segments = False):
    if polygons_as_segments:
        return [[X, Y] for X,Y in pairwise(Points) if X != Y]+[[Points[-1],Points[0]]]
    else:
        return Points

def sort_angleFromPoint(L, Point):
    X = Point[0]
    Y = Point[1]

    L_wAngle = list(map(lambda Point: (atan2(Point[1] - Y, Point[0] - X) % (2*pi), (Point[1]-Y)**2 + (Point[0]-X)**2, Point), L))
    return list(map(lambda AngleTuple: AngleTuple[2], sorted(L_wAngle)))

def build_polygon_rotsort(Points, Vertex = None):
    if Vertex == None:
        Vertex = midPoint(Points[0], midPoint(Points[1], Points[2]))
    Points = sort_angleFromPoint(Points, Vertex)
    return createPolygonFromSortedPoints(Points)

def build_polygon_direction(Points, Vector):
    SortedPoints = sort_vectorDir(Points, Vector)

    Max = SortedPoints.pop(-1)
    Min = SortedPoints.pop(1)

    Lup   = filter(lambda Point: sarea(Point, Max, Min) >  0, SortedPoints)
    Ldown = filter(lambda Point: sarea(Point, Max, Min) <= 0, SortedPoints)

    return createPolygonFromSortedPoints([Min] + Lup + [Max] + list(reversed(Ldown)))


# def build_polygon_shuffle_and_fix(Points):
#     SuffledPoints = random.shuffle(Points)
#     CandidatePolygon = createPolygonFromSortedPoints(ShuffledPoints)
#     finished = False
#     while not finished:
#         finished = True
#         for Segment1 in CandidatePolygon:
#             for Segment2 in CandidatePolygon:
#                 if Segment1 != Segment2:
#                     # Check if segments intersect in middle
#                     if segmentIntersectionTest(Segment1, Segment2) \
#                             and not (Seg


#     return

def clipping_line(Polygon, Line):
    if len(Polygon) == 0:
        return []

    AddedLast = Polygon[0] != Polygon[-1]
    if AddedLast:
        Polygon.append(Polygon[0])

    Clipping = []
    A = Line[0]
    B = Line[1]
    PreviousPoint = None
    PreviousSign = None

    for Point in Polygon:
        SArea = sarea(A, B, Point)

        if PreviousPoint != None:
            if SArea * PreviousSign < 0:
                Intersection = lineIntersection(Line, [PreviousPoint, Point])
                Clipping.append(Intersection)
            if SArea >= 0:
                Clipping.append(Point)

        PreviousPoint = Point
        PreviousSign = SArea

    if AddedLast:
        Polygon.pop(-1)

    return Clipping

def clipping_polygon(PolygonBase, PolygonClipper):
    PolygonCopy = list(PolygonBase)

    AddedLast = PolygonClipper[0] != PolygonClipper[-1]
    if AddedLast:
        PolygonClipper.append(PolygonClipper[0])

    for X,Y in pairwise(PolygonClipper):
        PolygonCopy = clipping_line(PolygonCopy, [Y,X])

    if AddedLast:
        PolygonClipper.pop(-1)

    return PolygonCopy

def core(Polygon):
    return clipping_polygon(Polygon, Polygon)


# Hull:

def modIncrement(Value, Modulus, Increment = 1):
    return (Value + Increment) % Modulus

def convex_hull(Polygon): # Polygon must be monotonic or radial (Graham convex hull) (build_polygon_rotsort, build_polygon_direction)
    Hull = []

    StartIndex = Polygon.index(min(Polygon, key = lambda P: P[1]))
    Hull.append(Polygon[StartIndex])

    CurrentIndex = modIncrement(StartIndex, len(Polygon))
    while True:
        Current = Polygon[CurrentIndex]

        if len(Hull) >= 2 and sarea(Hull[-2], Hull[-1], Current) > 0:
            Hull.pop()
        elif CurrentIndex == StartIndex:
            break
        else:
            Hull.append(Current)
            CurrentIndex = modIncrement(CurrentIndex, len(Polygon))

    return Hull

def slow_convex_hull(Polygon):
    Hull = []

    Start = min(Polygon, key = lambda P: P[1])
    Hull.append(Start)
    Angle = 0

    while True:
        Vertex = Hull[-1]
        NextValue = None

        for Point in Polygon:
            PointValue = ((atan2(Point[1] - Vertex[1], Point[0] - Vertex[0]) - Angle) % (2*pi), (Point[1]-Vertex[1])**2 + (Point[0]-Vertex[0])**2, Point)
            if Point != Vertex and (NextValue == None or PointValue < NextValue):
                NextValue = PointValue

        Angle = (Angle + NextValue[0]) % (2*pi)
        Next = NextValue[2]

        if Next == Start:
            break

        Hull.append(Next);

    return Hull

def ikea(Polygon):
    #TODO
    return

# Triangulation

def graham_triangulation(Points):
    Start= min(Points, key = lambda P: P[1])
    Polygon = build_polygon_rotsort(Points, Start)
    Polygon.append(Start) # Iterate easily

    Hull = [Start]
    Triangles = []
    PolygonWithoutDuplicates = [Start]

    #######################
    # Triangle neighbours
    TrianglesNeighIn = []
    TrianglesNeighOut = []
    TriangleID = 0
    ExternalTriangleStack = [] # List with triangles that have a side facing outside
    #######################

    StartIndex = 0
    CurrentIndex = 1
    MaxReachedIndex = 0
    while True:
        Current = Polygon[CurrentIndex]

        if Current == Polygon[CurrentIndex-1] and CurrentIndex < (len(Polygon) -1): # Ignore duplicated points aside from last start
            CurrentIndex += 1
            continue

        if CurrentIndex > MaxReachedIndex and CurrentIndex < (len(Polygon) -1): # New triangle, avoid last vertex (duplicated start)
            MaxReachedIndex = CurrentIndex
            PolygonWithoutDuplicates.append(Current)

            if len(PolygonWithoutDuplicates) > 2:
                Triangle = [Start, PolygonWithoutDuplicates[-2], PolygonWithoutDuplicates[-1]]
                Triangles.append(Triangle)

                #######################
                # Triangle neighbours #
                TriangleNeighbours = []
                if len(TrianglesNeighIn) > 0: # Last triangle from the ones inside the Polugon
                    PreviousTriangleRow = TrianglesNeighIn[-1]
                    TriangleNeighbours.append(PreviousTriangleRow[0]) # Add id of previous "in" triangle to current neighbours
                    PreviousTriangleRow[2].append(TriangleID) # Add current id to neighbours of the previous "in" triangle

                TriangleRow = (TriangleID, Triangle, TriangleNeighbours)
                ExternalTriangleStack.append(TriangleRow)
                TrianglesNeighIn.append(TriangleRow)
                TriangleID = TriangleID+1
                #######################

        if len(Hull) >= 2 and sarea(Hull[-2], Hull[-1], Current) > 0:
            Triangle = [Hull[-2], Hull[-1], Current]
            Triangles.append(Triangle)
            Hull.pop()
            CurrentIndex -= 1

            #######################
            # Triangle neighbours
            Neighbour1Row = ExternalTriangleStack.pop()
            Neighbour2Row = ExternalTriangleStack.pop()

            Neighbour1Row[2].append(TriangleID) # Add current id to neighbours of the external triangle
            Neighbour2Row[2].append(TriangleID) # ^

            TriangleNeighbours = []
            TriangleNeighbours.append(Neighbour1Row[0]) # Add id of previous external triangle to current neighbours
            TriangleNeighbours.append(Neighbour2Row[0]) # ^

            TriangleRow = (TriangleID, Triangle, TriangleNeighbours)
            ExternalTriangleStack.append(TriangleRow)
            TrianglesNeighOut.append(TriangleRow)
            TriangleID += 1
            #######################
        elif Current == Start:
            break
        else:
            Hull.append(Current)

        CurrentIndex += 1

    Polygon.pop() # Remove duplicated start
    return (Hull, Triangles, PolygonWithoutDuplicates, sorted(TrianglesNeighIn + TrianglesNeighOut))

def graham_triangulation_dcel(PointsCoordinates):
    #######################
    # Create polygon
    StartPointCoordinates = min(PointsCoordinates, key = lambda P: P[1])
    Polygon = build_polygon_rotsort(PointsCoordinates, StartPointCoordinates)
    #######################


    #######################
    # Create return structures # TODO use OOO and leave lists out
    # TODO use references instead of so many ids
    Points = [] # Point = (id, coord, edge id list that start from this point)
    Hull = [] # List of Point Ids
    Edges = [] # (id, start point id, end point id, mirror edge id, next edge id, previous edge id, face id that includes it)
    Faces = [] # (id, list of edge ids, list of point ids)
    #######################


    #######################
    # Remove duplicates in polygon
    StartPointIndex = 0
    StartPoint = (StartPointIndex, StartPointCoordinates, [])
    Points.append(StartPoint)

    for PointCoordinates in Polygon:
        if PointCoordinates != Points[-1][1]:
            Points.append((len(Points), PointCoordinates, []))

    PolygonSize = len(Points)
    if PolygonSize < 3:
        return None

    Points.append(StartPoint) # Easier iteration
    #######################

    def addEdges(PointIdList, MirrorEdgesIds, PolygonId):
        EdgeBaseId = len(Edges)
        LocalEdgesIds = []
        for PointIdIndex in xrange(0, len(PointIdList)):
            StartPointId = PointIdList[PointIdIndex-1]
            EndPointId = PointIdList[PointIdIndex]
            EdgeId = EdgeBaseId + PointIdIndex

            # Previous and Next edge ids are known even if they do not exist yet
            PreviousEdgeId = EdgeId -1
            if PreviousEdgeId < EdgeBaseId:
                PreviousEdgeId += len(PointIdList)
            NextEdgeId = EdgeId +1
            if NextEdgeId > EdgeBaseId + len(PointIdList)-1:
                NextEdgeId -= len(PointIdList)

            # This could be done searching by edges starting on EndPointId,
            # instead of managing the MirrorEdgesIds
            MirrorEdgeId = MirrorEdgesIds.pop()
            if MirrorEdgeId != None: # Set the mirror's mirror
                Edges[MirrorEdgeId][3] = EdgeId

            Edge = [EdgeId, StartPointId, EndPointId, MirrorEdgeId, NextEdgeId, PreviousEdgeId, PolygonId]
            Points[StartPointId][2].append(EdgeId)
            Edges.append(Edge)
            LocalEdgesIds.append(EdgeId)

        return LocalEdgesIds

    def addPolygon(PointIdList, MirrorEdgesIds):
        PolygonId = len(Faces)
        EdgeIdList = addEdges(PointIdList, MirrorEdgesIds, PolygonId)
        Polygon = [PolygonId, EdgeIdList, PointIdList]
        Faces.append(Polygon)
        return Polygon

    CurrentPolygonIndex = 1
    MaxReachedPolygonIndex = 1
    Hull.append(StartPointIndex)

    # Mirrorless Edges
    MirrorlessExternalEdgesIds = []
    MirrorlessInternalEdgesIds = [None] # So the pop in the first triangle does not fail, this would be the first edge in the hull, that still does not exist

    while True:
        CurrentPoint = Points[CurrentPolygonIndex]

        if CurrentPolygonIndex > MaxReachedPolygonIndex and CurrentPolygonIndex < PolygonSize: # New "in" triangle (avoid last duplicated start)
            MaxReachedPolygonIndex = CurrentPolygonIndex

            # Given enough points (Start, Previous and Current), This point
            # creates a triangle, and manage the MirrorEdgesIds
            MirrorlessInternalEdgesIds.append(None)
            MirrorlessInternalEdgesIds.append(None)
            Polygon = addPolygon([CurrentPolygonIndex, StartPointIndex, CurrentPolygonIndex-1], MirrorlessInternalEdgesIds) # Point order is important to match mirrors
            NewEdgesIds = Polygon[1]
            MirrorlessExternalEdgesIds.append(NewEdgesIds[0]) # One for each None pushed
            MirrorlessInternalEdgesIds.append(NewEdgesIds[1]) # One for each None pushed

        if len(Hull) >= 2 and sarea(Points[Hull[-2]][1], Points[Hull[-1]][1], CurrentPoint[1]) > 0: # sarea works with coordinates
            RemovedHullPointIndex = Hull.pop()

            # Add "outer" triangle with the removed hull point, and manage the
            # MirrorEdgesIds, again, point order is important to match mirrors
            # stacks
            MirrorlessExternalEdgesIds.append(None)
            Polygon = addPolygon([CurrentPolygonIndex, RemovedHullPointIndex, Hull[-1]], MirrorlessExternalEdgesIds)
            NewEdgesIds = Polygon[1]
            MirrorlessExternalEdgesIds.append(NewEdgesIds[0]) # One for each None pushed

            CurrentPolygonIndex -= 1
        elif CurrentPolygonIndex == PolygonSize: # Current point is last start and the Hull is finished
            break
        else:
            Hull.append(CurrentPolygonIndex)

        CurrentPolygonIndex += 1

    Points.pop() # Remove duplicated start

    # Create the mirrors of the Hull (in reverse direction)
    # TODO: Change addEdges with direction to avoid two O(size of hull)
    MirrorlessExternalEdgesIds.append(MirrorlessInternalEdgesIds.pop()) # Last 'internal' edge is external
    # Add the first edge in the hull, it exists now (this triangulation gives it
    # always the id 2, last index of the first polygon generated)
    MirrorlessExternalEdgesIds.insert(0, 2)
    Hull.reverse()
    HullEdgesIds = addEdges(Hull, MirrorlessExternalEdgesIds, None)

    return (Points, HullEdgesIds, Edges, Faces)


def improve_triangulation(DCEL, StopAtFirst = False):
    # TODO use a stack of edges: At the start, every edge is on it and they keep
    # getting removed once they have been checked, and if there's a flip, all
    # affected edges are put again in the stack
    Points = DCEL[0]
    Edges = DCEL[2]
    Faces = DCEL[3]

    def coordinates(PointId):
        return Points[PointId][1]

    Improved = False
    # (id, start point id, end point id, mirror edge id, next edge id, previous edge id, face id that includes it)
    for Edge in Edges:
        EdgeId = Edge[0]
        MirrorEdgeId = Edge[3]
        Mirror = Edges[MirrorEdgeId]
        if Edge[6] == None or Mirror[6] == None: # Edge or Mirror in hull
            continue

        TriangleVertexPointId = Edges[Edge[4]][2] # End Point id of the next edge
        CandidatePointId = Edges[Mirror[4]][2] # End PointId of the mirror's next edge (triangle vertex point of the mirror)
        EdgeStartPointId = Edge[1]
        EdgeEndPointId = Edge[2]

        # If is convex and point inside triangle's circumference, flip the edge
        TriangleVertexPointCoordinates = coordinates(TriangleVertexPointId)
        CandidatePointCoordinates = coordinates(CandidatePointId)
        EdgeStartCoordinates = coordinates(EdgeStartPointId)
        EdgeEndCoordinates = coordinates(EdgeEndPointId)

        Sarea1 = sarea(TriangleVertexPointCoordinates, EdgeStartCoordinates, CandidatePointCoordinates)
        Sarea2 = sarea(CandidatePointCoordinates, EdgeEndCoordinates, TriangleVertexPointCoordinates)

        if (Sarea1 < 0) and (Sarea2 < 0) and (inCircle(TriangleVertexPointCoordinates, EdgeStartCoordinates, EdgeEndCoordinates, CandidatePointCoordinates) > 0):
            # Flip it!

            # Set points
            Points[EdgeStartPointId][2].remove(EdgeId)
            Points[EdgeEndPointId][2].remove(MirrorEdgeId)

            Edge[1] = CandidatePointId
            Edge[2] = TriangleVertexPointId
            Mirror[1] = TriangleVertexPointId
            Mirror[2] = CandidatePointId

            Points[CandidatePointId][2].append(EdgeId)
            Points[TriangleVertexPointId][2].append(MirrorEdgeId)

            # Set next & previous
            EdgeOriginalNext = Edge[4]
            Edge[4] = Edge[5]
            Edge[5] = Mirror[4]
            Mirror[4] = Mirror[5]
            Mirror[5] = EdgeOriginalNext

            MirrorPrevious = Edges[Mirror[5]]
            MirrorNext = Edges[Mirror[4]]
            EdgePrevious = Edges[Edge[5]]
            EdgeNext = Edges[Edge[4]]

            MirrorPrevious[4] = MirrorEdgeId
            EdgePrevious[4] = EdgeId
            MirrorNext[5] = MirrorEdgeId
            EdgeNext[5] = EdgeId
            MirrorPrevious[5] = Mirror[4]
            EdgePrevious[5] = Edge[4]
            MirrorNext[4] = Mirror[5]
            EdgeNext[4] = Edge[5]

            # Set face changes
            MirrorPrevious[6] = Mirror[6]
            EdgePrevious[6] = Edge[6]

            FaceEdge = Faces[Edge[6]]
            FaceEdge[1] = [Edge[5], EdgeId, Edge[4]]
            FaceEdge[2] = [CandidatePointId, TriangleVertexPointId, EdgeStartPointId]
            FaceMirror = Faces[Mirror[6]]
            FaceMirror[1] = [Mirror[5], MirrorEdgeId, Mirror[4]]
            FaceMirror[2] = [TriangleVertexPointId, CandidatePointId, EdgeEndPointId]

            Improved = True
            if StopAtFirst:
                return Improved

    return Improved






