'''
Created on Sep 2, 2015 5:50:46 PM
@author: cx

what I do:
    I provide sim function for doc-doc pair

what's my input:
    tagged doc results
what's my output:
    function para: ([doc no, text],[doc no,text])
        return sim score

'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from DocGraphRepresentation.DocKnowledgeGraph import DocKnowledgeGraphC
import numpy as np
import logging
from DocGraphRepresentation.ConstructSearchResDocGraph import SearchResDocGraphConstructorC


class BoeLmSimmerC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.DocKgDir = ""
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DocKgDir = self.conf.GetConf('dockgdir')
        
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'dockgdir'
        
    
    def DocPairSim(self,DocA,DocB):
        '''
        just use cosine similarity of their boe model
        '''
        DocKgA = SearchResDocGraphConstructorC.LoadDocGraph(self.DocKgDir, "LP50", DocA[0])
        DocKgB = SearchResDocGraphConstructorC.LoadDocGraph(self.DocKgDir, "LP50", DocB[0])
        score = DocKnowledgeGraphC.BoeCos(DocKgA, DocKgB)
        return score
    
    
    
    

if __name__=='__main__':
    import sys,os
    from AdhocEva.RankerEvaluator import RankerEvaluatorC
    from DocSimilarity.DocSimEvaluate import DocSimEvaluatorC
    if 2 != len(sys.argv):
        print 'I evaluate Boe sim '
        print 'in\nout'
        BoeLmSimmerC.ShowConf()
        DocSimEvaluatorC.ShowConf()
        sys.exit()
    
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    ch.setFormatter(formatter)
    
    
    
    conf = cxConfC(sys.argv[1])   
    QIn = conf.GetConf('in')
    EvaOut = conf.GetConf('out')
    
    Simmer = BoeLmSimmerC(sys.argv[1])
    Evaluator = DocSimEvaluatorC(sys.argv[1])
    score = Evaluator.EvaluateSimFunc(Simmer.DocPairSim)
    
    print >> EvaOut,score
    EvaOut.close()
        
        
        
        
        
            
            
        
        





