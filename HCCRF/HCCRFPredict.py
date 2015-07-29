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
from HCCRFLearn import HCCRFLearnerC


class HCCRFPredictorC(object):
    
    @classmethod
    def Predict(cls,GraphData,w1,w2):
        score = HCCRFBaseC.JointMu(w1, w2, GraphData)[0]
        return GraphData.DocNo,score
    
    def PipePredict(self,QueryInName,DataDir,w1,w2):
        
        llGraphData = HCCRFLearnerC.ReadTargetGraphData(QueryInName, DataDir)
        llDocScore = [[self.Predict(GraphData, w1, w2) for GraphData in lGraphData] \
                       for lGraphData in llGraphData]
        
        lQid = [line.split('\t')[0] for line in open(QueryInName).read().splitlines()]
        return lQid,llDocScore
        
