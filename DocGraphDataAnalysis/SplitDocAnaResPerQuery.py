'''
Created on Sep 8, 2015 7:34:39 PM
@author: cx

what I do:
    i split the tagged doc results as SERP per query
what's my input:
    query
    doc ana
    search res
what's my output:
    a file per query, contains its doc ana, orderred by doc's rank

'''

import site
import logging

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC



class DocAnaResSERPSplitterC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.Searcher = IndriSearchCenterC()
        self.hDocAnaData = {}
        self.hDocText = {}
        self.OutDir = ''
        self.QInName = ""
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.Searcher.SetConf(ConfIn)
        DocAnaIn = self.conf.GetConf('docanain')
        DocTextIn = self.conf.GetConf('doctextin')
        self.ReadDocAna(DocAnaIn,DocTextIn)
        self.OutDir = self.conf.GetConf('outdir')
        self.QInName = self.conf.GetConf('in')
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'docanain\noutdir\nin\ndoctextin'
        IndriSearchCenterC.ShowConf()

    def ReadDocAna(self,DocAnaIn,DocTextIn):
        lLines = open(DocAnaIn).read().splitlines()
        lDict = [[line.split()[0],line] for line in lLines]
        self.hDocAnaData = dict(lDict)
        
        lLines = open(DocTextIn).read().splitlines()
        
        lDict = [line.split('#')[0].split('\t') for line in lLines]
        self.hDocText = dict(lDict)
        return True
    
    
    def DumpOneQ(self,qid,query):
        lDoc = self.Searcher.RunQuery(query, qid)
        out = open(self.OutDir + '/%s' %(query.replace(' ','_')),'w')
        
        for doc in lDoc:
            if (not doc.DocNo in self.hDocAnaData) | (not doc.DocNo in self.hDocText):
                continue
            line = self.hDocAnaData[doc.DocNo]
            
            vCol = line.split('\t')
            text = self.hDocText[doc.DocNo]
            print >>out, vCol[0] + '\t' + text
            
            if len(vCol) > 2:
                vAna = vCol[1:]
                for i in range(len(vAna)/8):
                    print >>out, '\t'.join(vAna[8*i:8*i + 8])
            
        out.close()
        logging.info('[%s] data dumped',query)
        return True
    
    def Process(self):
        
        lQidQuery = [line.split('\t') for line in open(self.QInName).read().splitlines()]
        
        for qid,query in lQidQuery:
            self.DumpOneQ(qid, query)
            
        logging.info('finished')
        
        
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print 'I dump per query doc ana'
        DocAnaResSERPSplitterC.ShowConf()
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)          
    
    Processor = DocAnaResSERPSplitterC(sys.argv[1])
    
    Processor.Process()
        
        
        
                                 
    
        
