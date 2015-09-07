'''
Created on Sep 1, 2015 5:08:04 PM
@author: cx

what I do:
    I rank doc via Boe lm model
what's my input:
    q's entity (as in q ana format)
    pre given doc graph dir
    

what's my output:
    the ranking of a given set of doc
        via BOE model (simply the doc's q'e weights)

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from DocGraphRepresentation.DocKnowledgeGraph import DocKnowledgeGraphC
import numpy as np
from BoeLanguageModel.BoeLmBase import BoeLmC
import logging
from DocGraphRepresentation.ConstructSearchResDocGraph import SearchResDocGraphConstructorC


class BoeLmRankerC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.hQObj = {}
        self.DocKgDir = ""
        self.Inferencer = BoeLmC()
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DocKgDir = self.conf.GetConf('dockgdir')
        QAnaInName = self.conf.GetConf('qanain')
        self.LoadQObj(QAnaInName)
        
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'dockgdir\nqanain'
        
    def LoadQObj(self,QAnaInName):
        for line in open(QAnaInName).read().splitlines():
            vCol = line.strip().split('\t')
            qid = vCol[0]
            ObjId = vCol[2]
            score = float(vCol[-1])
            if not qid in self.hQObj:
                self.hQObj[qid] = [[ObjId,score]]
            else:
                self.hQObj[qid].append([ObjId,score])
                
        logging.info('qobj loaded from [%s]',QAnaInName)
        return True
    
    
    def RankScoreForDoc(self,qid,doc):
        DocKg = SearchResDocGraphConstructorC.LoadDocGraph(self.DocKgDir, qid, doc.DocNo)
        lQObj = self.hQObj[qid]
        score = 0
        for ObjId,weight in lQObj:
            ObjPb = self.Inferencer.inference(ObjId, DocKg)
            score += ObjPb * weight
            logging.info('[%s] [%s] - [%s] obj score: %f',qid,doc.DocNo,ObjId,ObjPb)
        logging.info('[%s] [%s] ranking score: %f',qid,doc.DocNo,score)
        return score
    
    def Rank(self,qid,query,lDoc):
        if not qid in self.hQObj:
            logging.warn('qid [%s] no ana obj, withdraw to given score',qid)
            return [doc.DocNo for doc in lDoc]
        lScore = [self.RankScoreForDoc(qid, doc) for doc in lDoc]
        lDocNoScore = zip([doc.DocNo for doc in lDoc],lScore)
        lDocNoScore.sort(key=lambda item: item[1], reverse = True)
        lRankRes = [item[0] for item in lDocNoScore]
        return lRankRes
    
    
    

if __name__=='__main__':
    import sys,os
    from AdhocEva.RankerEvaluator import RankerEvaluatorC
    if 2 != len(sys.argv):
        print 'I evaluate Boe lm '
        print 'in\nout'
        BoeLmRankerC.ShowConf()
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
    
    Ranker = BoeLmRankerC(sys.argv[1])
    Evaluator = RankerEvaluatorC(sys.argv[1])
    Evaluator.Evaluate(QIn, Ranker.Rank, EvaOut)
     
    
        
        
        
        
        
            
            
        
        




