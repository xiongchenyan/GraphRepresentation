'''
Created on Aug 9, 2015 3:09:57 PM
@author: cx

what I do:
    I am the data structure for document graph
what's my input:

what's my output:


'''


import pickle,logging,json
import numpy as np
import ntpath
import os

class DocGraphC(object):
    
    def __init__(self):
        self.NodeMtx = np.zeros([0,0])
        self.EdgeTensor = np.zeros([0,0,0])
        self.rel = 0
        self.hNodeId = {}
        self.NodeN = 0
        self.NodeFeatureDim = 0
        self.EdgeFeatureDim = 0
        self.DocNo = ""
        
    def SetDims(self):
        self.NodeN = self.NodeMtx.shape[0]
        self.NodeFeatureDim = self.NodeMtx.shape[1]
        self.EdgeFeatureDim = self.EdgeTensor.shape[2]
    
    
    def GetRelScore(self):
        return self.rel
    
        
    def PickEvidenceGroup(self,Group,InName = ""):
        '''
        choose evidecne group from data:
            letor: only query node features (node 0)
            esdrank: all node features, edge features only between node 0 and other nodes
            hccrf: everything            
        '''
        Group = Group.lower()
        if Group == 'letor':
            self.KeepLeToR()
        if Group == 'esdrank':
            self.KeepEsdRank()
            
        if Group == 'tagme':
            self.KeepEsdRankTagMeNode(InName)
            
        return
    
    
    def KeepLeToR(self):
        self.NodeMtx = self.NodeMtx[0,:].reshape([1,self.NodeMtx.shape[1]])
        self.EdgeTensor = self.EdgeTensor[0,0,:].reshape([1,1,self.EdgeTensor.shape[2]])
#         logging.debug('restrict graph data to LeToR only')
        
    def KeepEsdRank(self):
        self.EdgeTensor[1:,1:,:] = 0 
#         logging.debug('restrict graph data to EsdRank only (no obj-obj edges)')
        
    
    def KeepEsdRankTagMeNode(self,InName):
        hFeature = self.ReadEdgeFeatureFromDir(InName)
        
        TagMeDim = hFeature['QObjSourceScore_TagMe']
        
        lTargetNode = [0]
        for i in range(1,self.EdgeTensor.shape[1]):
            if self.EdgeTensor[0,i,TagMeDim] != 0:
                lTargetNode.append(i)
                
        self.NodeMtx = self.NodeMtx[lTargetNode,:]
        self.EdgeTensor = self.EdgeTensor[lTargetNode,:,:][:,lTargetNode,:]
        
#         logging.debug('[%s] keep node %s',InName,json.dumps(lTargetNode))
#         logging.debug('node shape %s, edge shape %s',json.dumps(self.NodeMtx.shape),json.dumps(self.EdgeTensor.shape))    
        
        
        

    def ReadEdgeFeatureFromDir(self,InName):
        vCol = InName.split('/')
        vCol = [item for item in vCol if item]
        EdgeFeatureName = '/'+ '/'.join(vCol[:-2]) + '/EdgeFeatureId'
        
        lLines = open(EdgeFeatureName).read().splitlines()
        hFeature = dict([line.split('\t') for line in lLines])
        return hFeature
    
    
    
    def EdgeTensorSymmetricCheck(self):
        '''
        checking graphdata,
            if the edge tensor not symmetric, 
                using average (convert directed edge to undirected edge)
        '''
        for i in range(self.EdgeFeatureDim):
            if not np.array_equal(self.EdgeTensor[:,:,i].T,self.EdgeTensor[:,:,i]):
#                 logging.warn('Graph Edge Tensor [%d] dim not symmetric',i)
                self.EdgeTensor[:,:,i] = (self.EdgeTensor[:,:,i] + self.EdgeTensor[:,:,i].T)/ 2.0
