'''
Created on my MAC Jun 9, 2015-7:56:45 PM
What I do:
I read tagged query results
What's my input:
query + tag me cache results
What's my output:
lObjId for each query
@author: chenyanxiong
'''


'''
June 20
Change to QueryPreFetchedNodeCollectorC
conf becomes a file, each line:
    name cachefilename
     
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
from QueryNodeCollector import QueryNodeCollectorC

class QueryPreFetchedNodeCollectorC(QueryNodeCollectorC):
    
    def Init(self):
        QueryNodeCollectorC.Init(self)
#         self.hQObjId = {}
#         self.TagMeCacheInName = ""
        self.PreFetchInName = ""
        self.lSourceName = []
        self.lSourceFile = []
        self.lhQObjId = []
        
        
    def SetConf(self, ConfIn):
        QueryNodeCollectorC.SetConf(self, ConfIn)
        self.PreFetchInName = self.conf.GetConf('qanaconf')
        self.LoadPreFetchedNodes()
        
    @staticmethod
    def ShowConf():
        QueryNodeCollectorC.ShowConf()
        print 'qanaconf'
        
    def LoadOneSourceObj(self,InName):
        lData = open(InName).read().splitlines()
        hQObjId = {}
        for data in lData:
            vCol = data.split('\t')
            qid = vCol[0]
            ObjId = vCol[2]
            score = float(vCol[-1])
            
            if not qid in hQObjId:
                hQObjId[qid] = [[ObjId,score]]
            else:
                hQObjId[qid].append([ObjId,score])
        logging.info('query cache loaded from [%s]',InName)
        
        return hQObjId
    
    
    def LoadPreFetchedNodes(self):
        lLines = open(self.PreFetchInName).read().splitlines()
        lvCol = [line.split() for line in lLines]
        
        self.lSourceName =[vCol[0] for vCol in lvCol]
        self.lSourceFile = [vCol[1] for vCol in lvCol]
        self.lhQObjId = [self.LoadOneSourceObj(InName) for InName in self.lSourceFile]
        logging.info('pre fecthed q node loaded')
        return
    
    
    
    
    def process(self, qid, query):
        lObj = []
        for hQObjId in self.lhQObjId:
            if not qid in hQObjId:
                continue
            lObj.extend(hQObjId[qid])
        return lObj
            
            
            
