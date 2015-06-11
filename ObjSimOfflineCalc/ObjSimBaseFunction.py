'''
Created on my MAC Jun 11, 2015-11:28:29 AM
What I do:
    Load per query obj set
    to be used as target pair for all offline calculating
What's my input:
    Node Generator's output dir
        each file is the objid for this query
What's my output:
    I am a function, only return lhQObjId = [set(objid)]
@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.WalkDirectory import WalkDir
import ntpath


def LoadPerQObjIdFromDir(InDir):
    lFName = WalkDir(InDir)
    lhQObjId = []
    for fname in lFName:
        lThisObjId = open(fname).read().splitlines()
        lhQObjId.append(dict(zip(lThisObjId,[fname] * len(lThisObjId))))
    return lhQObjId
