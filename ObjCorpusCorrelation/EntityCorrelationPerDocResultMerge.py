'''
Created on Feb 23, 2015 7:52:52 PM
@author: cx

what I do:
Merge the results from EntityCorrelationPerDoc
what's my input:
    the dir contains files of entity correlations
        id id cnt
what's my output:
    id id cnt
    but sum up all files


Now directly use dict to handle them
     if not, use merge sort (all files are ordered)

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.WalkDirectory import WalkDir
import pickle
import sys


def Process(InDir,OutName):
    lFName = WalkDir(InDir)
    hPair = {}
    for fname in lFName:
        print "processing [%s] [%d] uniq pair now" %(fname,len(hPair))
        for line in open(fname):
            vCol = line.strip().split()
            if len(vCol) < 3:
                continue
            key = vCol[0] + '\t' + vCol[1]
            cnt = int(vCol[2])
            if not key in hPair:
                hPair[key] = cnt
            else:
                hPair[key] += cnt
                
    print "dumpping"
    pickle.dump(hPair,open(OutName,'w'))
    print "done"


if 3 != len(sys.argv):
    print "InDir + output merged cnt file name"
    sys.exit()
    
    
Process(sys.argv[1], sys.argv[2])    
    

    

