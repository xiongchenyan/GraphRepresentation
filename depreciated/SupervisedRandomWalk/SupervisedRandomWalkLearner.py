'''
Created on my MAC Jun 22, 2015-5:33:12 PM
What I do:
    I train supervised random walk (pairwise loss for now)
What's my input:
    graph and label
    and hyper parameters:
        lambda: loss weight (model complexity)
        alpha: re-start probability
        b: fraction in WMV loss
        
        
What's my output:
    trained parameter
@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')
from scipy.optimize import minimize
import numpy as np

from SupervisedRandomWalk.GraphDataPreparation import GraphDataPreparationcC

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC


class SupervisedRandomWalkLearner(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        
#         self.lGraphData = []
#         self.lLabel = []
        
        '''
        hyperparameters
        '''
        self.Lambda = 1
        self.Alpha = 0.2
        self.b = 0.4
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.Lambda = self.conf.GetConf('lambda', self.Lambda)
        self.Alpha = self.conf.GetConf('alpha', self.Alpha)
        self.b = self.conf.GetConf('b', self.b)
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'lambda\nalpha\nb'
        
        
    def Sigmod(self,x):
        return 1.0 / (1 + np.exp(-x / self.b))

    
    def FeatureToEdgeStrength(self,GraphTensor,w):
        EdgeMtx = np.zeros(GraphTensor.shape[:2])
        
        for i in range(EdgeMtx.shape[0]):
            EdgeMtx[i,:] = self.Sigmod(GraphTensor[i,:,:].dot(w).T)   #
            
        return EdgeMtx
    
    
    def EdgeMtxToTransProbMtx(self,EdgeMtx):
        n = EdgeMtx.shape[0]
        TransMtx = EdgeMtx / (EdgeMtx.dot(np.ones(n,1)).dot(np.ones(1,n)))
        TransMtx = (1-self.Alpha) * TransMtx + 
    
    





