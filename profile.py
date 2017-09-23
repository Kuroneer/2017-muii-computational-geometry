#!/usr/bin/env python

import timeit
def time(functionString):
    res = timeit.timeit('lilcgal.'+functionString, setup='import lilcgal', number=50000)
    print("> {} took {}".format(functionString, res))

time('dist2_dim2([0,0],[1,1])')
time('dist2_generic([0,0],[1,1])')
time('sarea_trig([0,0],[1,1],[0,1])')
time('sarea_crossvector([0,0],[1,1],[0,1])')
time('segmentIntersectionTest([[0,0],[1,1]],[[1,0],[0,1]])')

time('inCircle_det([0,0],[1,1],[1,0],[0,1])')
time('inCircle_dist2([0,0],[1,1],[1,0],[0,1])')

