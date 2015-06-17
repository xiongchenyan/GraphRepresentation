'''
Created on my MAC Jun 17, 2015-2:51:41 PM
What I do:
    Split obj similarity dict to dict per query level
What's my input:
    query node dir
    obj dict
What's my output:
    a dir contains dict for each query
@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from cxBase.WalkDirectory import WalkDir
import ntpath,os

import pickle



def FetchForOneQ(lObjId,hPairDict,OutName):
    hOut = {}
    for ObjIdA in lObjId:
        for ObjIdB in lObjId:
            key = ObjIdA + '\t' + ObjIdB
            if (key) in hPairDict:
                hOut[key] = hPairDict[key]
    pickle.dump(hOut,open(OutName,'w'))
    return


def Process(NodeInDir,PairDictInName,OutDir):
    lInName = WalkDir(NodeInDir)
    if not os.path.exists(OutDir):
        os.makedirs(OutDir)
    print 'start load dict'
    hPairDict = pickle.load(open(PairDictInName))
    print 'dict loaded'
    
    for InName in lInName:
        OutName = OutDir + '/' + ntpath.basename(InName)
        lObjId = open(InName).read().splitlines()
        FetchForOneQ(lObjId, hPairDict, OutName)
        print '[%s] finished' %(ntpath.basename(InName))
        
    print 'finished'
    
    
import sys

if 4 != len(sys.argv):
    print "q node dir + obj pair sim dict + out dir"
    sys.exit()
    
    
Process(sys.argv[1],sys.argv[2],sys.argv[3])
        
        
        
        
    
