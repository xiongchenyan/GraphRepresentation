'''
I weight lm via ctf, and text cosine
'''



import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')
from cxBase.Conf import cxConfC
from BoeLmBase import BoeLmC
from IndriRelate.CtfLoader import TermCtfC
from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
import logging
from cxBase.WalkDirectory import WalkDir
from IndriRelate.LmBase import LmBaseC
import numpy as np

class BoeLmWeighterC(BoeLmC):
    
    def __init__(self,ConfIn = ""):
        BoeLmC.Init(self)
        if "" != ConfIn:
            self.SetConf(ConfIn)
    
    def Init(self):
        BoeLmC.Init(self)
        self.DocTextDir = ""
        self.ObjCenter = FbObjCacheCenterC()
        self.CtfCenter = TermCtfC()
        self.lInferenceWeight = [1,0,0]
        self.hDocText = {}
        
        
        
    def SetConf(self,ConfIn):
        conf = cxConfC(ConfIn)
        
        self.DocTextDir = conf.GetConf('doctextdir')
        self.LoadDocText()
        
        self.ObjCenter.SetConf(ConfIn)
        
        CtfInName = conf.GetConf('objctf')
        self.CtfCenter.Load(CtfInName)
        
    @classmethod
    def ShowConf():
        print 'doctextdir\nobjctf'
        FbObjCacheCenterC.ShowConf()
        
    def LoadDocText(self):
        for fname in WalkDir(self.DocTextDir):
            for line in open(fname):
                DocNo,text = line.strip().split('\t')
                self.hDocText[DocNo] = text    
        logging.info('doc text loaded')
        
    def GetAllIdf(self,DocKg):
        lItem = DocKg.hNodeId.items()
        lItem.sort(key=lambda item:item[1])
        lObjId = [item[0] for item in lItem]
        
        
        
        lRes = []
        for ObjId in lObjId:
            idf  = self.CtfCenter.GetLogIdf(ObjId)
            lRes.append(idf)
        return lRes
    
    def GetAllTf(self,DocKg):
        return list(DocKg.vNodeWeight)
    
    def GetAllTextCosine(self,DocKg):
        
        DocText = ""
        if DocKg.DocNo in self.hDocText:
            DocText = self.hDocText[DocKg.DocNo]
        
        lCos = []
        if "" == DocText:
            return [0] * len(DocKg)
        DocLm = LmBaseC(DocText)
        lItem = DocKg.hNodeId.items()
        lItem.sort(key=lambda item:item[1])
        lObjId = [item[0] for item in lItem]
        
        for ObjId in lObjId:
            desp = self.ObjCenter.FetchObjDesp(ObjId)
            lm = LmBaseC(desp)
            lCos.append(LmBaseC.Cosine(lm, DocLm))
            
            
        
        return lCos
    
    
    def LinearWeightTfIdfTextSim(self,ObjId,DocKg,TfScore = 1,IdfScore = 0, TextSimScore = 0):
        
        if not ObjId in DocKg:
            return self.MinLogProb
        
        lTf = np.array(self.GetAllTf(DocKg))
        lIdf = np.array(self.GetAllIdf(DocKg))
        lCos = np.array(self.GetAllTextCosine(DocKg))
        
        W = np.array([TfScore,IdfScore,TextSimScore])
        
        W = W / float(sum(W))
        
        lScore = lTf * W[0] + lIdf * W[1] + lCos * W[2]
        p = DocKg.hNodeId[ObjId]
        
        return lScore[p]
        
    def inference(self, ObjId, DocKg):
        return self.LinearWeightTfIdfTextSim(ObjId, DocKg, self.lInferenceWeight[0], self.lInferenceWeight[1], self.lInferenceWeight[2])
        
        
        

        
        
        
        
