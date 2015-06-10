'''
Created on my MAC Jun 10, 2015-2:59:54 PM
What I do:
edge feature between doc obj
for now only use facc confidence?
What's my input:
doc, obj
What's my output:
hFeature for them
@author: chenyanxiong
'''

'''
Again I am just a virtual to show API

'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging

class DocObjEdgeFeatureExtractorC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.FeatureName = 'DocObjEdge'
        
        
    def process(self,doc,obj):
        logging.warn('please call my subclass')
        return {}
        
        