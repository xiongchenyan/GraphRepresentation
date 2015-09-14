'''
Created on my MAC Sep 13, 2015-10:42:11 PM
What I do:
    I fetch results from tie-yan's LDA
What's my input:
    TargetDocNo
    Dir of DocNo-> URL mapping
    Dir of raw results (.xx xx is block number)
What's my output:
    a file of docno \t text
     only keep target doc
@author: chenyanxiong
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.WalkDirectory import WalkDir
from cxBase.Conf import cxConfC


def LoadTargetUrl(InDir,sDocNo):
    hUrlDocNo = {}
    lFName = WalkDir(InDir)
    for fname in lFName:
        for line in open(fname):
            vCol = line.strip().split('\t')
            if len(vCol) < 2:
                continue
            DocNo,Url = vCol[:2]
            if DocNo in sDocNo:
                hUrlDocNo[Url] = DocNo
    print "loaded [%d/%d] target url" %(len(hUrlDocNo,len(sDocNo)))            
    return hUrlDocNo


def FetchTargetDocLines(InDir,hUrlDocNo,OutName):
    out = open(OutName,'w')
    lFName = WalkDir(InDir)
    for fname in lFName:
        print 'start reading [%s]' %(fname)
        for line in open(fname):
            vCol = line.strip().split('\t')
            if len(vCol) < 2:
                continue
            url = vCol[0]
            data = '\t'.join(vCol[1:])
            if url in hUrlDocNo:
                DocNo = hUrlDocNo[url]
                print >>out, DocNo + '\t' + data
                print DocNo + ' find'
    
    print 'finished'
    
    
import sys

if 5 != len(sys.argv):
    print 'target doc no + url-doc no mapping dir + data dir + output'
    sys.exit()
    
    
sDocNo = set(open(sys.argv[1]).read().splitlines())

hUrlDocNo = LoadTargetUrl(sys.argv[2], sDocNo)

FetchTargetDocLines(sys.argv[3], hUrlDocNo, sys.argv[4])

        