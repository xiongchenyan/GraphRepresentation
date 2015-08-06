'''
Created on Aug 5, 2015 2:38:10 PM
@author: cx

what I do:
    I train HCCRF using ListMLE loss
what's my input:
    I use the same input/output with HCCRFTrainC
what's my output:


'''



import site

site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

import numpy as np
from HCCRFBase import HCCRFBaseC
from HCCRFLearn import HCCRFLearnerC
from HCCRFPredict import HCCRFPredictorC
from ListMLE.ListMLEModel import ListMLEModelC
import logging,json

class HCCRFListMLETrainC(HCCRFLearnerC):
    
    @classmethod
    def Loss(cls, theta, llGraphData):
        l = ListMLEModelC.Loss(theta, llGraphData, cls.RankingScore)
        
        logging.info('listmle loss [%f]',l)
        
        return l
        
        
        


    @classmethod
    def RankingScore(cls,theta,GraphData):
        w1 = theta[:GraphData.NodeFeatureDim]
        w2 = theta[-GraphData.EdgeFeatureDim:]
        
        DocNo,score = HCCRFPredictorC.Predict(GraphData, w1, w2)
        
        return score


    @classmethod
    def Gradient(cls, theta, llGraphData):
        gf = ListMLEModelC.Gradient(theta, llGraphData, cls.RankingScore, cls.RankingScoreGradient)
        
        w1 = theta[:llGraphData[0][0].NodeFeatureDim]
        w2 = theta[-llGraphData[0][0].EdgeFeatureDim:]
        logging.debug('w1:\n %s',np.array2string(w1))
        logging.debug('w2:\n %s',np.array2string(w2))
        logging.debug('gf %s: %s',json.dumps(gf.shape),np.array_str(gf))
        return gf
        
    
    @classmethod
    def RankingScoreGradient(cls,theta,GraphData):
        w1 = theta[:GraphData.NodeFeatureDim]
        w2 = theta[-GraphData.EdgeFeatureDim:]
        
        Omega = HCCRFBaseC.EdgeOmega(w2,GraphData)
        OmegaInv = np.linalg.inv(Omega)
        A = HCCRFBaseC.NodeA(w1, GraphData)
        
        gfw1 = cls.MuPartialW1(GraphData, A, OmegaInv)
        gfw2 = cls.MuPartialW2(GraphData, A, OmegaInv, w2)
        
        gf = np.array(list(gfw1) + list(gfw2))
        return gf
    
    
    
    
    
        
        
        
        
        