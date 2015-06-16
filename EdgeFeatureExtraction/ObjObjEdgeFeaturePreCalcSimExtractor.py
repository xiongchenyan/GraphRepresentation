'''
Created on my MAC Jun 10, 2015-5:19:57 PM
What I do:
extract feature from pre calculated obj-obj correlation
e.g.
    facc correlation
    fakba correlation
    embedding similarity
    
What's my input:
I am a sub class of ObjObjEdgeFeatureExtractorC

my conf is a line:
    objprecalcsimilarity filename
the filename contains:
    each line:
        correlation name \t pickle dict (obj\tobj -> score)
        
I will read these file, cache them, and for each pair of obj, get its score in each
What's my output:
hFeature
@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
from EdgeFeatureExtraction.ObjObjEdgeFeatureExtractor import ObjObjEdgeFeatureExtractorC
import pickle

class ObjObjEdgeFeaturePreCalcSimExtractorC(ObjObjEdgeFeatureExtractorC):
    
    def Init(self):
        ObjObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'PreCalc'
        
        self.PreCalcFileInName = ""
        self.lSimName = []  #read from PreCalcFileInName's referenced files 
        self.lhObjPairSim = []
        self.lDirected = []   #whether is directed
        
        
    def SetConf(self, ConfIn):
        ObjObjEdgeFeatureExtractorC.SetConf(self, ConfIn)
        self.PreCalcFileInName = self.conf.GetConf('precalcsimfile')
        self.LoadPreCalcSim()
        
    @staticmethod
    def ShowConf():
        ObjObjEdgeFeatureExtractorC.ShowConf()
        print 'precalcsimfile'
        
    def LoadPreCalcSim(self):
        lLines = open(self.PreCalcFileInName).read().splitlines()
        lvCol = [line.split() for line in vCol]
        self.lSimName = [vCol[0] for vCol in lvCol]
        self.lhObjPairSim = [pickle.load(open(vCol[1])) for vCol in lvCol]
        self.lDirected = [int(vCol[2]) for vCol in lvCol]
        logging.info('pre calc sim loaded as referenced by [%s]',self.PreCalcFileInName)
        
        
    def process(self, ObjA, ObjB):
        hFeature = {}
        logging.debug('[%s-%s] precalc sim features:',ObjA.GetId(),ObjB.GetId())
        hFeature.update(self.ExtractPreCalcSim(ObjA,ObjB))
        return hFeature
    
    def ExtractPreCalcSim(self,ObjA,ObjB):
        ObjAId = ObjA.GetId()
        ObjBId = ObjB.GetId()
        key = ObjAId + '\t' + ObjBId
        if ObjAId > ObjBId:
            DirectKey = ObjBId + '\t' + ObjAId
        else:
            DirectKey = key
            
              
        hFeature = {}
        for i in range(len(self.lSimName)):
            SimName = self.lSimName[i]
            hSim = self.lhObjPairSim[i]
            Directed = self.lDirected[i]
            if Directed:
                ThisKey = DirectKey
            else:
                ThisKey = key
            score = 0
            if key in hSim:
                score = hSim[ThisKey]
            FeatureName = self.FeatureName + SimName.title()
            hFeature[FeatureName] = score
            logging.debug('[%s:%f]',FeatureName,score)
        return hFeature
            
        




