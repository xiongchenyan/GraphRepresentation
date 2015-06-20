'''
Created on my MAC Jun 20, 2015-8:09:52 PM
What I do:
    I prepare all useful data for graph ranking
        (TBD: define output format)
include:
    fetch qrel data save as vector


    transfer the raw graph to tensor
    read the input, and transfer to tensor, (numpy 3-D array).
    
    read twice,
        first time get the node id and feature id mapping
        second time make the tensor, and normalize
        
IMPORTANT: there should be no missing feature for any input line
    
What's my input:
    EdgeFeatureExtractor's output:
        node node hFeature
        (first node in the line is query)
What's my output:
    numpy array, one file for one query

@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

import numpy as np
import pickle,json
import logging
from cxBase.WalkDirectory import WalkDir


def UpdateHashId(name,hDict):
    if not name in hDict:
        hDict[name] = len(hDict)
        

def GenerateHashMapping(InName):
    hNodeId = {}
    lEdgeFeatureName = []
    for line in open(InName):
        NodeA,NodeB,FeatureStr = line.strip().split('\t')
        UpdateHashId(NodeA, hNodeId)
        UpdateHashId(NodeB, hNodeId)
        
        hFeature = json.loads(FeatureStr)
        lEdgeFeatureName.extend(hFeature.keys())
        
        
    lEdgeFeatureName = list(set(lEdgeFeatureName))
    lEdgeFeatureName.sort()  #make sure feature id is uniq
    hEdgeFeatureId = dict(zip(lEdgeFeatureName,range(len(lEdgeFeatureName))))
        
    logging.info('[%s] id made [%d] node [%d] edge feature',InName,len(hNodeId),len(hEdgeFeatureId))
    return hNodeId,hEdgeFeatureId


def FormGraphTensorPerFile(InName,hNodeId,hEdgeFeatureId):
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
    
    
        
        
    





