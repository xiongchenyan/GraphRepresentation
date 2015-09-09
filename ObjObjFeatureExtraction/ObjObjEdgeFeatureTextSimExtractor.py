'''
Created on my MAC Jun 10, 2015-4:30:05 PM
What I do:
extract text sim between two objects as features
What's my input:

What's my output:

@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
import json
from IndriRelate.LmBase import LmBaseC
from ObjObjFeatureExtraction.ObjObjEdgeFeatureExtractor import ObjObjEdgeFeatureExtractorC
from IndriRelate.CtfLoader import TermCtfC

class ObjObjEdgeFeatureTextSimExtractorC(ObjObjEdgeFeatureExtractorC):
    
    def Init(self):
        ObjObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'TextSim'
#         self.lObjField = ['name','desp','alias']
#         self.lFieldSimMetric = ['coor','js','cosine']
        self.lObjField = ['desp']
        self.lFieldSimMetric = ['cosine']        
        self.CtfCenter = TermCtfC()
        self.TermCtfIn = ""
        
    def SetConf(self, ConfIn):
        ObjObjEdgeFeatureExtractorC.SetConf(self, ConfIn)
        self.TermCtfIn = self.conf.GetConf('termctf')
        self.CtfCenter = TermCtfC(self.TermCtfIn)
        
    @staticmethod
    def ShowConf():
        ObjObjEdgeFeatureExtractorC.ShowConf()
        print 'termctf'    
        
    
    def FeatureDims(self):
        return [self.FeatureName + field.title() +  SimMetric.title() for SimMetric,field in zip(self.lFieldSimMetric,self.lObjField)]
        
    def process(self, ObjA, ObjB):
        hFeature = {}
        hFeature.update(self.ExtractTextSimFeature(ObjA,ObjB))
        logging.debug('[%s]-[%s] obj text sim features extracted %s',ObjA.GetId(),ObjB.GetId(),json.dumps(hFeature))
        return hFeature
    
    def ExtractTextSimFeature(self,ObjA,ObjB):
        hFeature = {}
        
        for SimMetric,field in zip(self.lFieldSimMetric,self.lObjField):
            
            FeatureName = self.FeatureName + field.title() + SimMetric.title()
            LmA = LmBaseC(ObjA.GetField(field))
            LmB = LmBaseC(ObjB.GetField(field))
            score = LmBaseC.Similarity(LmA, LmB, self.CtfCenter, SimMetric)
            hFeature[FeatureName] = score
            
        return hFeature
        
        


