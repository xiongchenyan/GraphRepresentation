'''
Created on Feb 24, 2015 2:25:50 PM
@author: cx

what I do:
Find the top neighbors for each object in given correlation data
what's my input:
    target object no
    pickle dump of correlation cnt   | or just raw pair data
    df dict of objects
what's my output:
    for each target object
        obj\tobj\tPMI score (keep top 10)
'''

'''
Mar 2nd
Add multiple score calculations:
    TF:
    MRR: Mutual Rank ration: ctf rank (individual) / associated tf rank
select by input conf: correlationmeasure
implemented:
    not tested
'''

'''
Mar 12
add the function to read raw pair data as well

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

import pickle
import sys
from cxBase.Conf import cxConfC
from IndriRelate.CtfLoader import TermCtfC


def FormTargetObjNeighbors(hTargetObj,hPair,CtfCenter,CorrelationScoreType = 'tf'):
    TotalPair = sum(item[1] for item in hPair.items())
    
    hTargetObjNeighbor = {}
    #for the raw neighbor prob first
    PairCnt = 0
    for pair,tf in hPair.items():
        PairCnt += 1
        if 0 == (PairCnt % 1000):
            print 'processing [%d/%d] pair' %(PairCnt,len(hPair))
        lObj = pair.split()
        
        for i in range(len(lObj)):
            if not lObj[i] in hTargetObj:
                continue
            if not lObj[i] in hTargetObjNeighbor:
                hTargetObjNeighbor[lObj[i]] = [[lObj[i - 1],tf]]
            else:
                hTargetObjNeighbor[lObj[i]].append([lObj[i - 1],tf])
    
    print "start calculating neighbor score [%s]" %(CorrelationScoreType)
    for obj,lNeighborTF in hTargetObjNeighbor.items():
        hTargetObjNeighbor[obj] = CalculateOneTargetObjNeighborScore(lNeighborTF, CtfCenter, PairCnt, CorrelationScoreType)
        
                
    return hTargetObjNeighbor


def CalculateOneTargetObjNeighborScore(lObjTF,CtfCenter,TotalPairCnt,CorrelationScoreType = 'tf'):
    '''
    calcualte the correlation score using different metrics
    tf: just orighnal score
    mrr: mutual rank
    
    return lObjCorrScore = [[obj id, score]]
    '''
    
    if CorrelationScoreType == 'tf':
        return lObjTF
    
    if CorrelationScoreType == 'mrr':
        return MRRCorrelation(lObjTF,CtfCenter)
    
    print '[%s] not supported' %(CorrelationScoreType)    
    return lObjTF


def MRRCorrelation(lObjTF,CtfCenter):
    lObjDF = [[obj,CtfCenter.GetCtf(obj)] for obj,score in lObjTF]
    lObjDF.sort(key = lambda item: item[1], reverse = True)
    lObjTF.sort(key = lambda item: item[1],reverse = True)
    
    hObjDFRank = dict(zip([item[0] for item in lObjDF],range(1,len(lObjDF) + 1)))
    
    lObjMrr = list(lObjTF)
    for i in range(len(lObjMrr)):
        lObjMrr[i][1] = hObjDFRank[lObjMrr[i][0]] / float(i + 1)
        
    return lObjMrr
        
    
    
    

def FormPairDictFromRaw(PairRawIn):
    hPair = {}
    for line in open(PairRawIn):
        vCol = line.strip().split('\t')
        key = " ".join(vCol)
        if not key in hPair:
            hPair[key] = 1
        else:
            hPair[key] += 1
    print "formed [%d] pair from [%s]" %(len(hPair),PairRawIn)
    return hPair
    
    
    


def DumpTargetObjTopNeighbor(hTargetObjNeighbor,OutName, NumOfNeighbor = 10):
    out = open(OutName,'w')
    for ObjId,lNeighbor in hTargetObjNeighbor.items():
        lNeighbor.sort(key=lambda item:item[1],reverse = True)
        for Neighbor in lNeighbor[:NumOfNeighbor]:
            print >>out, ObjId + '\t' + Neighbor[0] + '\t%f' %(Neighbor[1])
    out.close()
    
    
if 2 != len(sys.argv):
    print "conf:\n"
    print "targetobj\npairdict|pairraw (choose one)\nidfdict\nout\nnumofneighbor\ncorrelationmeasure tf#mrr"
    sys.exit()
    
conf = cxConfC(sys.argv[1])
TargetObjIn = conf.GetConf('targetobj')
PairDictIn = conf.GetConf('pairdict')
PairRawIn = conf.GetConf('pairraw')
IdfDictIn = conf.GetConf('idfdict')
OutName = conf.GetConf('out')
NumOfNeighbor = int(conf.GetConf('numofneighbor'))
CorrType = conf.GetConf('correlationmeasure')


lLine = open(TargetObjIn).read().splitlines()
hTargetObj = dict(zip(lLine,range(len(lLine))))
print "[%d] target obj load" %(len(hTargetObj))

hPair = {}
if PairDictIn != "":
    hPair = pickle.load(open(PairDictIn))
    print "[%d] pair cnt load" %(len(hPair))
else:
    if PairRawIn != "":
        hPair = FormPairDictFromRaw(PairRawIn)
    
CtfCenter = TermCtfC()
CtfCenter.Load(IdfDictIn)
print "df load"

print "forming neighbors..."
hTargetObjNeighbor = FormTargetObjNeighbors(hTargetObj, hPair, CtfCenter,CorrType)
print "dumpping results..."
DumpTargetObjTopNeighbor(hTargetObjNeighbor, OutName, NumOfNeighbor)
print "finished"





        
        
        
     
        
    
        
    
    
    
    
    
    
    
    


