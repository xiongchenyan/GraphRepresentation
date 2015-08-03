'''
Created on Jul 24, 2015 11:48:36 AM
@author: cx

what I do:
    The learner of HCCRF
    I only contain the API's of the model
        pipeline run stuff are not included
what's my input:
    the graph data (list of)
what's my output:
    the trained w1, w2
    
    
procedure:
    implement gradients
    implement loss func
    initialize parameter?
    and put all these to scikit learn's



'''




'''
to call scipy.optimize.minimize
API of loss func:
    loss(theta(w1 + w2), lGraphData)
        return loss function value (remind it is mimization)
API of gradient func:
    gradient(theta(w1 + w2), lGraphData)
        return gradients

scipy.optimize.minimize(self.loss,theta,arg=(lGraphData),method='BFGS',jac=self.Gradient)
check: http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize
for more details
'''
'''
July 28 2015
reviewed, seems right, tensor operations are the most worried part.
'''
import itertools
from numpy.linalg.linalg import LinAlgError
import numpy as np
# import scipy
from scipy.optimize import minimize
import logging
from math import log,sqrt,pi
import json
from HCCRFBase import HCCRFBaseC
import os,sys

class HCCRFLearnerC(object):
    

    @classmethod    
    def Loss(cls,theta,lGraphData):
        f = np.mean([cls.LossPerGraph(theta, GraphData) for GraphData in lGraphData])
        f = float(f)
        logging.info('loss [%f]',f)
        return f
    @classmethod  
    def Gradient(cls,theta,lGraphData):
#         logging.info('calling gradients func')
        gf = np.mean([cls.GradientPerGraph(theta, GraphData) for GraphData in lGraphData],0)
#         logging.info('gradient: %s',np.array_str(gf))
        return gf
    
    
    @classmethod  
    def LossPerGraph(cls,theta,GraphData):
        
        
        w1 = theta[:GraphData.NodeFeatureDim]
        w2 = theta[-GraphData.EdgeFeatureDim:]
        
        A = HCCRFBaseC.NodeA(w1, GraphData)
        Omega = HCCRFBaseC.EdgeOmega(w2,GraphData)
        OmegaInv = np.linalg.inv(Omega)
        
        mu = HCCRFBaseC.JointMu(w1, w2, GraphData,A,OmegaInv)[0]
        sigma = OmegaInv[0,0]
        y = GraphData.rel
        
#         if True:
#             logging.debug('w1: %s',json.dumps(w1.tolist()))
#             logging.debug('w2: %s', json.dumps(w2.tolist()))
#             logging.debug('Omega: %s',json.dumps(Omega.tolist()))
        logging.debug('Omega symmetric %d',int(np.allclose(Omega.T,Omega)))
        #pd metrix?
        try:
            lCskRes = np.linalg.cholesky(Omega)
        except LinAlgError:
            logging.error('Omega is not postive definite')
            '''
            this is impossible, there must be something wrong with D or B
#             show D and B
            '''
#             B = HCCRFBaseC.EdgeB(w2, GraphData)
#             D = HCCRFBaseC.EdgeD(w2, GraphData, B)
            
#             print "D:"
#             print np.array_str(D)
#             print "B:"
#             print np.array_str(B)
#             print B
            sys.exit()
            

        
#             logging.debug('Sigma matrix: %s',json.dumps(OmegaInv.tolist()))
        logging.debug('Sigma symmetric %d',int(np.allclose(OmegaInv.T,OmegaInv)))
        logging.debug('y [%f] Mu [%f] Sigma [%f]',y,mu,sigma)
        l = - (1.0/(2.0 * (sigma**2))) * ((y - mu)**2) - log(sigma)
        
        return -l
    
    
    @classmethod
    def GradientPerGraph(cls,theta,GraphData):
        w1 = theta[:GraphData.NodeFeatureDim]
        w2 = theta[-GraphData.EdgeFeatureDim:]
        
        
        A = HCCRFBaseC.NodeA(w1, GraphData)
        OmegaInv = np.linalg.inv(HCCRFBaseC.EdgeOmega(w2,GraphData))
        mu = HCCRFBaseC.JointMu(w1, w2, GraphData,A,OmegaInv)[0]
        sigma = OmegaInv[0,0]
        y = GraphData.rel
        
        MuPW1 = cls.MuPartialW1(GraphData,A,OmegaInv)
        MuPW2 = cls.MuPartialW2(GraphData,A,OmegaInv,w2)
        SigmaPW2 = cls.SigmaPartialW2(GraphData,A,OmegaInv,w2)
        
#         logging.debug('Shape:MuPW1: %s, MuPW2: %s, SigmaPW2: %s',json.dumps(MuPW1.shape),json.dumps(MuPW2.shape),json.dumps(SigmaPW2.shape))
        
        gW1 = -(1.0/(sigma**2)) * (y-mu) * MuPW1
        gW2 = -(1/(sigma**3)) * ((y-mu)**2) * SigmaPW2 \
              -(1/(sigma**2)) * (y-mu) * MuPW2 \
              +(1/sigma) * SigmaPW2
        
        
