'''
Created on my MAC Jun 10, 2015-3:47:48 PM
What I do:
I extract edge feature for doc-obj, from facc
What's my input:
doc obj
FaccDir
What's my output:
    Facc Ana score
    Facc Ana no context score
@author: chenyanxiong
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
from EdgeFeatureExtraction.DocObjEdgeFeatureExtractor import DocObjEdgeFeatureExtractorC
from Facc.FaccDataCenter import FaccDataCenterC


class DocObjEdgeFeatureFaccExtractorC(DocObjEdgeFeatureExtractorC):
    
    def Init(self):
        DocObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'Facc'
        self.FaccCenter = FaccDataCenterC()
        self.hDocObjProb = {}
        
        
        
    def SetConf(self, ConfIn):
        DocObjEdgeFeatureExtractorC.SetConf(self, ConfIn)
        self.FaccCenter.SetConf(ConfIn)
        self.hDocObjProb = self.FaccCenter.FetchAllAnnotation()
        
    @staticmethod
    def ShowConf():
        DocObjEdgeFeatureExtractorC.ShowConf()
        FaccDataCenterC.ShowConf()
        
    def process(self, doc, obj):
        hFeature = {}
        
        hFeature.update(self.ExtractFaccAnaProbFeature(doc,obj))
        logging.debug('doc [%s] obj [%s] facc feature extracted [%s]',doc.DocNo,obj.GetId())
        return hFeature
    
    def ExtractFaccAnaProbFeature(self,doc,obj):
        key = doc.DocNo + '\t' + obj.GetId()
        
        score = 0
        if key in self.hDocObjProb:
            score = self.hDocObjProb[key]
        
        
        FeatureName = self.FeatureName + 'AnaProb'
        logging.debug('%s:%f',FeatureName,score)
        return {FeatureName:score}



