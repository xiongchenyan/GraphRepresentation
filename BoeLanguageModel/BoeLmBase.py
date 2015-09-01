'''
Created on Sep 1, 2015 3:45:48 PM
@author: cx

what I do:
    I am the base class of boe language model
what's my input:
    doc and q'e
    doc's e is scored and stored in DocKgC
    perhaps: obj's idf
what's my output:
    p(q'e| doc)
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from DocGraphRepresentation.DocKnowledgeGraph import DocKnowledgeGraphC
import numpy as np

class BoeLmC(object):
    def __init__(self):
        self.Init()
        
    def Init(self):
        self.MinLogProb = -20
        return
    
    
    def inference(self,ObjId,DocKg):
        '''
        return the log prob if p(ObjId| DocKg)
        '''
        
        score = self.MinLogProb
        if ObjId in DocKg:
            if DocKg[ObjId] != 0:
                score = np.log(DocKg[ObjId])
        return score
            
            
        
        
    

