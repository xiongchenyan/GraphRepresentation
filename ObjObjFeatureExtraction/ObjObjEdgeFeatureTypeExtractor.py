'''
Created on Jul 28, 2015 4:00:56 PM
@author: cx

what I do:
     I extract the type oriented features for two objs
what's my input:
    obj obj
what's my output:
    avg frac of same type
    number of same type
    whether notable type same

'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
from ObjObjFeatureExtraction.ObjObjEdgeFeatureExtractor import ObjObjEdgeFeatureExtractorC
import json
class ObjObjEdgeFeatureTypeExtractorC(ObjObjEdgeFeatureExtractorC):
    
    def Init(self):
        ObjObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'Type'
        self.lFeatureName = [self.FeatureName + item for item in ['HasSame','SameTypeFrac','SameNotable']]
        
        
    def process(self, ObjA, ObjB):
        hFeature = {}
        logging.debug('extracting type sim feature for [%s]-[%s]',ObjA.GetId(),ObjB.GetId())
        hFeature.update(self.ExtractTypeSimFeature(ObjA,ObjB))
        hFeature.update(self.ExtractNotableTypeSimFeature(ObjA,ObjB))
        logging.debug('type feature: %s',json.dumps(hFeature))
        return hFeature
    
    def FeatureDims(self):
        return self.lFeatureName
    
    def ExtractTypeSimFeature(self,ObjA,ObjB):
        
        hFeature = {}
        
        lAType = ObjA.GetField('type')
        lBType = ObjB.GetField('type')
        
        sB = set(lBType)
        OverlapCnt = 0
        for a in lAType:
            if a in sB:
                OverlapCnt += 1
                
        hFeature[self.FeatureName + 'HasSame'] = min(OverlapCnt,1)
        hFeature[self.FeatureName + 'SameTypeFrac'] = float(OverlapCnt) / float(max((len(lAType) + len(lBType) / 2.0),1))
        
        return hFeature
        
    def ExtractNotableTypeSimFeature(self,ObjA,ObjB):
        hFeature = {}
        ANotable = ObjA.GetField('NotableType')
        BNotable = ObjB.GetField('NotableType')
        score = 0
        if (ANotable == BNotable) & (ANotable != ""):
            score = 1  
        hFeature[self.FeatureName + 'SameNotable'] = score
        
        return hFeature
        
        
        
    