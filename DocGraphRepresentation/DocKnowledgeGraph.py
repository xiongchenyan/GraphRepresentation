'''
Created on my MAC Aug 31, 2015-9:47:57 PM
What I do:

What's my input:
    I am the base data structure of doc knowledge graph
What's my output:

@author: chenyanxiong
'''

import numpy as np
import pickle,logging,json
import scipy

class DocKnowledgeGraphC(object):
    
    def __init__(self):
        self.Init()
        
        
    def Init(self):
        self.DocNo = ""
        self.hNodeId = {}   #obj id -> hash value (p) as in the node weights and edge weight mtx
        self.vNodeWeight = np.zeros(0)
        self.mEdgeMatrix = np.zeros([0,0])
        
    def dump(self,OutName):
        out = open(OutName,'w')
        pickle.dump([self.DocNo,self.hNodeId,self.vNodeWeight,self.mEdgeMatrix],out)
        
    def load(self,InName):
        self.DocNo,self.hNodeId,self.vNodeWeight,self.mEdgeMatrix = pickle.load(open(InName))
        
        
    def NormalizeEdgeMtx(self):
        logging.debug('edge mtx:\n %s',np.array2string(self.mEdgeMatrix))
        row_sums = self.mEdgeMatrix.sum(axis=1,keepdims=True)
        if 0 != row_sums:
            self.mEdgeMatrix /= row_sums
        else:
            logging.warn('some node has no indegree')
#     def ObjWeight(self,ObjId):
#         score = 0
#         if ObjId in self.hNodeId:
#             score = self.vNodeWeight[self.hNodeId[ObjId]]
#         return score
    
    
    @staticmethod
    def BoeCos(DkgA,DkgB):
        NormA = DkgA.Norm()
        NormB = DkgB.Norm()
        if 0 == (NormA * NormB):
            return 0
        return DkgA.dot(DkgB) / DkgA.Norm() * DkgB.Norm()
    
    def Norm(self):
        return np.linalg.norm(self.vNodeWeight)
    
    def dot(self,DocKgB):
        score = 0
        for node in self.hNodeId:
            if node in DocKgB:
                score += self[node] * DocKgB[node]
        return score
    
    
    def CalcPageRank(self):
        '''
        TBD:
            perform page rank on doc's graph
            with restart probability as node weight
        return a vector of node weights
        '''
        
        raise NotImplementedError
    
    def __contains__(self,key):
        return key in self.hNodeId
    
    def __getitem__(self,key):
        if not key in self.hNodeId:
            raise KeyError
        return self.vNodeWeight[self.hNodeId[key]]
    
    
    
    
    def __len__(self):
        return len(self.hNodeId)