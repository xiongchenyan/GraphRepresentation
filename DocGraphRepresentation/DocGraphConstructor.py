'''
Created on Sep 1, 2015 8:52:13 PM
@author: cx

what I do:
    I am the root class to construct doc graph
what's my input:

what's my output:


'''

import site
import logging

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC

import os
from DocKGUnsupervisedFormer import DocKGTagMeFormerC,DocKGFaccFormerC,DocKGUnsupervisedFormerC
from DocGraphRepresentation.DocKnowledgeGraph import DocKnowledgeGraphC


'''
TBD: abstract SearchResDocGraphConstructorC to this root class
implement annotated result doc graph constructor too
be aware of the output dump dir organization
'''

class DocGraphConstructorC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        
        self.GraphFormer = DocKGUnsupervisedFormerC()  #virtual here
        self.GraphSource = 'tagme'
        self.OutDir = ""

    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'graphsource\noutdir'
        DocKGFaccFormerC.ShowConf()
        DocKGTagMeFormerC.ShowConf()
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.GraphSource = self.conf.GetConf('graphsource',self.GraphSource)
        
        if self.GraphSource == 'tagme':
            self.GraphFormer = DocKGTagMeFormerC(ConfIn)
        if self.GraphSource == 'facc':
            self.GraphFormer = DocKGFaccFormerC(ConfIn)
        
        if not self.GraphSource in set(['tagme','facc']):
            logging.error('graph formmer type [%s] not supported',self.GraphSource)
            raise NotImplementedError
        
        
    
    @classmethod
    def LoadDocGraph(cls,InDir,qid,DocNo):
        DocKg = DocKnowledgeGraphC()
        DocKg.load(InDir + '/' + qid + '/' + DocNo)
        return DocKg
    
    
    def Process(self,DocNoInName):
        lDocNo = [line.split()[0] for line in open(DocNoInName).read().splitlines()]
        
        lDocKg = [self.GraphFormer.FillDocGraph(DocNo) for DocNo in lDocNo]
        
        if not os.path.exists(self.OutDir):
            os.makedirs(self.OutDir)
            
        for DocKg in lDocKg:
            DocKg.dump(self.OutDir + '/' + DocKg.DocNo)
            logging.debug('[%s] dummped [%d] node',DocKg.DocNo,len(DocKg))
            
        logging.info('[%s] doc kg formed',DocNoInName)
        return True
    
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print 'I construct given doc no doc kg'
        print 'in'
        DocGraphConstructorC.ShowConf()
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)          
    
    Processor = DocGraphConstructorC(sys.argv[1])
    
    conf = cxConfC(sys.argv[1])
    DocInName = conf.GetConf('in')
    Processor.Process(DocInName)    
