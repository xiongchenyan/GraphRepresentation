'''
Created on Aug 11, 2015 6:57:02 PM
@author: cx

what I do:
    I re-rank query using LES
    for a query 
        1, fetch doc
        2, fetch objid for q and doc
        3, fill obj
        4, match doc obj to doc
        5, inference
what's my input:
    q,lDoc,
    and their objects (from NodeCollector's result dir)
what's my output:
    new ranking
    or evalution results

'''



import site
import math
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
site.addsitedir('/bos/usr0/cx/PyCode/SemanticSearch')

import os
import json
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
import pickle


from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from AdhocEva.AdhocEva import AdhocEvaC

from LESInference import LESInferencerC


class LESRanker(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        
        self.Searcher = IndriSearchCenterC()
        self.ObjCenter = FbObjCacheCenterC()
        self.Evaluator = AdhocEvaC()
        
        self.Inferener = LESInferencerC()
        
        self.QDocNodeDataDir = ""
        self.hQDocObj = {}
        self.OrigQWeight = 0.5
        
    
    @classmethod
    def ShowConf(cls):
        cxBaseC.ShowConf()
        IndriSearchCenterC.ShowConf()
        FbObjCacheCenterC.ShowConf()
        AdhocEvaC.ShowConf()
        
        print 'qdocnodedatadir\norigqweight 0.5'
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.Searcher.SetConf(ConfIn)
        self.Evaluator.SetConf(ConfIn)
        self.ObjCenter.SetConf(ConfIn)
        self.QDocNodeDataDir = self.conf.GetConf('qdocnodedatadir') + '/'
        self.OrigQWeight = self.conf.GetConf('origqweight', self.OrigQWeight)
        
        
        
    def LoadQDocObj(self,query):
        InName = self.QDocNodeDataDir + IndriSearchCenterC.GenerateQueryTargetName(query)
        
        for line in open(InName):
            key,ObjId = line.strip().split('\t')
            if not key in self.hQDocObj:
                self.hQDocObj[key] = [ObjId]
            else:
                self.hQDocObj[key].append(ObjId)
                
        return True
    
    
    def RankingForOneQ(self,qid,query):
        lDoc = self.Searcher.RunQuery(query, qid)
        logging.info('LES ranking for [%s-%s]',qid,query)
        QKey = 'q_%s' %(qid)
        if not QKey in self.hQDocObj:
            #do nothing
            logging.info('query [%s] has no object, return raw raning',qid)
            return lDoc
        
        
        lQObj = [self.ObjCenter.FetchObj(ObjId) for ObjId in self.hQDocObj[QKey]]
        
        lDocLESScore = []
        LesCnt = 0
        for doc in lDoc:
            if not doc.DocNo in self.hQDocObj:
                lDocLESScore.append(0)
                continue
            LesCnt += 1
            lDocObj = [self.ObjCenter.FetchObj(ObjId) for ObjId in self.hQDocObj[doc.DocNo]]
            
            score = self.Inferener.inference(query, doc, lQObj, lDocObj)
            lDocLESScore.append(score)
        
        #add average score to doc without annotation
        #using zero is not very proper
        AvgScore = sum(lDocLESScore) / float(LesCnt)
        
        
        lDocLESScore = [item if item != 0 else AvgScore for item in lDocLESScore]
        
        lScore= [self.OrigQWeight * math.exp(doc.score) + (1-self.OrigQWeight) * LESScore \
                     for doc,LESScore in zip(lDoc,lDocLESScore)]
        
        lDocNoScore =zip ([doc.DocNo for doc in lDoc], lScore)
        lDocNoScore.sort(key=lambda item:item[1], reverse = True)
        lRankedDocNo = [item[0] for item in lDocNoScore]
        
        logging.info('query [%s] ranked',qid)

        return lRankedDocNo 


    def Process(self,QIn,OutName):
        
        lQidQuery = [line.split('\t') for line in open(QIn).read().splitlines()]
        
        llDocNo = [self.RankingForOneQ(qid, query) for qid,query in lQidQuery]
        
        logging.info('start evaluation')
        
        lQid = [item[0] for item in lQidQuery]
        lQuery = [item[1] for item in lQidQuery]
        lPerQEvaRes = self.Evaluator.EvaluateFullRes(lQid, lQuery, llDocNo)
        
        out = open(OutName,'w')
        for qid,EvaRes in lPerQEvaRes:
            print >> out, qid, EvaRes.dumps()
            
        out.close()
        logging.info('%s %s',lPerQEvaRes[-1][0],lPerQEvaRes[-1][1].dumps())
        
        return True
    
if __name__=='__main__':
    import sys

    if 2 != len(sys.argv):
        print 'I evaluate latent entity space (LES) ranking'
        print 'in\nout\n'
        LESRanker.ShowConf()
        sys.exit()
    
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    ch.setFormatter(formatter)
    
    
    
    conf = cxConfC(sys.argv[1])
    InName = conf.GetConf('in')
    OutName = conf.GetConf('out')
    
    Ranker = LESRanker(sys.argv[1])
    Ranker.Process(InName, OutName)
        
        
        
        
            
            
            
        
        
        
        
        
        
        
            


