'''
Created on my MAC Jun 10, 2015-3:00:43 PM
What I do:
edge features between objs
the key factor (I believe)
What's my input:
obj id-obj id
What's my output:
hFeature
    Current TargetFeature:
        text sim
        connected in Fb (idf edge)
        correlation in FACC1 (pre generated)
        correlation in FAKBA (pre generated)
        embedding sim (google word2vec)
note that the feature in directed (A->B != B->A)        
@author: chenyanxiong
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging


class ObjObjEdgeFeatureExtractorC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.FeatureName = 'ObjObjEdge'
        
    def process(self,ObjA,ObjB):
        logging.warn('please call my sub class')
        return {}
    
    def FeatureDims(self):
        raise NotImplementedError