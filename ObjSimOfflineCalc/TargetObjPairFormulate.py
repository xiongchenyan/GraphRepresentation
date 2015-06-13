'''
Created on my MAC Jun 13, 2015-6:55:56 PM
What I do:
    simply formulate all target obj pair in the given dir
What's my input:
    the dir of each query's obj node
What's my output:
    a file each line is obj-obj id (obj id is sorted)
@author: chenyanxiong
'''

from ObjSimBaseFunction import LoadPerQObjIdFromDir

def FormTargetPair(lhObjId):
    lPair = []
    for hObjId in lhObjId:
        lObjId = hObjId.keys()
        lObjId.sort()
        for i in range(len(lObjId)):
            for j in range(i+1, len(lObjId)):
                lPair.append(lObjId[i] + '\t' + lObjId[j])
    return lPair


def Process(InDir, OutName):
    lhObjId = LoadPerQObjIdFromDir(InDir)
    lPair = FormTargetPair(lhObjId)
    lPair = list(set(lPair))
    out = open(OutName,'w')
    for pair in lPair:
        print >>out, pair
    out.close()
    print "total [%d] pair dumped to [%s]" %(len(lPair),OutName)
    
    
import sys

if 3 != len(sys.argv):
    print "q node in dir + target pair out name"
    sys.exit()
    
Process(sys.argv[1], sys.argv[2])
