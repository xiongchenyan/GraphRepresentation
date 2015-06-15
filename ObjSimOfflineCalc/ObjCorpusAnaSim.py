'''
Created on my MAC Jun 11, 2015-12:00:57 PM
What I do:
    I generate obj-obj->score from corpus ana results
What's my input:
    a file, contains the pairwise cnt for target pairs (pickle dump)
    a ctf file for obj ctf in facc | fakba 
    a score metric choice:
        default:    \frac{pair cnt}{obj a' ctf}
What's my output:
    a pickle dict, obj\tobj score (directed, a->b different with b->a, both should in dict)
@author: chenyanxiong
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
import sys
import pickle
import logging

from IndriRelate.CtfLoader import TermCtfC


def CalcSimilarity(ObjA,ObjB,CorrCnt,ObjCtfCenter,SimMetric = 'tfidf'):
    if SimMetric == 'tfidf':
        if not ObjA in ObjCtfCenter.hTermCtf:
            return 0
        return float(CorrCnt) * ObjCtfCenter.GetLogIdf()
    if SimMetric == 'tf':
        return CorrCnt
    if SimMetric == 'prob':
        if not ObjA in ObjCtfCenter.hTermCtf:
            return 0
        return float(CorrCnt) / float(ObjCtfCenter.GetCtf())
    return CorrCnt


def Process(PairCorrCntDictInName, CtfInName,OutName, SimMetric = 'tfidf'):
    hPairCnt = pickle.load(open(PairCorrCntDictInName))
    logging.info('pair cnt loaded')
    
    
    ObjCtfCenter = TermCtfC()
    ObjCtfCenter.Load(CtfInName)
    
    hPairCorr = {}
    
    logging.info('start to calc obj corpus ana similarity')
    cnt = 0
    for key,tf in hPairCnt.items():
        ObjA,ObjB = key.split()
        CorrScore = CalcSimilarity(ObjA, ObjB, tf, ObjCtfCenter, SimMetric)
        hPairCorr[key] = CorrScore
        cnt += 1
        if 0 == (cnt % 1000):
            logging.info('processed [%d] pair',cnt)
    
    pickle.dump(open(OutName,'w'),hPairCorr)
    logging.info('corr score dumped to [%s]',OutName)
    return


import sys
if 5 != len(sys.argv):
    print 'I calc obj corpua ana sim from raw ana tf dict'
    print '4 para: corpus ana dict in + obj ctf in + out + simmetric (tfidf|tf|prob)'
    sys.exit()
    
Process(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        
    
    
        