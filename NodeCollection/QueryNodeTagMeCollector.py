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

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
from QueryNodeCollector import QueryNodeCollectorC

class QueryTagMeNodeCollectorC(QueryNodeCollectorC):
    
    def Init(self):
        QueryNodeCollectorC.Init(self)
        self.hQObjId = {}
        self.TagMeCacheInName = ""
        
        
    def SetConf(self, ConfIn):
        QueryNodeCollectorC.SetConf(self, ConfIn)
        self.TagMeCacheInName = self.conf.GetConf('querytagmecache')
        self.LoadTagMeObj()
        
    @staticmethod
    def ShowConf():
        QueryNodeCollectorC.ShowConf()
        print 'querytagmecache'
        
    def LoadTagMeObj(self):
        lData = open(self.TagMeCacheInName).read().splitlines()
        for data in lData:
            vCol = data.split('\t')
            qid = vCol[0]
            ObjId = vCol[2]
            score = float(vCol[-1])
            
            if not qid in self.hQObjId:
                self.hQObjId[qid] = [[ObjId,score]]
            else:
                self.hQObjId[qid].append([ObjId,score])
        logging.info('TagMe query cache loaded from [%s]',self.TagMeCacheInName)
        return
    
    
    def process(self, qid, query):
        if not qid in self.hQObjId:
            return []
        return self.hQObjId[qid]
            
            
            
