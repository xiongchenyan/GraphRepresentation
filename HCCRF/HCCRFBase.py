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

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import pickle,logging,json
import numpy as np
from scipy.special import expit
import ntpath
import os
from HCCRF.DocGraph import DocGraphC  

class HCCRFBaseC(object):
    
    @classmethod
    def LoadGraphData(cls,InName,EvidenceGroup = 'hccrf'):
        '''
        load the data of a graph
        #default the file name is doc no
        '''
        GraphData = DocGraphC()
        GraphData.load(InName)
        GraphData.PickEvidenceGroup(EvidenceGroup,InName)
        
        return GraphData
    
    @classmethod
    def ReadTargetGraphData(cls,QueryInName,DataDir,EvidenceGroup = 'hccrf'):
        lQid = [line.split('\t')[0] for line in open(QueryInName).read().splitlines()]
        
        llGraphData = []
        
        for qid in lQid:
            QDir = DataDir + '/' + qid + '/'
            for dirname,dirnames,lDocName in os.walk(QDir):
                lInName = [dirname + '/' + DocName for DocName in lDocName]
                llGraphData.append([HCCRFBaseC.LoadGraphData(InName,EvidenceGroup) for InName in lInName])
                logging.info('read [%d] graph for q [%s]',len(llGraphData[-1]),qid)
                
        return llGraphData
    
    
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
#         logging.debug('B shape %s, VS: %d',json.dumps(B.shape),GraphData.NodeN)
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
        
#         logging.debug('info in JointMu')
#         logging.debug('OmegaInv:\n %s',np.array2string(OmegaInv))
#         logging.debug('A: %s', np.array2string(A))
#         logging.debug('NodeMtx:\n %s', np.array2string(GraphData.NodeMtx))
        Mu = OmegaInv.dot(A)
        return Mu
    
    @classmethod
    def JointSigma(cls,w2,GraphData,OmegaInv = None):
        if OmegaInv == None:
            OmegaInv = np.linalg.inv(cls.EdgeOmega(w2, GraphData))
            
        return OmegaInv
            
    
    
     
        
        
        
        
        