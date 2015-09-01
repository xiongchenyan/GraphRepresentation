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
        self.hNodeId = {}   #obj id -> hash value (p) as in the node weights and edge weight mtx
        self.vNodeWeight = None
        self.mEdgeMatrix = None
        
    def dump(self,OutName):
        out = open(OutName,'w')
        pickle.dump([self.NodeId,self.vNodeWeight,self.mEdgeMatrix],out)
        
    def load(self,InName):
        self.NodeId,self.vNodeWeight,self.mEdgeMatrix = pickle.load(open(InName))
        
        
    
    def ObjWeight(self,ObjId):
        score = 0
        if ObjId in self.hNodeId:
            score = self.vNodeWeight[self.hNodeId[ObjId]]
        return score
    
    
    @staticmethod
    def BoeCos(DkgA,DkgB):
        return 1 - scipy.spatial.distance.cosine(DkgA.vNodeWeight, DkgB.vNodeWeight)
    
    
    def CalcPageRank(self):
        '''
        TBD:
            perform page rank on doc's graph
            with restart probability as node weight
        return a vector of node weights
        '''
        
        raise NotImplementedError
    
    
    
    
