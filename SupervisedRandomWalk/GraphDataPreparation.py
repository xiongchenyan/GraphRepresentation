'''
Created on my MAC Jun 20, 2015-8:09:52 PM
What I do:
    I prepare all useful data for graph ranking
        define output format：
            a dir


include:
    fetch qrel data save as vector
        
    read node-node-feature file
        transfer the raw graph to tensor
        dump feature-id node-id mapping
    write a set of file for each query?
        qname_{graph,nodeid,featureid,label}
    
        
IMPORTANT: there should be no missing feature for any input line
    
What's my input:
    EdgeFeatureExtractor's output:
        node node hFeature
        (first node in the line is query)
    qrel file
What's my output:
    four file for one query:
        query_graph (tensor pickle dump)
        query_label
        query_nodeid
        query_edgeid

@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.WalkDirectory import WalkDir
import ntpath
import numpy as np
import pickle,json
import logging
from cxBase.WalkDirectory import WalkDir
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from AdhocEva.AdhocQRel import AdhocQRelC

class GraphDataPreparationcC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.InDir = ""
        self.OutDir = ""
        
        self.QRelCenter = AdhocQRelC()
        
    
    
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.InDir = self.conf.GetConf('indir')
        self.OutDir = self.conf.GetConf('outdir')
        QRelInName = self.conf.GetConf('qrel')
        self.QRelCenter.Load(QRelInName)
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'indir\noutdir\nqrel'
        

    def UpdateHashId(self,name,hDict):
        if not name in hDict:
            hDict[name] = len(hDict)
            
    def GeneratePerQHashMapping(self,InName):
        hNodeId = {}
        lEdgeFeatureName = []
        for line in open(InName):
            NodeA,NodeB,FeatureStr = line.strip().split('\t')
            self.UpdateHashId(NodeA, hNodeId)
            self.UpdateHashId(NodeB, hNodeId)
            
            hFeature = json.loads(FeatureStr)
            lEdgeFeatureName.extend(hFeature.keys())
            
            
        lEdgeFeatureName = list(set(lEdgeFeatureName))
        lEdgeFeatureName.sort()  #make sure feature id is uniq
        hEdgeFeatureId = dict(zip(lEdgeFeatureName,range(len(lEdgeFeatureName))))
            
        logging.info('[%s] id made [%d] node [%d] edge feature',InName,len(hNodeId),len(hEdgeFeatureId))
        return hNodeId,hEdgeFeatureId
    
    def FormGraphTensorPerFile(self, InName,hNodeId,hEdgeFeatureId):
        '''
        form tensor for data in InName
        '''
        
        NodeN = len(hNodeId)
        FeatureDim = len(hEdgeFeatureId)
        logging.info('initializing [%d^2,-%d] graph tensor',NodeN,FeatureDim)
        GraphTensor = np.zeros((NodeN,NodeN,FeatureDim))
        
        
        for line in open(InName):
            NodeA,NodeB, FeatureStr = line.strip().split('\t')
            hFeature = json.loads(FeatureStr)
            
            AId = hNodeId[NodeA]
            BId = hNodeId[NodeB]
            for key,score in hFeature.items():
                FId = hEdgeFeatureId[key]
                GraphTensor[AId,BId,FId] = score
                
        return GraphTensor
    
    
    
    def ProcessOneQuery(self,InName):
        QName = ntpath.basename(InName)
        OutPre = self.OutDir + '/' + QName
        
        hNodeId,hEdgeFeatureId = self.GeneratePerQHashMapping(InName)
        
        pickle.dump(hNodeId,open(OutPre + '_NodeId','w'))
        pickle.dump(hEdgeFeatureId,open(OutPre + '_EdgeFeatureId','w'))
        logging.info('[%s] hash id dumped',QName)
        
        
        GraphTensor = self.FormGraphTensorPerFile(InName, hNodeId, hEdgeFeatureId)
        pickle.dump(GraphTensor,open(OutPre + '_Graph','w'))
        logging.info('[%s] graph tensor dumped',QName)
        
        
        QRelVec = self.FetchQRelVec(hNodeId)
        pickle.dump(QRelVec,open(OutPre + '_Label','w'))
        logging.info('[%s] label vec dumped',QName)
        
    
    
    def Process(self):
        lInName = WalkDir(self.InDir)
        
        for InName in lInName: 
            self.ProcessOneQuery(InName)

        logging.info('finished, data in [%s]',self.OutDir)
        
        
        

if __name__ == '__main__':
    import sys
    
    if 2 != len(sys.argv):
        print 'I made raw graph data to numpy format'
        GraphDataPreparationcC.ShowConf()
        sys.exit()
        
        
    Preparer = GraphDataPreparationcC(sys.argv[1])
    Preparer.Process()
        
        
        
        
    





