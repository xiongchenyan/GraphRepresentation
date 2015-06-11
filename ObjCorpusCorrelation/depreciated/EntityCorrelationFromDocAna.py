'''
Created on Feb 12, 2015 1:11:12 PM
@author: cx

what I do:
Generate entity correlation "context" pairs in AnnD
Window size = 100
what's my input:
FACC or Fakba dir
what's my output:
objid objid perline
each line is an appearane of context correlation

Feb 22:
add target obj id input option
only get those edges with target obj id (e.g. query's candidate objects) if used
'''

'''
Feb 23 
Not in use now. too slow to run in one single machine
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/SemanticSearch')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')


from Facc.FaccReader import FaccReaderC
from Facc.FakbaReader import FakbaReaderC

from cxBase.Conf import cxConfC
import sys

if 2 != len(sys.argv):
    print "conf:\ndir\nout\ntype facc|fakba\ntargetobj (if needed)"
    sys.exit()

conf = cxConfC(sys.argv[1])
InDir = conf.GetConf('dir')
OutName = conf.GetConf('out')
DataType = conf.GetConf('type','facc')
TargetObjIn = conf.GetConf('targetobj')
hTargetId = {}
if "" != TargetObjIn:
    lId = open(TargetObjIn).read().splitlines()
    hTargetId = dict(zip(lId,[0]*len(lId)))


if DataType == 'facc':
    Reader = FaccReaderC()
else:
    Reader = FakbaReaderC()
    
Reader.opendir(InDir)
out = open(OutName,'w')
cnt = 0
PairCnt = 0
for lAna in Reader:
    for i in range(len(lAna)):
        for j in range(i + 1,len(lAna)):       
            if lAna[j].st - lAna[i].st > 100:
                break
            if lAna[i].ObjId == lAna[j].ObjId:
                continue
            if len(hTargetId) != 0:
                if (not lAna[i].ObjId in hTargetId) & (not lAna[j].ObjId in hTargetId):
                    continue
            print >>out, lAna[i].ObjId + '\t' + lAna[j].ObjId
            print >>out, lAna[j].ObjId + '\t' + lAna[i].ObjId
            PairCnt += 1
    cnt += 1
    if 0 == (cnt % 100):
        print 'processed [%d] doc' %(cnt)
        
out.close()        
print 'finished [%d] pairwise correlation' %(PairCnt)
