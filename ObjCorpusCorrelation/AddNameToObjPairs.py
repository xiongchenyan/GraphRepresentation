'''
Created on Feb 24, 2015 3:23:15 PM
@author: cx

what I do:
    add name to object pairs:
what's my input:
    obj id\t objid\t correlation score
what's my output:
    add "\t name a \t name b" in the end of each line

'''


import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC
from cxBase.Conf import cxConfC
import sys

if 2 != len(sys.argv):
    FbObjCacheCenterC.ShowConf()
    print "in\nout"
    sys.exit()
    
    
ObjCenter = FbObjCacheCenterC(sys.argv[1])
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')

out = open(OutName,'w')

cnt = 0
for line in open(InName):
    line = line.strip()
    vCol = line.split('\t')
    lName = [ObjCenter.FetchObjName(ObjId) for ObjId in vCol[:2]]
    print >> out, line + '\t' + '\t'.join(lName)
    cnt += 1
    if 0 == (cnt % 100):
        print "processed [%d] line" %(cnt)
    
out.close()
    
