'''
Created on Jul 28, 2015 11:11:19 AM
@author: cx

what I do:
    I pipeline train test and evaluation HCCRF
what's my input:
    Train query file name, test query file name, data dir (can be default), out name 

what's my output:
    the evaluation result

'''


import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

import logging
from cxBase.Conf import cxConfC
# from HCCRFBase import HCCRFBaseC
from HCCRFLearn import HCCRFLearnerC
from HCCRFPredict import HCCRFPredictorC

from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
class HCCRFPipeTrainTestEvaC(object):
    
    def __init__(self):
        self.Init()
        
        
    def Init(self):
        self.Evaluator = AdhocEvaC()
        self.Evaluator.Prepare()
        self.DataDir = '/bos/usr0/cx/tmp/GraphRepresentation/GraphFeature/CW09GraphFeatures/Feature/'
        
        self.Learner = HCCRFLearnerC()
        self.Predictor = HCCRFPredictorC()
        
    
    def ParseParaStr(self,ParaStr):
        lPara = ParaStr.split(';')
        lParaScore = [Para.split('=') for Para in lPara]
        hPara = dict(lParaScore)
        conf = cxConfC()
        conf.hConf = hPara
        return conf
        
        
        
    def Process(self,TrainQueryIn,TestQueryIn,ParaStr, EvaOutName):
        logging.info('training using [%s] testing using [%s] eva out to [%s]',TrainQueryIn,TestQueryIn,EvaOutName)
        
        
        conf = self.ParseParaStr(ParaStr)
        
        EvidenceGroup = conf.GetConf('evidencegroup', 'hccrf') 
        
        logging.info('pipe start training')
        
        
        w1,w2 = self.Learner.PipeTrain(TrainQueryIn, self.DataDir,EvidenceGroup)
        
        logging.info('pipe start testing')
        
        lQid,llDocScore = self.Predictor.PipePredict(TestQueryIn, self.DataDir, w1, w2,EvidenceGroup)
        
        
        logging.info('pipe start evaluating')
        
        lEvaRes = []
        
        for qid,lDocScore in zip(lQid,llDocScore):
            lDocScore.sort(key=lambda item:item[1],reverse = True)
            lDocNo = [item[0] for item in lDocScore]
            EvaRes = self.Evaluator.EvaluatePerQ(qid, "", lDocNo)
            lEvaRes.append(EvaRes)
            
        MeanEvaRes = AdhocMeasureC.AdhocMeasureMean(lEvaRes)
        lEvaRes.append(MeanEvaRes)
        lQid.append('mean')
        
        out = open(EvaOutName,'w')
        for qid,EvaRes in zip(lQid,lEvaRes):
            print >>out, qid + '\t' + EvaRes.dumps()
            
        out.close()
        logging.info('finished, eva res [%s]',lEvaRes[-1].dumps())
        return True
    
    

if __name__ == '__main__':
    import sys
    import sys
    if 5 != len(sys.argv):
        print "4 para: train q, test q , para str, out"
        print 'parastr: EvidenceGroup:letor|esdrank|hccrf'
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)       

        
    Processor = HCCRFPipeTrainTestEvaC()
    Processor.Process(sys.argv[1],sys.argv[2],sys.argv[3], sys.argv[4])    
            
        
        
        
        
     
    
    
    
        