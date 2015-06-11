'''
Created on Feb 23, 2015 4:04:33 PM
@author: cx

what I do:
I generate entity correlation per file
what's my input:
    a file (with full path)
    target object id
    a type (facc|fakba)
    an output dir
what's my output:
    in the output dir, the correlation with this file name prefix
        so I will need to get the file name from the input file name

'''
'''
because it is per file, I can store the pairs in memory, and sort them in output
'''

'''

'''

import ntpath
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/SemanticSearch')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')


from Facc.FaccReader import FaccReaderC
from Facc.FakbaReader import FakbaReaderC
import sys

def GenerateOutNameFromInName(InName,InType = 'facc'):
    '''
    if facc: then the last two dim of directory + file name
    if fakba: just InName
    '''
    if InType != 'facc':
        return ntpath.basename(InName)
    
    vCol = InName.split('/')
    return '_'.join(vCol[-3:])


def Process(InName,OutDir,hTargetId = {}, InType = 'facc'):
    hPair = {}
    if InType == 'facc':
        Reader = FaccReaderC()
    else:
        Reader = FakbaReaderC()
        
    Reader.open(InName)
    OutName = OutDir + '/' + GenerateOutNameFromInName(InName, InType)
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
                
                lObjId = [lAna[i].ObjId,lAna[j].ObjId]
                lObjId.sort()
                key = ' '.join(lObjId)
                if not key in hPair:
                    hPair[key] = 1
                else:
                    hPair[key] += 1
                
#                 print >>out, lAna[i].ObjId + '\t' + lAna[j].ObjId
#                 print >>out, lAna[j].ObjId + '\t' + lAna[i].ObjId
                PairCnt += 1
        cnt += 1
        if 0 == (cnt % 100):
            print 'processed [%d] doc' %(cnt)
    
    
    lPairCnt = hPair.items()
    lPairCnt.sort(key = lambda item: item[0])
    for Pair,cnt in lPairCnt:
        print >>out, Pair + ' %d' %(cnt)
    out.close()        
    print 'finished to [%s] [%d] in [%d] pair pairwise correlation' %(OutName,PairCnt,len(hPair))
    
    return True
    
def ReadTargetId(TargetIdInName):
    hTargetId = {}
    if "" != TargetIdInName:
        lId = open(TargetIdInName).read().splitlines()
        hTargetId = dict(zip(lId,[0]*len(lId)))
    return hTargetId


if 5 != len(sys.argv):
    print "InName + outdir + target id in + intype (facc|fakba)"
    sys.exit()
    
hTargetId = ReadTargetId(sys.argv[3])
Process(sys.argv[1],sys.argv[2],hTargetId,sys.argv[4])








