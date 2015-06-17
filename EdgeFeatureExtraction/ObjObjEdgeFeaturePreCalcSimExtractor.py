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
from IndriSearch.IndriSearchCenter import IndriSearchCenterC

class ObjObjEdgeFeaturePreCalcSimExtractorC(ObjObjEdgeFeatureExtractorC):
    
    def Init(self):
        ObjObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'PreCalc'
        
        self.PreCalcFileInName = ""
        self.lSimName = []  #read from PreCalcFileInName's referenced files 
        self.lPreCalcDir = []   #the dir contains query's obj sim dict 
        self.lDirected = []   #whether is directed
        self.lhQueryObjPairSim = []   #l [{}for each pre calc sim  ] {query -> hobjpairsim}}  
        
        
    def SetConf(self, ConfIn):
        ObjObjEdgeFeatureExtractorC.SetConf(self, ConfIn)
        self.PreCalcFileInName = self.conf.GetConf('precalcsimfile')
        self.SetPreCalcSim()
        
    @staticmethod
    def ShowConf():
        ObjObjEdgeFeatureExtractorC.ShowConf()
        print 'precalcsimfile'
        
    def SetPreCalcSim(self):
        lLines = open(self.PreCalcFileInName).read().splitlines()
        lvCol = [line.split() for line in lLines]
        self.lSimName = [vCol[0] for vCol in lvCol]
        self.lPreCalcDir = [vCol[1] for vCol in lvCol]
        self.lDirected = [int(vCol[2]) for vCol in lvCol]
        self.lhQueryObjPairSim = [{} for vCol in lvCol]
        logging.info('pre calc sim setted as referenced by [%s]',self.PreCalcFileInName)
        
        
    def LoadOneQueryObjSim(self,query):
        for i in range(len(self.lPreCalcDir)):
            InName = self.lPreCalcDir[i] +'/' + IndriSearchCenterC.GenerateQueryTargetName(query)
            if not os.path.exists(InName):
                return False
            hObjPairSim = pickle.load(open(InName))
            self.lhQueryObjPairSim[i][query] = hObjPairSim
        logging.info('query [%s] obj sim loaded',query)
        return True
        
        
        
    def process(self, ObjA, ObjB,query):
        hFeature = {}
        logging.debug('[%s-%s] precalc sim features:',ObjA.GetId(),ObjB.GetId())
        hFeature.update(self.ExtractPreCalcSim(ObjA,ObjB,query))
        return hFeature
    
    def ExtractPreCalcSim(self,ObjA,ObjB,query):
        if not query in self.lhQueryObjPairSim[0]:
            if not self.LoadOneQueryObjSim(query):
                return {}
              
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
            hSim = self.lhQueryObjPairSim[i][query]
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
            
        




