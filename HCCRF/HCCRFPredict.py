'''
Created on Jul 24, 2015 11:48:09 AM
@author: cx

what I do:
    I am the predictor of HCCRF
what's my input:
    lGraphData,w1,w2
what's my output:
    lScore
'''

from HCCRFBase import HCCRFBaseC

class HCCRFPredictorC(object):
    
    @classmethod
    def Predict(cls,GraphData,w1,w2):
        return HCCRFBaseC.JointMu(w1, w2, GraphData)[0]
        
