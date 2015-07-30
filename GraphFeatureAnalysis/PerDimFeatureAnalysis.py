'''
Created on my MAC Jul 29, 2015-8:56:32 PM
What I do:
    I perform per dimension based feature analysis
What's my input:
    Feature data dir, target query list, target feature name
What's my output:
    the node pair and the feature dim value
    or binned value as statistics

@author: chenyanxiong
'''


import site
import logging
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')


from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from cxBase.Vector import VectorC
from cxBase.WalkDirectory import WalkDir
import json
import numpy as np

class PerDimFeatureAnalysiserC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.DataDir = ""
        self.QInName = ""
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DataDir = self.conf.GetConf('datadir') + '/'
#         self.QInName = self.conf.GetConf('qin')
        
        
        
        
    def LoadFeatureFromOneFile(self,InName):
        
        lLines = open(InName).read().splitlines()
        lvCol = [line.split('\t') for line in lLines]
        lTriple = [[item[0],item[1],json.loads(item[2])] for item in lvCol]
        
        return lTriple


    def PickTargetFeatureDim(self,lTriple,FeatureName):
        
        lRes = []
        for a,b,hFeature in lTriple:
            score = 0
            if FeatureName in hFeature:
                score = hFeature[FeatureName]
            lRes.append([a,b,score])
        return lRes
    
    
    def FetchTargetFeatureDim(self,FeatureName):
        '''
        fetch all target feature dim
        '''
        
        lQid = [line.split('\t')[0] for line in open(self.QInName).read().splitlines()]
        
        lRes = []
        
        lFName = WalkDir(self.DataDir)
        for InName in lFName:
            lTriple = self.LoadFeatureFromOneFile(InName)
            lRes.extend(self.PickTargetFeatureDim(lTriple, FeatureName))
                
        return lRes
    
    
    def HistogramFeatureDim(self,FeatureName,OutName):
        lRes = self.FetchTargetFeatureDim(FeatureName)
        lBin = np.histogram([item[2]  for item in lRes],10)
        
        out = open(OutName,'w')
        for i in range(len(lBin[0])):
            print >>out, '%s\t%s' %(lBin[0][i],lBin[1][i])
            
        out.close()
        logging.info('binned [%s] to [%s]',FeatureName,OutName)
        
        
        
        
if __name__ == '__main__':
    import sys
    if 4 != len(sys.argv):
        print "I analysis per dimension feature of graph feature"
        print 'data dir + feature name + output'
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)       

        
    Processor = PerDimFeatureAnalysiserC()
    Processor.DataDir = sys.argv[1]
    Processor.HistogramFeatureDim(sys.argv[2], sys.argv[3])
        
        
    
            
        
            
        
        
        
        
        
        
        
        
        
        
            
        
        