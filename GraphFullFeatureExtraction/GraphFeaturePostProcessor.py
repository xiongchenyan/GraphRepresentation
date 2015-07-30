'''
Created on Jul 22, 2015 3:27:15 PM
@author: cx

what I do:
I read the raw features
    normalize per query basis
    transfer to numpy arrays
what's my input:
    dir of extracted graph features
what's my output:
    another dir, same tree, same files, but in pickle dump numpy array format


'''

'''
for each q:
    read and get min max of the feature
for each q-doc's graph
    read features
    normalize
    transfer to mtx and tensor
    dump
'''

'''
work log:

7/22/2015
    implemented
    
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')


from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from cxBase.Vector import VectorC
from AdhocEva.AdhocQRel import AdhocQRelC
from cxBase.WalkDirectory import WalkDir
from FeatureProcess.FeatureProcessor import FeatureProcessorC


import logging
import pickle
import ntpath
import os
import json
import numpy

class GraphFeaturePostProcessorC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        
        self.RelCenter = AdhocQRelC()
        self.InDir = ""
        self.OutDir = ""
        
        self.hNodeFeatureId = {}  #the id of node features
        self.hEdgeFeatureId = {} #the id of edge features
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.InDir = self.conf.GetConf('indir') + '/'
        self.OutDir = self.conf.GetConf('outdir') + '/'
        self.RelCenter.SetConf(ConfIn)
        
    
    @classmethod
    def ShowConf(cls):
        cxBaseC.ShowConf()
        print cls.__name__
        print 'indir\noutdir'
        AdhocQRelC.ShowConf()
        
        
        
    
    def HashFeatureName(self):
        '''
        go through the full input dir, hash node features and edge features
        '''
        
        sNodeFeatureName = set()
        sEdgeFeatureName = set()
        
        lFName = WalkDir(self.InDir)
        
        for FName in lFName:
#             logging.info('checking feature names in [%s]',FName)
            lLines = open(FName).read().splitlines()
            lNodeLines = [line for line in lLines if self.IsNodeFeatureLine(line)]
            lEdgeLines = [line for line in lLines if not self.IsNodeFeatureLine(line)]
            
            sNodeFeatureName.update(self.GetFeatureName(lNodeLines))
            sEdgeFeatureName.update(self.GetFeatureName(lEdgeLines))
            
            
            
        
        self.MakeNodeFeatureHash(sNodeFeatureName)
        self.MakeEdgeFeatureHash(sEdgeFeatureName)
        
        logging.info('feature hash id assigned')
        return True
    
    
    def MakeNodeFeatureHash(self,sNodeFeatureName):
        '''
        put LeToR features first
        '''
        lName = list(sNodeFeatureName)
        
        lLtrName = [name for name in lName if name.startswith('LeToR')]
        lObjName = [name for name in lName if not name.startswith('LeToR')]
        
        lLtrName.sort()
        lObjName.sort()
        
        lName = lLtrName + lObjName
        
        self.hNodeFeatureId = dict(zip(lName,range(len(lName))))
        
        
        return True
    
    def MakeEdgeFeatureHash(self,sEdgeFeatureName):
        '''
        put QObj features first
        '''
        lName = list(sEdgeFeatureName)
        
        lQObjName = [name for name in lName if name.startswith('QObj')]
        lObjObjName = [name for name in lName if not name.startswith('QObj')]
        
        lQObjName.sort()
        lObjObjName.sort()
        
        lName = lQObjName + lObjObjName
        
        self.hEdgeFeatureId = dict(zip(lName,range(len(lName))))
        
        return True
    
    
    
    def GetFeatureName(self,lLines):
#         lhFeature = []
#         for line in lLines:
#             FStr = line.split('\t')[-1]
#             try:
#                 hFeature = json.loads(FStr)
#                 lhFeature.append(hFeature)
#             except ValueError:
#                 logging.error('[%s] cannot be json loaded', FStr)
#                 sys.exit()
        
        lhFeature = [json.loads(line.split('\t')[-1]) for line in lLines]
        
        lName = []
        for hFeature in lhFeature:
            lName.extend(hFeature.keys())
            
        return set(lName)
        
        
    
    

    def FindMaxMinFeatureValuesForQ(self,QDir):
        '''
        find the max and min feature values of this query
            so I perform max-min normalization per query level
            Should work too and is simple
        '''
        hFeatureMax = {}
        hFeatureMin = {}
        lDocName = WalkDir(QDir)
        for DocName in lDocName:
            logging.info('finding max min of [%s]',DocName)
            for line in open(DocName):
                vCol = line.strip().split('\t')
                hFeature = json.loads(vCol[-1])
                hFeatureMax = FeatureProcessorC.Max(hFeature, hFeatureMax)
                hFeatureMin = FeatureProcessorC.Min(hFeature,hFeatureMin)
        
        logging.info('q [%s] max-min feature score get',ntpath.basename(QDir))
        
        return hFeatureMax,hFeatureMin
    
    def ProcessOneDoc(self,Qid,DocInName,hFeatureMax,hFeatureMin):
        '''
        read data
        hash to node id
        normalize
        fetch rel label
        dump node mtx
        dump edge tensor
        dump rel label
        dump node name -> id
        '''
        
        lLines = open(DocInName).read().splitlines()
        lNodeLines = [line for line in lLines if self.IsNodeFeatureLine(line)]
        lEdgeLines = [line for line in lLines if not self.IsNodeFeatureLine(line)]
        
        hNodeId = self.HashPerDocNode(lNodeLines)

        
        NodeMtx = self.FormNodeMtx(lNodeLines,hNodeId,hFeatureMax,hFeatureMin)
        EdgeTensor = self.FormEdgeTensor(lEdgeLines,hNodeId,hFeatureMax,hFeatureMin)


        DocNo = ntpath.basename(DocInName)
        rel = self.RelCenter.GetScore(Qid, DocNo)
        
        
        OutName = self.OutDir + '/' + Qid + '/' + DocNo
        if not os.path.exists(self.OutDir + '/' + Qid ):
            os.makedirs(self.OutDir + '/' + Qid )
        out = open(OutName,'w')
        
        pickle.dump([NodeMtx,EdgeTensor,rel,hNodeId],out)
        
        
        logging.info('[%s] processed and dumped',OutName)
        
        return True
    
    
    def HashPerDocNode(self,lLines):
        
        lNode = []
        QNode = ""
        for line in lLines:
            vCol = line.split('\t')
            for NodeName in vCol[:2]:
                if self.IsObjNode(NodeName):
                    lNode.append(NodeName)
                if self.IsQNode(NodeName):
                    QNode = NodeName
                    
        lNode = list(set(lNode))
        lNode.sort()
        lTotalNode = [QNode] + lNode
        
        hNodeId = dict(zip(lTotalNode,range(len(lTotalNode))))
        
        return hNodeId
            
    
    def FormNodeMtx(self,lNodeLines,hNodeId,hFeatureMax,hFeatureMin):
        '''
        make lines to node id, hFeature pair
        normalize hFeature
        put it in corresponding rows in NodeMtx
        '''        
        NodeMtx = numpy.zeros([len(hNodeId),len(self.hNodeFeatureId)])
        
        for line in lNodeLines:
            vCol = line.split('\t')
            NodeP = hNodeId[vCol[0]]
            
            hFeature = json.loads(vCol[-1])
            hFeature = FeatureProcessorC.MaxMinNormalization(hFeature, hFeatureMax,hFeatureMin)
            
            FeatureVec = FeatureProcessorC.VectorlizeFeature(hFeature, self.hNodeFeatureId)
            
            NodeMtx[NodeP] = FeatureVec
        
        logging.info('node feature matrix converted')
            
        return NodeMtx
    
    def FormEdgeTensor(self,lEdgeLines,hNodeId,hFeatureMax,hFeatureMin):
        '''
        make lines to node a, node b, hFeature triple
        normalize
        put it in corresponding cell in EdgeTensor
        '''
        
        EdgeTensor = numpy.zeros([len(hNodeId),len(hNodeId),len(self.hEdgeFeatureId)])
        
        for line in lEdgeLines:
            vCol = line.split('\t')
            NodeA = hNodeId[vCol[0]]
            NodeB = hNodeId[vCol[1]]
            hFeature = json.loads(vCol[2])
            hFeature = FeatureProcessorC.MaxMinNormalization(hFeature, hFeatureMax, hFeatureMin)
            
            FeatureVec = FeatureProcessorC.VectorlizeFeature(hFeature, self.hEdgeFeatureId)
        
            EdgeTensor[NodeA,NodeB] = FeatureVec
        
        logging.info('edge feature tensor converted')
            
        return EdgeTensor
        
            
        
            
            
            
    
    
    def Process(self):
        
        self.HashFeatureName()
        
        for QDir,mid,lDocName in os.walk(self.InDir):
            logging.info('start working on query dir [%s]',QDir)
            hFeatureMax,hFeatureMin = self.FindMaxMinFeatureValuesForQ(QDir)
            qid = ntpath.basename(QDir)
            for DocName in lDocName:
                self.ProcessOneDoc(qid, QDir + '/' + DocName, hFeatureMax, hFeatureMin)
                
            logging.info('q [%s] processed',qid)
        
        self.DumpFeatureHash()
        
        logging.info('feature normalized and transformed')
        return True
    
    
    def DumpFeatureHash(self):
        out = open(self.OutDir + 'NodeFeatureId','w')
        lNodeF = self.hNodeFeatureId.items()
        lNodeF.sort(key=lambda item:int(item[1]))
        print >>out, '\n'.join(['%s\t%s' %(item[0],item[1]) for item in lNodeF])
        out.close()
        
        out = open(self.OutDir + 'EdgeFeatureId','w')
        lEdgeF = self.hEdgeFeatureId.items()
        lEdgeF.sort(key=lambda item:int(item[1]))
        print >>out, '\n'.join(['%s\t%s' %(item[0],item[1]) for item in lEdgeF])
        out.close()
        logging.info('feature id name dumped')
        return    
        
    
    
    
    def IsQNode(self,NodeName):
        return NodeName.startswith('q_')
    
    def IsObjNode(self,NodeName):
        return NodeName.startswith('/m/')
    
    def IsNodeFeatureLine(self,line):
        vCol = line.split('\t')
        if self.IsQNode(vCol[1]) | self.IsObjNode(vCol[1]):
            return False
        return True
        



        
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print "I normalize and  convert graph features to numpy format"
        GraphFeaturePostProcessorC.ShowConf()
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)       

        
    Processor = GraphFeaturePostProcessorC(sys.argv[1])
    Processor.Process()
    
    
    
    
        
    
    
    
    
