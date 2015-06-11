'''
Created on Feb 10, 2015 3:23:50 PM
@author: cx

what I do:
I fetch the neighbor of candidata objects

what's my input:
query-obj candidate cache file
what's my output:
add lines for each line in input, corresponding to its neighbors.
columns are the same as original lines, 
but with an additional column saying which edge it is

'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/SemanticSearch')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC
from cxBase.Conf import cxConfC
import sys

if 2 != len(sys.argv):
    FbObjCacheCenterC.ShowConf()
    print 'in\nout'
    sys.exit()
    
conf = cxConfC(sys.argv[1])
CacheCenter = FbObjCacheCenterC(sys.argv[1])

InName = conf.GetConf('in')
OutName = conf.GetConf('out')

out = open(OutName,'w')

for line in open(InName):
    line = line.strip()
    vCol = line.split('\t')
    ObjId = vCol[2]
    lLinkedObj = CacheCenter.FetchObj(ObjId).GetNeighbor()
    print >> out,line
    for edge,ApiObj in lLinkedObj:
        print >>out,'\t'.join(vCol[:2]) + '\t' + ApiObj.GetId() + '\t' + ApiObj.GetName() + '\tNeighbor\t1\t' + edge
    
out.close()
print "finished"