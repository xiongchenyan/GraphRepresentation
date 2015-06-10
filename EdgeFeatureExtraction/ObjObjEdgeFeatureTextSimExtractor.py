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


class ObjObjEdgeFeatureTextSimExtractorC(ObjObjEdgeFeatureExtractorC):
    
    def Init(self):
        ObjObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'TextSim'
        self.lObjField = ['name','desp','alias']
        
    def SetConf(self, ConfIn):
        ObjObjEdgeFeatureExtractorC.SetConf(self, ConfIn)
        
        
        


