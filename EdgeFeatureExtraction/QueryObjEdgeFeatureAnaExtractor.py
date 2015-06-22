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

'''
June 20
support multiple annotation input (TagMe and manual for now)
the conf is changed to a file:
    each line:
        source name \t annotation result file
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')


from cxBase.base import cxBaseC
import logging
from EdgeFeatureExtraction.QueryObjEdgeFeatureExtractor import QueryObjEdgeFeatureExtractorC


class QueryObjEdgeFeatureAnaExtractorC(QueryObjEdgeFeatureExtractorC):
    
    def Init(self):
        QueryObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'Ana'
        
        self.PreFetchInName = ""
        self.lSourceName = []
        self.lSourceFile = []
        self.lhQObjIdScore = []
        
    def SetConf(self, ConfIn):
        QueryObjEdgeFeatureExtractorC.SetConf(self, ConfIn)
        
        self.PreFetchInName = self.conf.GetConf('qanaconf')
        self.LoadAnaScore()
        
        
        
    @staticmethod
    def ShowConf():
        QueryObjEdgeFeatureExtractorC.ShowConf()
        print 'qanaconf'
        
    

    
    
    def LoadAnaScore(self):
        lLines = open(self.PreFetchInName).read().splitlines()
        lvCol = [line.split() for line in lLines]
        
        self.lSourceName =[vCol[0] for vCol in lvCol]
        self.lSourceFile = [vCol[1] for vCol in lvCol]
        self.lhQObjIdScore = [self.LoadOneSourceRho(InName) for InName in self.lSourceFile]
        logging.info('q ana score loaded')
        return
    
    
    def LoadOneSourceRho(self,InName):
        lLines = open(InName).read().splitlines()
        lvCol = [line.split('\t') for line in lLines]
        lQObjRho = [[vCol[0],vCol[2],float(vCol[-1])] for vCol in lvCol]
        lKeyRho = [[item[0] + '\t' + item[1],item[2]] for item in lQObjRho]
        
        hQObjAnaScore = dict(lKeyRho)
        logging.info('load qobj  rho from [%s] done',InName)
        return hQObjAnaScore
    
    def process(self, qid, query, obj):
        hFeature = {}
        ObjId = obj.GetId()
        hFeature.update(self.GetAnaRhoFeature(qid,ObjId))
        logging.debug('query [%s] - obj [%s] tag me feature extracted',query,ObjId)
        return hFeature
    
    def GetAnaRhoFeature(self,qid,ObjId):
        key = qid + '\t' + ObjId
        
        hFeature = {}
        for i in range(len(self.lSourceName)):
            hQObjAnaScore = self.lhQObjIdScore[i]
            
            score = 0
            if key in hQObjAnaScore:
                score = hQObjAnaScore[key]
                
            FeatureName = self.FeatureName + self.lSourceName[i] +  'Rho'
            hFeature[FeatureName] = score
            
            logging.debug('[%s][%s] [%s] rho [%f]',qid,ObjId,score)
            
            
        return hFeature
        
        
        
    
    