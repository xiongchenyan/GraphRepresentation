'''
Created on Sep 1, 2015 4:25:44 PM
@author: cx

what I do:
    I form doc Kg for given query's search results
what's my input:
    query and serp cache
    resources needed by DocKGUnsupervisedFormer
    

what's my output:
    a directory
        /qid/DocNo
            each file is the dump of DocKg
'''

import site
import logging

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC

import os
from DocKGUnsupervisedFormer import DocKGTagMeFormerC,DocKGFaccFormerC,DocKGUnsupervisedFormerC
from DocGraphRepresentation.DocKnowledgeGraph import DocKnowledgeGraphC

from DocGraphRepresentation.DocGraphConstructor import DocGraphConstructorC

class SearchResDocGraphConstructorC(DocGraphConstructorC):
    
    def Init(self):
        DocGraphConstructorC.Init(self)
        self.Searcher = IndriSearchCenterC()
        
        self.OutDir = ""
        
        
    def SetConf(self, ConfIn):
        DocGraphConstructorC.SetConf(self, ConfIn)
        self.Searcher.SetConf(ConfIn)
        self.OutDir = self.conf.GetConf('outdir')
        
    @staticmethod
    def ShowConf():
        DocGraphConstructorC.ShowConf()
        IndriSearchCenterC.ShowConf()    
        print 'outdir'
        
    def FormForOneQ(self,qid,query):
        lDoc = self.Searcher.RunQuery(query, qid)
        
        lDocKg = [self.GraphFormer.FillDocGraph(doc.DocNo) for doc in lDoc]
        
        QueryOutDir = self.OutDir + '/' + qid
        if not os.path.exists(QueryOutDir):
            os.makedirs(QueryOutDir)
            
        for DocKg in lDocKg:
            DocKg.dump(QueryOutDir + '/' + DocKg.DocNo)
            logging.debug('[%s] dummped [%d] node',DocKg.DocNo,len(DocKg))
            
        logging.info('[%s-%s] doc kg formed',qid,query)
        return True
    
    
    def Process(self,QInName):
        lQidQuery = [line.split('\t') for line in open(QInName).read().splitlines()]
        
        for qid,query in lQidQuery:
            self.FormForOneQ(qid, query)
            
        logging.info('[%s] query finished',QInName)
        return True
    
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print 'I construct query search result doc kg'
        SearchResDocGraphConstructorC.ShowConf()
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)          
    
    Processor = SearchResDocGraphConstructorC(sys.argv[1])
    
    conf = cxConfC(sys.argv[1])
    QInName = conf.GetConf('in', '/bos/usr0/cx/tmp/data/WebTrackQ09')
    Processor.Process(QInName)
    
    
        
        
        
    