#         logging.debug('w2 shape %s, gw2 shape %s',json.dumps(w2.shape),json.dumps(gW2.shape))
#         sys.exit()
        gW1 = gW1.reshape(w1.shape)  #reshape from column mtx to vector
        gW2 = gW2.reshape(w2.shape)  #same
        
        gf = np.array(list(gW1) + list(gW2))
        
        logging.debug('gf %s: %s',json.dumps(gf.shape),np.array_str(gf))
        return gf
    
    
    '''
    TBD: make sure the tensor/matrix operation's dimension alignments are correct...
    first level derivative operations
    '''
    @classmethod
    def MuPartialW1(cls,GraphData,A,OmegaInv):
        
        res = (OmegaInv[0,:].dot(cls.APartialW1(GraphData))).T  #careful
        res.reshape(GraphData.NodeFeatureDim)
        return res
    
    @classmethod
    def MuPartialW2(cls, GraphData,A,OmegaInv,w2):
        OmegaInvPartial = cls.OmegaInvPartialW2(GraphData,OmegaInv,w2)
        
        TargetOmegaInvPartial = OmegaInvPartial[0,:,:]  #careful tensor slice, should be a n\times |w1| mtx
        
#         logging.debug('Target Omega Inv partial dim [%d*%d] should be [%d*%d]'  \
#                       ,TargetOmegaInvPartial.shape[0],TargetOmegaInvPartial.shape[1],\
#                       GraphData.NodeN,GraphData.EdgeFeatureDim)
        
        res = TargetOmegaInvPartial.T.dot(A)   #careful
        
        res.reshape(w2.shape) 
        return res
    
    @classmethod
    def SigmaPartialW2(cls,GraphData,A,OmegaInv,w2):
        
        OmegaInvPartial = cls.OmegaInvPartialW2(GraphData,OmegaInv,w2)  #n*n*|w2| tensor
        res = OmegaInvPartial[0,0,:]  #|w2| vector corresponding to first dim
        res = res.reshape(w2.shape)
        return res
    
    
    '''
    second level derivative operations
    '''
    
    @classmethod
    def APartialW1(cls,GraphData):
        return GraphData.NodeMtx
    
    @classmethod
    def OmegaInvPartialW2(cls,GraphData,OmegaInv,w2):
        '''
        return a n*n*|w2| tensor
        '''
        
        OmegaPartial = cls.OmegaPartialW2(GraphData,w2)
        
        res = np.zeros(GraphData.EdgeTensor.shape)
        
        for i in range(GraphData.EdgeFeatureDim):
            res[:,:,i] = OmegaInv.dot(OmegaPartial[:,:,i]).dot(OmegaInv)
            
        return res
    
    
    @classmethod
    def OmegaPartialW2(cls,GraphData,w2):
        gB = cls.BPartialW2(GraphData, w2)
        
        gD = np.zeros(gB.shape)
        SumMid = np.sum(gB,1) #n * w2 mtx
        for i in range(GraphData.NodeN):
            gD[i,i,:] = SumMid[i,:]
        
        res = gD - gB
        
        
        return res
    
    
    @classmethod
    def BPartialW2(cls,GraphData,w2):
        gB = np.zeros(GraphData.EdgeTensor.shape)
        
        B = HCCRFBaseC.EdgeB(w2, GraphData)
        WMtx = B * B * np.exp(-GraphData.EdgeTensor.dot(w2))
        
        for i in range(GraphData.EdgeFeatureDim):
            gB[:,:,i] = WMtx * GraphData.EdgeTensor[:,:,i]
        
        
        return gB
    
    
    
    def Train(self,lGraphData):
        '''
        call bfgs to train
        '''
        
        '''
        retrain 5 times and pick the best
        '''
        ReTrainRound = 5
        
        LastLoss = np.inf
        BestW1 = None
        BestW2 = None
        
        for i in range(ReTrainRound):
        
            logging.info('start training round [%d]',i)
            InitTheta = np.random.rand(lGraphData[0].NodeFeatureDim + lGraphData[0].EdgeFeatureDim)
    #         gf = self.Gradient(InitTheta, lGraphData)
            
            TrainRes = minimize(self.Loss,InitTheta,\
                                args=(lGraphData), \
                                method='BFGS', \
                                jac=self.Gradient, \
                                options = {'disp':True, 'gtol':1e-03}
                                )
            
            logging.info('training result message: [%s]',TrainRes.message)
            
            w1 = TrainRes.x[:lGraphData[0].NodeFeatureDim]
            w2 = TrainRes.x[-lGraphData[0].EdgeFeatureDim:]
            
            if LastLoss > TrainRes.fun:
                LastLoss = TrainRes.fun
                BestW1 = w1
                BestW2 = w2
                logging.info('better res [%f] find in round [%d]',LastLoss,i)
            
        return BestW1,BestW2
    
    
    '''
    these should be put into the class that runs training process?
    '''
    def PipeTrain(self,QueryInName,DataDir,EvidenceGroup = 'hccrf'):
        '''
        QueryInName contains all training queries
        DataDir contains all data (train test could all be there, will only read those 
            in QueryInName
        '''
        
        llGraphData = HCCRFBaseC.ReadTargetGraphData(QueryInName,DataDir,EvidenceGroup)
        lGraphData = list(itertools.chain(*llGraphData))
        return self.Train(lGraphData)
    

    
    
    
    
                
                
            
        
        
        
        
        
            
        
        
    
        
        
    
    
    
    
        
    
        
        
        
        
        
    
    
    
    
    




