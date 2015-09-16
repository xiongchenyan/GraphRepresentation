'''
Created on Sep 16, 2015 11:36:01 AM
@author: cx

what I do:
    I fetch target lines in MSRA's LDA data
what's my input:
    target dir + prefix
    zhuyun's doc no-> url mapping data prefix
    number of partition [0,48)
what's my output:
    a dir with files corresponding to each parts in given data
    but filtered based on defined rules


'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.WalkDirectory import WalkDir
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import subprocess

class MSRATargetLinesParalledlFetcherC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.MSRAInDataPre = "/bos/data1/ClueWeb09-TopicModels/tokenize/split_48/part-"
        self.PartNum = 48
        self.DocUrlMappingDataPre = "/bos/tmp11/zhuyund/TopicModels/TopicModelURLDocNo/output_doc_text/url2extid_doc_text/url2extid.block."
        self.OutPre = ""
        
        self.ProcessScript = 'MSRALDAKeepWikiInFile.py'
        self.lCmd = ['qsub','python']


    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.MSRAInDataPre = self.conf.GetConf('indatapre', self.MSRAInDataPre)
        self.PartNum = self.conf.GetConf('partnum', self.PartNum)
        self.DocUrlMappingDataPre = self.conf.GetConf('docurlmappingpre', self.DocUrlMappingDataPre)
        self.OutPre = self.conf.GetConf('outpre', self.OutPre)
        self.ProcessScript = self.conf.GetConf('torunscript', self.ProcessScript)
        self.lCmd.append(self.ProcessScript)
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'indatapre\npartnum\ndocurlmappingpre\noutpre\ntorunscript'
        
    def Process(self):
        for i in range(self.PartNum):
            InName = self.MSRAInDataPre + '%d' %(i)
            OutName = self.OutPre + '%d' %(i)
            MappingName = self.DocUrlMappingDataPre + '%d' %(i)
            lCmd = self.lCmd + [InName,MappingName,OutName]
            print subprocess.check_output(lCmd)
        print 'all submitted'
        
        
        
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print 'I mul process MSRA LDA data'
        MSRATargetLinesParalledlFetcherC.ShowConf()
        sys.exit()
        
    Processor = MSRATargetLinesParalledlFetcherC(sys.argv[1])
    Processor.Process()
        
        
        
        
        
        
        
        

