#!/usr/bin/env python2

import timeit

def pointGeneratorSetup(Num, Varname):
    return '{} = [[random(), random()] for x in xrange({})]'.format(Varname, Num)

def time(functionString, setup):
    res = timeit.timeit('lilcgal_sort.'+functionString, setup='import lilcgal_sort; from random import random;'+setup, number=500)
    print("> {} with setup {} took {}".format(functionString, setup, res))

time('sort_vectorDir_dot(L,[1,1])', pointGeneratorSetup(1000, 'L'))
time('sort_vectorDir_dot_tuple(L,[1,1])', pointGeneratorSetup(1000, 'L'))
time('sort_vectorDir_dot2(L,[1,1])', pointGeneratorSetup(1000, 'L'))
time('sort_vectorDir_dot_customfun(L,[1,1])', pointGeneratorSetup(1000, 'L'))
time('sort_vectorDir_dot_customlambda(L,[1,1])', pointGeneratorSetup(1000, 'L'))
time('sort_vectorDir_matrixTurn(L,[1,1])', pointGeneratorSetup(1000, 'L'))
time('sort_vectorDir_dot_tuple(L,[1,1])', pointGeneratorSetup(10000, 'L'))
time('sort_vectorDir_dot_customfun(L,[1,1])', pointGeneratorSetup(10000, 'L'))
time('sort_vectorDir_dot_customlambda(L,[1,1])', pointGeneratorSetup(10000, 'L'))
