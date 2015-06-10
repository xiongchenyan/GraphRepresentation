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
        
        self.lSimName = [line.split('\t')[0] for line in lLines]
        self.lhObjPairSim = [pickle.load(open(line.split('\t')[1])) for line in lLines]
        
        logging.info('pre calc sim loaded as referenced by [%s]',self.PreCalcFileInName)
        
        
    def process(self, ObjA, ObjB):
        hFeature = {}
        
        hFeature.update(self.ExtractPreCalcSim(ObjA,ObjB))
        
        return hFeature
    
    def ExtractPreCalcSim(self,ObjA,ObjB):
        ObjAId = ObjA.GetId()
        ObjBId = ObjB.GetId()
        key = ObjAId + '\t' + ObjBId
        hFeature = {}
        for SimName,hSim in zip(self.lSimName,self.lhObjPairSim):
            score = 0
            if key in hSim:
                score = hSim[key]
            hFeature[self.FeatureName + SimName.title()] = score
        return hFeature
            
        




