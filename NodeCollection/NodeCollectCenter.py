'''
Created on my MAC Jun 10, 2015-2:11:01 PM
What I do:
I am the center class to collect query node and doc node
for now (Jun 10)
    query has tagme result
    doc has facc annotation result
    will build framework upon them
What's my input:
query
What's my output:
query
lDoc
lObj (entity node)  
(all features waiting for edge feature extracting step, 
    scores discarded as all I am doing now is load cache,
    reduce the complexity of API by increasing a disk I/O)
@author: chenyanxiong
'''


'''
Jun 10
basic function implemented
not tested
'''

'''
Jun 10 add output format:
    a dir: each file is a q name, and contains all its objid
'''

'''
Jun 14 testing,
output to dir run successful
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
import json
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
from NodeCollection.QueryNodeTagMeCollector import QueryTagMeNodeCollectorC
from NodeCollection.DocNodeFaccAnaCollector import DocNodeFaccAnaCollectorC

from IndriSearch.IndriSearchCenter import IndriSearchCenterC

class NodeCollectorCenterC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.Searcher = IndriSearchCenterC()
        self.QueryNodeTagMeCollector = QueryTagMeNodeCollectorC()
        self.DocNodeFaccAnaCollector = DocNodeFaccAnaCollectorC()
        
        self.lQueryNodeGroup = []
        self.lDocNodeGroup = []
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.lQueryNodeGroup = self.conf.GetConf('querynodegroup',self.lQueryNodeGroup)
        self.lDocNodeGroup = self.conf.GetConf('docnodegroup', self.lDocNodeGroup)
        self.Searcher.SetConf(ConfIn)
        if 'tagme' in self.lQueryNodeGroup:
            self.QueryNodeTagMeCollector.SetConf(ConfIn)
        if 'facc' in self.lDocNodeGroup:
            self.DocNodeFaccAnaCollector.SetConf(ConfIn)
        
        logging.info('node collector center conf set')
        return
    
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        QueryTagMeNodeCollectorC.ShowConf()
        DocNodeFaccAnaCollectorC.ShowConf()
        IndriSearchCenterC.ShowConf()
        print 'querynodegroup tageme'
        print 'docnodegroup facc'
        
    
    def process(self,qid,query):
        '''
        retrieval lDoc
        call query node generator
        call doc node generator
        '''
        
        lDoc = self.Searcher.RunQuery(query, qid)
        
        
        lQObj = self.CollectQueryNode(qid,query)
        
        lDocObj = self.CollectDocNode(lDoc,qid,query)
        
        logging.info('[%s][%s] get [%d] doc [%d] q obj node [%d] doc obj node',qid,query,len(lDoc),len(lQObj),len(lDocObj))
        return lDoc,lQObj,lDocObj
    
    
    def CollectQueryNode(self,qid,query):
        lQNodeScore = []
        
        if 'tagme' in self.lQueryNodeGroup:
            lQNodeScore.extend(self.QueryNodeTagMeCollector.process(qid, query))
            
            
        lQObj = list(set([item[0] for item in lQNodeScore]))
        return lQObj
    
    def CollectDocNode(self,lDoc,qid,query):
        lDocObj = []
        if 'facc' in self.lDocNodeGroup:
            llDocNodeScore = self.DocNodeFaccAnaCollector.process(lDoc, qid, query)
            for lDocNodeScore in llDocNodeScore:
                if [] != lDocNodeScore:
                    lDocObj.extend([item[0] for item in lDocNodeScore])
            
        
        return lDocObj
    
    def PipeRun(self,QInName,OutName,OutFormat = 'json'):
        '''
        read qid,query
        run
        output to out name
        each line a json dumped [qid,query,lDoc,lQObj,lDocObj]
        '''
        
        lQidQuery = [line.split('\t') for line in open(QInName).read().splitlines()]
        
        if OutFormat == 'json':
            out = open(OutName,'w')
        
        for qid,query in lQidQuery:
            lDoc,lQObj,lDocObj = self.process(qid, query)
            if OutFormat == 'json':
                print >>out, json.dumps([qid,query,lDoc,lQObj,lDocObj])
            if OutFormat == 'dir':
                out = open(OutName + '/' + IndriSearchCenterC.GenerateQueryTargetName(query),'w')
                print >>out, '\n'.join(list(set(lQObj + lDocObj)))
                out.close()
        
        if OutFormat == 'json':    
            out.close()
        logging.info('query in [%s] node genereated, dumped to [%s]',QInName,OutName)
    
        
        
if __name__=='__main__':
    import sys,os

    if 2 != len(sys.argv):
        print 'I fetch node for queries (and their docs) in a given query file'
        print 'in\nout\noutformat'
        NodeCollectorCenterC.ShowConf()
        sys.exit()
    
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    ch.setFormatter(formatter)
    
    
    
    conf = cxConfC(sys.argv[1])
    InName = conf.GetConf('in')
    OutName = conf.GetConf('out')
    OutFormat = conf.GetConf('outformat')
    NodeCollector = NodeCollectorCenterC(sys.argv[1])
    
    NodeCollector.PipeRun(InName, OutName,OutFormat)
            
            
        
        
        
        
        
        
        
        
