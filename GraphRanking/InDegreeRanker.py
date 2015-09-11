'''
Created on Sep 9, 2015 12:22:24 PM
@author: cx

what I do:
    rank doc by q entity's in degree in DocKg
    
what's my input:
    q's entity (as in q ana format)
    pre given doc graph dir
what's my output:
    the ranking using indegree


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

class InDegreeRankerC(GraphRankerC):
    
    def RankScoreForDoc(self, qid, doc):
        logging.debug('start in degree ranking for [%s-%s]',qid,doc.DocNo)

        DocKg = SearchResDocGraphConstructorC.LoadDocGraph(self.DocKgDir, qid, doc.DocNo)
        if len(DocKg.hNodeId) == 0:
            return 0  #no kg, default min zero score
        logging.debug('[%s] doc kg loaded, [%d] [%d-%d]',DocKg.DocNo,\
                      DocKg.vNodeWeight.shape[0],DocKg.mEdgeMatrix.shape[0],DocKg.mEdgeMatrix.shape[1])
        DocKg.NormalizeEdgeMtx()
        lQObj = self.hQObj[qid]
        score = 0
        for ObjId,weight in lQObj:
            
            ObjScore = self.ScoreForOneQObj(ObjId, DocKg)
            score += ObjScore * weight
#             logging.info('[%s] [%s] - [%s] obj score: %f',qid,doc.DocNo,ObjId,ObjScore)
        logging.info('[%s] [%s] ranking score: %f',qid,doc.DocNo,score)
        return score
    
    def ScoreForOneQObj(self,QObjId,DocKg):
        
        score = 0
        if QObjId in DocKg:
            p = DocKg.hNodeId[QObjId]
            score = np.sum(DocKg.mEdgeMatrix[:,p])
            logging.debug('q obj [%s] indegree [%f]',QObjId,score)
        else:
            logging.debug('q obj [%s] not in doc',QObjId)
        return score
        
        


