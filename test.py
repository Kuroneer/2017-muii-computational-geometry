#!/usr/bin/env python

from lilcgal import *

def main():

    Point0 = [0,0]
    Point1 = [0,1]
    Point2 = [0,2]
    Point3 = [1,1]

    print()
    print(dist2_dim2(Point0, Point3))    # 2
    print(dist2_generic(Point0, Point3)) # 2
    print(dist(Point0, Point3))          # 1.4142

    print()
    print(area_trig(Point0, Point1, Point3)) # 0.5
    print(area_trig(Point0, Point3, Point1)) # -0.5
    print(area_trig(Point0, Point1, Point2)) # 0
    print(area_trig(Point1, Point1, Point2)) # 0
    print(area_trig(Point1, Point1, Point1)) # 0

    print()
    print(sarea_trig(Point0, Point1, Point3)) # 0.5
    print(sarea_trig(Point0, Point3, Point1)) # -0.5
    print(sarea_trig(Point0, Point1, Point2)) # 0
    print(sarea_trig(Point1, Point1, Point2)) # 0
    print(sarea_trig(Point1, Point1, Point1)) # 0

    print()
    print(sarea_crossvector(Point0, Point1, Point3)) # 0.5
    print(sarea_crossvector(Point0, Point3, Point1)) # -0.5
    print(sarea_crossvector(Point0, Point1, Point2)) # 0
    print(sarea_crossvector(Point1, Point1, Point2)) # 0
    print(sarea_crossvector(Point1, Point1, Point1)) # 0

    print()
    print(orientation(Point0, Point1, Point3)) # 1
    print(orientation(Point0, Point3, Point1)) # -1
    print(orientation(Point0, Point1, Point2)) # 0
    print(orientation(Point1, Point1, Point2)) # 0
    print(orientation(Point1, Point1, Point1)) # 0

    print()
    print(midPoint(Point2, Point3)) # [.5, 1.5]

    Point4 = [3,4]
    Point5 = [2,3]
    Point6 = [1,2]

    print()
    print(inSegment(Point4,[Point5,Point6])) # false
    print(inSegment(Point5,[Point4,Point6])) # true
    print(inSegment(Point4,[Point4,Point6])) # true
    print(inSegment(Point0,[Point5,Point6])) # false

    print()
    print(inTriangle(Point4, [Point4, Point0, Point6])) # True (is vertex)
    print(inTriangle(Point5, [Point4, Point0, Point6])) # True (is in segment)
    print(inTriangle([.5,1], [Point0, Point2, Point3])) # True (inside)
    print(inTriangle([.5,1], [Point0, Point3, Point2])) # True (inside, reversed triangle)
    print(inTriangle([1.5,1], [Point0, Point3, Point2])) # False

    Point0 = [0,0]
    Point1 = [0,1]
    Point3 = [1,1]
    Point7 = [1,0]
    print()
    print(segmentIntersectionTest([Point0, Point1], [Point3, Point7])) # False (parallel)
    print(segmentIntersectionTest([Point1, Point0], [Point3, Point7])) # False (parallel reversed)
    print(segmentIntersectionTest([Point1, Point1], [Point3, Point7])) # False (single point not in segment + segment)
    print(segmentIntersectionTest([[0,.5], [.5,.5]], [Point3, Point7])) # False (Broken T)
    print(segmentIntersectionTest([[1.5,.5], [.5,.5]], [Point3, Point7])) # True (+)
    print(segmentIntersectionTest([[1.5,.5], [1,.5]], [Point3, Point7])) # True (T)
    print(segmentIntersectionTest([Point5, Point5], [Point4, Point6])) # True (single point in segment + segment)
    print(segmentIntersectionTest([Point4, Point5], [Point5, Point6])) # True (parallel + same end)
    print(segmentIntersectionTest([Point4, Point5], [Point5, Point0])) # True (same end)

    print()
    print(lineIntersection([Point0, Point3], [Point1, Point7])) # [.5,.5]
    print(lineIntersection([Point0, Point1], [Point1, Point7])) # [ 0, 1]
    print(lineIntersection([Point0, Point1], [Point3, Point7])) # None
    print(lineIntersection([Point0, Point1], [Point0, Point1])) # None
    print(lineIntersection([Point0, Point1], [Point1, Point0])) # None

if __name__ == "__main__":
    main()

