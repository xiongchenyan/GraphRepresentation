'''
Created on Sep 9, 2015 1:59:04 PM
@author: cx

what I do:
    I rank doc via q obj's p-r score in doc Kg
what's my input:
    I am a sub class of GraphRanker
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

from GraphRanker import GraphRankerC
import numpy as np


class PageRankRankerC(GraphRankerC):
    
    def Init(self):
        GraphRankerC.Init(self)
        self.ReStartP = 0.1
    
    def SetConf(self, ConfIn):
        GraphRankerC.SetConf(self, ConfIn)
        self.ReStartP = self.conf.GetConf('restartp', self.ReStartP)
        
    @staticmethod
    def ShowConf():
        GraphRankerC.ShowConf()
        print 'restartp'
    
    def RankScoreForDoc(self, qid, doc):
        DocKg = SearchResDocGraphConstructorC.LoadDocGraph(self.DocKgDir, qid, doc.DocNo)
        lQObj = self.hQObj[qid]
        
        M = (1.0 - self.ReStartP) * DocKg.mEdgeMatrix + self.ReStartP * (np.diag(DocKg.vNodeWeight)) 
        vPR = self.MaximalEigenvector(M)
        score = 0

        for ObjId,weight in lQObj:
            ObjScore = 0
            if ObjId in DocKg:
                ObjScore = vPR[DocKg.hNodeId[ObjId]]
            score += ObjScore * weight
            logging.info('[%s] [%s] - [%s] obj PR score: %f',qid,doc.DocNo,ObjId,ObjScore)
        logging.info('[%s] [%s] ranking score: %f',qid,doc.DocNo,score)
        return score
    
    
    
    def MaximalEigenvector(self,M):
        """ using the eig function to compute eigenvectors """
        n = M.shape[1]
        w,v = np.linalg.eig(M)
        return abs(np.real(v[:n,0]) / np.linalg.norm(v[:n,0],1))