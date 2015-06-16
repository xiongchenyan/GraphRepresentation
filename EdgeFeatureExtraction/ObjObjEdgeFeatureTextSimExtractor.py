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

from IndriRelate.LmBase import LmBaseC
from ObjObjEdgeFeatureExtractor import ObjObjEdgeFeatureExtractorC
from IndriRelate.CtfLoader import TermCtfC

class ObjObjEdgeFeatureTextSimExtractorC(ObjObjEdgeFeatureExtractorC):
    
    def Init(self):
        ObjObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'TextSim'
        self.lObjField = ['name','desp','alias']
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
        
        
    def process(self, ObjA, ObjB):
        hFeature = {}
        hFeature.update(self.ExtractFieldJS(ObjA,ObjB))
        logging.debug('[%s]-[%s] obj text sim features extracted',ObjA.GetId(),ObjB.GetId())
        return hFeature
    
    def ExtractFieldJS(self,ObjA,ObjB):
        hFeature = {}
        
        for field in self.lObjField:
            FeatureName = self.FeatureName + field.title()
            LmA = LmBaseC(ObjA.GetField(field))
            LmB = LmBaseC(ObjB.GetField(field))
            score = LmBaseC.Similarity(LmA, LmB, self.CtfCenter, 'js')
            hFeature[FeatureName] = score
            
        return hFeature
        
        


