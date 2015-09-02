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

    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'graphsource'
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
    
