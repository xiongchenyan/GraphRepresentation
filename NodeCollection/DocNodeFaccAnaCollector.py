'''
Created on my MAC Jun 9, 2015-8:19:22 PM
What I do:
Read doc's facc annotation as doc's associated node
What's my input:
lDoc for one query
What's my output:

@author: chenyanxiong
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
from Facc.FaccDataCenter import FaccDataCenterC

class DocNodeFaccAnaCollectorC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.FaccDataCenter = FaccDataCenterC()
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.FaccDataCenter.SetConf(ConfIn)
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf() 
        FaccDataCenterC.ShowConf()   
        
    def process(self,lDoc,qid,query):
        lFaccDoc = self.FaccDataCenter.FetchFaccForQ(query)
        
        hDocMap = dict(zip([facc.DocNo for facc in lFaccDoc],range(len(lFaccDoc))))
        
        llNodeScore = []
        FindCnt = 0
        for doc in lDoc:
            if not doc.DocNo in hDocMap:
                llNodeScore.append([])
                continue
            lAnaRes = lFaccDoc[hDocMap[doc.DocNo]].lFacc
            lThisNodeScore = [[ana.DocNo,ana.Prob] for ana in lAnaRes]
            llNodeScore.append(lThisNodeScore)
            FindCnt += 1
        logging.info('query [%s] doc facc ana node get [%d/%d]',query,FindCnt,len(lDoc))
        return llNodeScore
        