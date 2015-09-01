'''
Created on my MAC Aug 31, 2015-9:59:01 PM
What I do:
    I form doc's kg in various unsupervised ways
What's my input:
    a root class about API's
    several independent class for each different ways of filling the doc graph
What's my output:
    DocKG
@author: chenyanxiong
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
import numpy as np
import scipy

from DocKnowledgeGraph import DocKnowledgeGraphC


class DocKGUnsupervisedFormerC(cxBaseC):
    
    def FillDocGraph(self,DocNo):
        raise NotImplementedError
    
    
    
    
class DocKGFaccFormerC(DocKGUnsupervisedFormerC):
    '''
    I fill doc's kg using FACC1 annotation
        node score = \sum_mention confidence score
    '''
    
    def Init(self):
        DocKGUnsupervisedFormerC.Init(self)
        self.FaccInDir = ""
        self.hFaccData = {}   # preloaded from QueryFaccDir I would say for now.
        
        
        
        
    def SetConf(self, ConfIn):
        DocKGUnsupervisedFormerC.SetConf(self, ConfIn)
        '''
        TBD
        '''
        
    def FillDocGraph(self, DocNo):
        '''
        TBD
        '''
        return
    
    
    
class DocKGTagMeFormerC(DocKGUnsupervisedFormerC):
    '''
    I fill doc's kg using TagMe annotation
        node score = \sum_mention confidence score
    '''
    def Init(self):
        DocKGUnsupervisedFormerC.Init(self)
        self.TagMeResIn = ""
        self.hTagMeData = {}  #preloaded from TagMe ana results (aligned to Freebase already and doc content discarded)
        
        
    def SetConf(self, ConfIn):
        DocKGUnsupervisedFormerC.SetConf(self, ConfIn)
        '''
        TBD
        '''
        return
    
    def FillDocGraph(self, DocNo):
        '''
        TBD
        '''
        return
        
    
    
    
    
    
        