#                 Mtx = GraphData.EdgeTensor[:,:,i]
#                 ErrorMtx = [(a,b,Mtx[a,b],Mtx[b,a]) for a in range(Mtx.shape[0]) for b in range(a+1,Mtx.shape[1]) if Mtx[a,b] != Mtx[b,a]]
#                 logging.warn(ErrorMtx)
#                 logging.warn(GraphData.EdgeTensor[:,:,i])
    
    
    
    def Load(self,InName):
        [self.NodeMtx,self.EdgeTensor,self.rel,self.hNodeId] = pickle.load(open(InName))
        self.DocNo = ntpath.basename(InName)
        self.EdgeTensorSymmetricCheck()
        self.SetDims()
        return True
    
    
    def Dump(self,OutName):
        pickle.dump([self.NodeMtx,self.EdgeTensor,self.rel,self.hNodeId],open(OutName,'w'))
        return True
    
    @classmethod
    def LoadEsdRankOneQGraph(cls,InDir,qid):
        '''
        load the per query graph from EsdRank's datadir
        
        Aug/9/2015 only support loading query node only
        '''
        lGraphData = []
        
        lDocNo = open(InDir + '/' + qid + '_doc_docNo').read().splitlines()
        lRelScore = open(InDir + '/' + qid + '_label').read().splitlines()
        
        for i in range(len(lDocNo)):
            GraphData = DocGraphC()
            
            InName = InDir + '/' + qid + '/%d'%(i + 1)
            mtx = np.loadtxt(InName, delimiter=',')
            if len(mtx.shape) == 1:
                mtx = np.array([mtx])
                
            GraphData.NodeMtx = mtx
            GraphData.EdgeTensor = np.ones([1,1,1])
            GraphData.hNodeId = {'q_%s'%(qid):1}
            GraphData.rel = lRelScore[i]
            GraphData.SetDims()
            
            lGraphData.append(GraphData)
        
        return lGraphData
    
    @classmethod
    def FeatureMinMaxNormalization(cls,llGraphData):
        if type(llGraphData[0]) != list:
            llGraphData = [llGraphData]
            #make sure it is a two dimensional list (ugly)
        
        logging.info('max-min normalization on given graph data')    
        NodeMax = np.array(llGraphData[0][0].NodeMtx)
        NodeMin = np.array(NodeMax)
        EdgeMax = np.array(llGraphData[0][0].EdgeTensor)
        EdgeMin = np.array(EdgeMax)
        
        for lGraphData in llGraphData:
            for GraphData in lGraphData:
                NodeMax = np.maximum(NodeMax,GraphData.NodeMtx)
                NodeMin = np.minimum(NodeMin,GraphData.NodeMtx)
                EdgeMax = np.maximum(EdgeMax,GraphData.EdgeTensor)
                EdgeMin = np.minimum(EdgeMin,GraphData.EdgeTensor)
        
        NodeMax = np.max(NodeMax,0)
        NodeMin = np.min(NodeMin,0)
        EdgeMax = np.max(EdgeMax,0)
        EdgeMin = np.min(EdgeMin,0)
                
        lNodeZeroP = [i for i in range(NodeMax.shape[0]) if NodeMax[i] == NodeMin[i]]
        lNodeElseP = list(set(range(NodeMax.shape[0])) - set(lNodeZeroP) )
        
        lEdgeZeroP = [i for i in range(EdgeMax.shape[0]) if EdgeMax[i] == EdgeMin[i]]
        lEdgeElseP = list(set(range(EdgeMax.shape[0])) - set(lEdgeZeroP) )
        
        logging.info('max-min value found')
        
        
        for i in range(len(llGraphData)):
            for j in range(llGraphData[i]):
                NodeMtx = llGraphData[i][j].NodeMtx
                EdgeTensor = llGraphData[i][j].EdgeTensor
                
                NodeMtx[:,lNodeZeroP] = 0
                NodeMtx[:,lNodeElseP] = (NodeMtx[:,lNodeElseP] - NodeMin[lNodeElseP]) / \
                        (NodeMax[lNodeElseP] - NodeMin[lNodeElseP])
                
                EdgeTensor[:,:,lEdgeZeroP] = 0
                EdgeTensor[:,:,lEdgeElseP] = (EdgeTensor[:,:,lEdgeZeroP] - EdgeMin[lEdgeElseP]) / \
                        (EdgeMax[lEdgeElseP] - EdgeMin[lEdgeElseP])
                        
                
                llGraphData[i][j].NodeMtx = NodeMtx
                llGraphData[i][j].EdgeTensor = EdgeTensor
        
        logging.info('max-min normlization finished')        
        return llGraphData
                
        
        
        
                
        
        
        
        
        
        
        
            
