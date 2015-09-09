'''
Created on Sep 9, 2015 12:23:33 PM
@author: cx

what I do:
    I am the base class for DocKg ranking
what's my input:

what's my output:


'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from DocGraphRepresentation.DocKnowledgeGraph import DocKnowledgeGraphC
import logging
from DocGraphRepresentation.ConstructSearchResDocGraph import SearchResDocGraphConstructorC


class GraphRankerC(cxBaseC):
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
        logging.error('need to be implemented by sub classes')
        raise NotImplementedError
    
    def Rank(self,qid,query,lDoc):
        if not qid in self.hQObj:
            logging.warn('qid [%s] no ana obj, withdraw to given score',qid)
            return [doc.DocNo for doc in lDoc]
        lScore = [self.RankScoreForDoc(qid, doc) for doc in lDoc]
        lMid = zip(lDoc,lScore)
        lDocNoScore = [[item[0].DocNo,item[1],item[0].score] for item in lMid]
        #sort doc by two keys, if boe scores tie, use original ranking score
        lDocNoScore.sort(key=lambda item: (item[1],item[2]), reverse = True)
        
        lRankRes = [item[0] for item in lDocNoScore]
        return lRankRes