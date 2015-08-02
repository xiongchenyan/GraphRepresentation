'''
Created on Jul 24, 2015 11:47:35 AM
@author: cx

what I do:
    I am the base function of HCCRF
what's my input:
     I provide basic functions of HCCRF
what's my output:


'''

'''
July 28 2015
reviewed, seems all right
'''

import pickle,logging,json
import numpy as np
from scipy.special import expit
import ntpath

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
        
        

class HCCRFBaseC(object):
    
    @classmethod
    def LoadGraphData(cls,InName):
        '''
        load the data of a graph
        #default the file name is doc no
        '''
        GraphData = DocGraphC()
        [GraphData.NodeMtx,GraphData.EdgeTensor,GraphData.rel,GraphData.hNodeId] = pickle.load(open(InName))
        GraphData.SetDims()
        GraphData.DocNo = ntpath.basename(InName)
        '''
        checking graphdata,
            if the edge tensor not symmetric, 
                using average (convert directed edge to undirected edge)
        '''
        for i in range(GraphData.EdgeFeatureDim):
            if not np.array_equal(GraphData.EdgeTensor[:,:,i].T,GraphData.EdgeTensor[:,:,i]):
#                 logging.warn('Graph Edge Tensor [%d] dim not symmetric',i)
                GraphData.EdgeTensor[:,:,i] = (GraphData.EdgeTensor[:,:,i] + GraphData.EdgeTensor[:,:,i].T)/ 2.0
#                 Mtx = GraphData.EdgeTensor[:,:,i]
#                 ErrorMtx = [(a,b,Mtx[a,b],Mtx[b,a]) for a in range(Mtx.shape[0]) for b in range(a+1,Mtx.shape[1]) if Mtx[a,b] != Mtx[b,a]]
#                 logging.warn(ErrorMtx)
#                 logging.warn(GraphData.EdgeTensor[:,:,i])
        
        
        return GraphData
    
    
    @classmethod
    def NodeA(cls,w1,GraphData):
        
        A = GraphData.NodeMtx.dot(w1)
        return A
    
    @classmethod
    def EdgeB(cls,w2,GraphData):
#         B = np.zeros([GraphData.NodeN,GraphData.NodeN])
#         for i in range(GraphData.EdgeTensor.shape[0]):
#             B += GraphData.EdgeTensor[i].dot(w2[i])
            
        B = GraphData.EdgeTensor.dot(w2)    
#         logging.debug('B is symmetric %d',int(np.array_equal(B.T, B)))
        B = expit(B)
        
        return B
    @classmethod
    def EdgeD(cls,w2,GraphData,B = None):
        
        if B == None:
            B = cls.EdgeB(w2, GraphData)
        
        D = np.diag(B.dot(np.ones([GraphData.NodeN,1])).reshape(GraphData.NodeN))
        
        return D
    @classmethod
    def EdgeOmega(cls,w2,GraphData):
        B = cls.EdgeB(w2, GraphData)
        D = cls.EdgeD(w2, GraphData, B)
        Omega = np.diag(np.ones([GraphData.NodeN])) + D - B 
        return Omega
    
    @classmethod
    def JointMu(cls,w1,w2,GraphData,A=None,OmegaInv = None):
        if A == None:
            A = cls.NodeA(w1, GraphData)
            OmegaInv = np.linalg.inv(cls.EdgeOmega(w2, GraphData))
        
        Mu = OmegaInv.dot(A)
        return Mu
    
    @classmethod
    def JointSigma(cls,w2,GraphData,OmegaInv = None):
        if OmegaInv == None:
            OmegaInv = np.linalg.inv(cls.EdgeOmega(w2, GraphData))
            
        return OmegaInv
            
    
    
     
        
        
        
        
        