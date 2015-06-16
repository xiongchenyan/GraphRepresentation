'''
Created on my MAC Jun 10, 2015-3:25:41 PM
What I do:
get tagme score for q obj
if not annotated, them 0
What's my input:
q, obj
What's my output:
hFeature
@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')


from cxBase.base import cxBaseC
import logging
from EdgeFeatureExtraction.QueryObjEdgeFeatureExtractor import QueryObjEdgeFeatureExtractorC


class QueryObjEdgeFeatureTagMeExtractorC(QueryObjEdgeFeatureExtractorC):
    
    def Init(self):
        QueryObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'TagMe'
        self.TagMeCacheInName = ""
        self.hQObjAnaScore = {}
        
    def SetConf(self, ConfIn):
        QueryObjEdgeFeatureExtractorC.SetConf(self, ConfIn)
        
        self.TagMeCacheInName = self.conf.GetConf('querytagmecache')
        self.LoadQObjTagMeRho()
        
        
        
    @staticmethod
    def ShowConf():
        QueryObjEdgeFeatureExtractorC.ShowConf()
        print 'querytagmecache'
        
    
    def LoadQObjTagMeRho(self):
        lLines = open(self.TagMeCacheInName).read().splitlines()
        
        lQObjRho = [[vCol[0],vCol[2],vCol[-1]] for vCol in lLines]
        lKeyRho = [[item[0] + '\t' + item[1],item[2]] for item in lQObjRho]
        
        self.hQObjAnaScore = dict(lKeyRho)
        logging.info('load qobj tagme rho from [%s] done',self.TagMeCacheInName)
    
    def process(self, qid, query, obj):
        hFeature = {}
        ObjId = obj.GetId()
        hFeature.update(self.GetTagMeRhoFeature(qid,ObjId))
        
        return hFeature
    
    def GetTagMeRhoFeature(self,qid,ObjId):
        key = qid + '\t' + ObjId
        score = 0
        
        if key in self.hQObjAnaScore:
            score = self.hQObjAnaScore[key]
        
        hFeature = {}
        hFeature[self.FeatureName + 'Rho'] = score
        return hFeature
        
        
        
    
    