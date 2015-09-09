'''
Created on Jul 14, 2015 11:16:04 AM
@author: cx

what I do:
    I am a individual center for feature between obj-obj
what's my input:
    query obj-obj
what's my output:
    hFeature
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
import json
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
import pickle

from ObjObjFeatureExtraction.ObjObjEdgeFeatureKGExtractor import ObjObjEdgeFeatureKGExtractorC
from ObjObjFeatureExtraction.ObjObjEdgeFeaturePreCalcSimExtractor import ObjObjEdgeFeaturePreCalcSimExtractorC
from ObjObjFeatureExtraction.ObjObjEdgeFeatureTextSimExtractor import ObjObjEdgeFeatureTextSimExtractorC
from ObjObjFeatureExtraction.ObjObjEdgeFeatureTypeExtractor import ObjObjEdgeFeatureTypeExtractorC
from ObjObjFeatureExtraction.ObjObjEdgeFeatureEmbeddingExtractor import ObjObjEdgeFeatureEmbSimExtractorC
from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC


class ObjObjFeatureExtractCenterC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        
        self.lObjObjFeatureGroup = []
        
        self.ObjObjKGExtractor = ObjObjEdgeFeatureKGExtractorC()
        self.ObjObjPreCalcExtractor = ObjObjEdgeFeaturePreCalcSimExtractorC()
        self.ObjObjTextSimExtractor = ObjObjEdgeFeatureTextSimExtractorC()
        self.ObjObjTypeSimExtractor = ObjObjEdgeFeatureTypeExtractorC()
        self.ObjObjEmbSimExtractor = ObjObjEdgeFeatureEmbSimExtractorC() 
        self.NodeDir = ""
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.lObjObjFeatureGroup = self.conf.GetConf('objobjfeaturegroup', self.lObjObjFeatureGroup)
        
        
        if 'kg' in self.lObjObjFeatureGroup:
            self.ObjObjKGExtractor.SetConf(ConfIn)
        if 'precalc' in self.lObjObjFeatureGroup: 
            self.ObjObjPreCalcExtractor.SetConf(ConfIn)
        if 'textsim' in self.lObjObjFeatureGroup:
            self.ObjObjTextSimExtractor.SetConf(ConfIn)
        if 'typesim' in self.lObjObjFeatureGroup:
            self.ObjObjTypeSimExtractor.SetConf(ConfIn)
        if 'embsim' in self.lObjObjFeatureGroup:
            self.ObjObjEmbSimExtractor.SetConf(ConfIn)
            
            
        logging.info('edge feature center confs setted')
        
    @classmethod
    def ShowConf(cls):
        print cls.__name__
        FbObjCacheCenterC.ShowConf()
        
        print 'objobjfeaturegroup'
        
        ObjObjEdgeFeatureKGExtractorC.ShowConf()
        ObjObjEdgeFeaturePreCalcSimExtractorC.ShowConf()
        ObjObjEdgeFeatureTextSimExtractorC.ShowConf()
        ObjObjEdgeFeatureTypeExtractorC.ShowConf()
        ObjObjEdgeFeatureEmbSimExtractorC.ShowConf()
   
    
    def FeatureDims(self):
        lFeatureDims = []
        if 'kg' in self.lObjObjFeatureGroup:
            lFeatureDims += self.ObjObjKGExtractor.FeatureDims()
        if 'precalc' in self.lObjObjFeatureGroup: 
            lFeatureDims += self.ObjObjPreCalcExtractor.FeatureDims()
        if 'textsim' in self.lObjObjFeatureGroup:
            lFeatureDims += self.ObjObjTextSimExtractor.FeatureDims()
        if 'typesim' in self.lObjObjFeatureGroup:
            lFeatureDims += self.ObjObjTypeSimExtractor.FeatureDims()
        if 'embsim' in self.lObjObjFeatureGroup:
            lFeatureDims += self.ObjObjEmbSimExtractor.FeatureDims()
        return lFeatureDims
    
    
    
    def ExtractPerObjObj(self,ObjA,ObjB,query):
        hFeature = {}
        logging.debug('start extracting for obj pair [%s-%s]',ObjA.GetId(),ObjB.GetId())
        if 'kg' in self.lObjObjFeatureGroup:
            hFeature.update(self.ObjObjKGExtractor.process(ObjA, ObjB))
        if 'precalc' in self.lObjObjFeatureGroup:
            hFeature.update(self.ObjObjPreCalcExtractor.process(ObjA, ObjB,query))
        if 'textsim' in self.lObjObjFeatureGroup:
            hFeature.update(self.ObjObjTextSimExtractor.process(ObjA, ObjB))
        if 'typesim' in self.lObjObjFeatureGroup:
            hFeature.update(self.ObjObjTypeSimExtractor.process(ObjA, ObjB))
        if 'embsim' in self.lObjObjFeatureGroup:
            hFeature.update(self.ObjObjEmbSimExtractor.process(ObjA, ObjB))
            
        logging.debug('obj pair [%s-%s] feature extracted',ObjA.GetId(),ObjB.GetId())    
        return hFeature
    
    def ExtractObjObjFeature(self,lObj,query):
        llhFeature = []   #obj -> obj, diagonal is empty
        logging.info('start extract [%d] obj pair feature mtx',len(lObj))
        for ObjA in lObj:
            lhFeature = []
            for ObjB in lObj:
                hFeature = {}
#                 if ObjA.GetId() != ObjB.GetId():
                hFeature = self.ExtractPerObjObj(ObjA, ObjB,query)
                lhFeature.append(hFeature)
            llhFeature.append(lhFeature)
        
        logging.info('obj obj feature extracted')
        return llhFeature
    
    
    def Process(self,qid,query,lObj):
        
        llObjObjFeature = self.ExtractObjObjFeature(lObj,query)
        
        return llObjObjFeature
    
    
