'''
Created on Sep 1, 2015 8:15:34 PM
@author: cx

what I do:
    I provide ranking function using LES model
    
    1,fetch q and doc's obj id
    2,fetch obj's infor
    3,rank use LES
what's my input:
    doc's kg dir
    q's ana obj
    obj center to fetch obj infor

what's my output:
    ranking score for given q-doc

'''



import site
import math
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

import os
import json
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging


from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC

from LESInference import LESInferencerC
from DocGraphRepresentation.DocKnowledgeGraph import DocKnowledgeGraphC
from DocGraphRepresentation.ConstructSearchResDocGraph import SearchResDocGraphConstructorC



class LESRanker(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        
        self.ObjCenter = FbObjCacheCenterC()
        self.Inferener = LESInferencerC()
        self.DocKgDir = ""
        self.hQObj = {}
        self.OrigQWeight = 0.5
        
    
    @classmethod
    def ShowConf(cls):
        cxBaseC.ShowConf()
        FbObjCacheCenterC.ShowConf()
        print 'origqweight 0.5'
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DocKgDir = self.conf.GetConf('dockgdir')
        QAnaInName = self.conf.GetConf('qanain')
        self.LoadQObj(QAnaInName)
        self.ObjCenter.SetConf(ConfIn)
        self.OrigQWeight = self.conf.GetConf('origqweight', self.OrigQWeight)
        
        
    def LoadQObj(self,QAnaInName):
        for line in open(QAnaInName).read().splitlines():
            vCol = line.strip().split('\t')
            qid = vCol[0]
            ObjId = vCol[2]
            score = vCol[-1]
            if not qid in self.hQObj:
                self.hQObj[qid] = [[ObjId,score]]
            else:
                self.hQObj[qid].append([ObjId,score])
                
        logging.info('qobj loaded from [%s]',QAnaInName)
        return True
    
    def RankScoreForDoc(self,qid,query,doc):
        DocKg = SearchResDocGraphConstructorC.LoadDocGraph(self.DocKgDir, qid, doc.DocNo)
        
        if not qid in self.hQObj:
            logging.warn('qid [%s] no ana obj, withdraw to given score',qid)
            return doc.score

        lQObjId = [item[0] for item in self.hQObj[qid]]
        lDocObjId = DocKg.hNodeId.keys()
        
        lQObj = [self.ObjCenter.FetchObj(ObjId) for ObjId in lQObjId]
        lDocObj =  [self.ObjCenter.FetchObj(ObjId) for ObjId in lDocObjId]
        
        score = self.Inferener.inference(query, doc, lQObj, lDocObj)
        
        return score
    
    def Rank(self,qid,query,lDoc):
        lScore = [self.RankScoreForDoc(qid, query, doc) for doc in lDoc]
        lDocNoScore = zip([doc.DocNo for doc in lDoc],lScore)
        lDocNoScore.sort(key=lambda item: item[1], reverse = True)
        lRankRes = [item[0] for item in lDocNoScore]
        return lRankRes
    
    


if __name__=='__main__':
    import sys
    from AdhocEva.RankerEvaluator import RankerEvaluatorC
    if 2 != len(sys.argv):
        print 'I evaluate LES '
        print 'in\nout'
        LESRanker.ShowConf()
        RankerEvaluatorC.ShowConf()
        
        sys.exit()
    
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    ch.setFormatter(formatter)
    
    
    
    conf = cxConfC(sys.argv[1])   
    QIn = conf.GetConf('in')
    EvaOut = conf.GetConf('out')
    
    Ranker = LESRanker(sys.argv[1])
    Evaluator = RankerEvaluatorC(sys.argv[1])
    Evaluator.Evaluate(QIn, Ranker.Rank, EvaOut)
  