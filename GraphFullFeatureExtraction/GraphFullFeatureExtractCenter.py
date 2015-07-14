'''
Created on Jul 14, 2015 11:39:09 AM
@author: cx

what I do:
    I am the center class to extract features for graph of each q-doc pair
what's my input:
    qid,query and their node

what's my output:
    the features of the graph

'''
from NodeCollection.NodeCollectCenter import NodeCollectorCenterC

'''
pipeline:

Init all extraction centers

For each query:
    Get nodes
    fill object infor
    
    call feature extraction of each part
    
    (if needed) fill in missing values?
        hard to do it here cause it is not global?
        if all features are not missing, it can be done here
    dump to disk
        raw format for manual check
        numpy format for model
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
site.addsitedir('/bos/usr0/cx/PyCode/SemanticSearch')

import os
import json
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
import pickle


from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC

from NodeCollection.NodeCollectCenter import NodeCollectorCenterC


from LeToRFeature.LeToRFeatureExtractCenter import LeToRFeatureExtractCenterC
from ObjObjFeatureExtraction.ObjObjFeatureExtractCenter import ObjObjFeatureExtractCenterC
from QueryObjectFeature.FbQObjFeatureExtractCenter import FbQObjFeatureExtractCenterC
from ObjectDocumentFeature.FbObjDocFeatureExtractCenter import FbObjDocFeatureExtractCenterC




class GraphFullFeatureExtractCenterC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
    
        self.NodeDir  = ""
        
        self.Searcher = IndriSearchCenterC()
        self.ObjCenter = FbObjCacheCenterC()
        
        self.QDocFeatureExtractor = LeToRFeatureExtractCenterC()
        self.QObjFeatureExtractor = FbQObjFeatureExtractCenterC()
        self.DocObjFeatureExtractor = FbObjDocFeatureExtractCenterC()
        self.ObjObjFeatureExtractor = ObjObjFeatureExtractCenterC()
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.NodeDir = self.conf.GetConf('nodedir') + '/'
        
        self.Searcher.SetConf(ConfIn)
        self.ObjCenter.SetConf(ConfIn)
        
        self.QDocFeatureExtractor.SetConf(ConfIn)
        self.QObjFeatureExtractor.SetConf(ConfIn)
        self.DocObjFeatureExtractor.SetConf(ConfIn)
        self.ObjObjFeatureExtractor.SetConf(ConfIn)
        
        logging.info('graph full feature extractor conf setted')
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        
        IndriSearchCenterC.ShowConf()
        FbObjCacheCenterC.ShowConf()
        
        LeToRFeatureExtractCenterC.ShowConf()
        FbQObjFeatureExtractCenterC.ShowConf()
        FbObjDocFeatureExtractCenterC.ShowConf()
        ObjObjFeatureExtractCenterC.ShowConf()
        
        
        
   
    def FormulateNodes(self,qid,query):
        '''
        get ldoc and read lObjId
        fill lObjId
        '''
        logging.info('formulating node for q [%s][%s]',qid,query)
        lDoc = self.Searcher.RunQuery(query, qid)
        
        lDocNo, lQObjId, llDocObjId = NodeCollectorCenterC.LoadRawFormatNodeRes(query, self.NodeDir) 
        
        #match lDoc dim lDocNo dim
        lDoc = IndriSearchCenterC.RearrangeDocOrder(lDoc,lDocNo)
        lQObj = [self.ObjCenter.FetchObj(ObjId) for ObjId in lQObjId]
        llDocObj = [[ self.ObjCenter.FetchObj(ObjId) for ObjId in lDocObjId] for lDocObjId in llDocObjId]
        
        
        logging.info('q[%s] all node fetched', qid)        
        return lDoc,lQObj, llDocObj 


    def Process(self,qid,query,OutDir):
        '''
        
        '''
        lDoc,lQObj, llDocObj = self.FormulateNodes(qid, query)
        
        
        for doc,lDocObj in zip(lDoc,llDocObj):
            hQDocFeature,lhQObjFeature,lhDocObjFeature,llhObjObjFeature = self.ExtractFeatureForOneQDoc(qid, query, doc, lQObj + lDocObj)
            self.DumpPerQRes(qid,query,doc,lQObj + lDocObj,hQDocFeature,lhQObjFeature,lhDocObjFeature,llhObjObjFeature,OutDir)
        
        
        logging.info('q [%s] processed')
        return True
            
            
        
        
    def PipeRun(self,QInName,OutDir):
        lQidQuery = [line.split('\t') for line in open(QInName).read().splitlines()]
        
        for qid,query in lQidQuery:
            self.Process(qid, query, OutDir)
            
        logging.info('queries in [%s] processed features at [%s]',QInName,OutDir)
        return True
        
            
        
    
    def ExtractFeatureForOneQDoc(self,qid,query,doc,lObj):
        #if wanna speed up, cache features
        #for clearity, now just extract multiple times
        
        
        hQDocFeature = self.QDocFeatureExtractor.Process(qid, query, doc)
        logging.debug('q[%s][%s] ltr feature extracted',query,doc.DocNo)
        
        lhQObjFeature = self.QObjFeatureExtractor.ProcessOneQuery([qid,query], lObj)
        logging.debug('q[%s][%s]  obj feature extracted',query,doc.DocNo)
        
        lhDocObjFeature = self.DocObjFeatureExtractor.ProcessOneQueryDocPair([qid,query], doc, lObj)
        logging.debug('q[%s][%s]  doc obj feature extracted',query,doc.DocNo)
        
        llhObjObjFeature = self.ObjObjFeatureExtractor.Process(qid, query, lObj) #symetric matrix
        logging.debug('q[%s] [%s] obj obj feature extracted',query,doc.DocNo)
        
        
        logging.debug('q [%s][%s]  all doc graph feature extracted',query,doc.DocNo)
        
        return hQDocFeature,lhQObjFeature,lhDocObjFeature,llhObjObjFeature
    
    
    def DumpPerQRes(self,qid,query,doc,lObj,hQDocFeature,lhQObjFeature,lhDocObjFeature,llhObjObjFeature,OutDir):
        '''
        raw:
            a dir for this q
                a file for each doc
                    node a, node b, hFeature.json
        '''

        if not os.path.exists(OutDir + '/' + qid):
            os.makedirs(OutDir + '/' + qid)
        
        OutName =     OutDir + '/' + qid + doc.DocNo
        out = open(OutName,'w')
        
        #q doc
        print >>out, 'q_%s' %(qid) + '\t' + doc.DocNo + '\t' + json.dumps(hQDocFeature)
        
        #obj doc
        for Obj, hDocObjFeature in zip(lObj,lhDocObjFeature):
            print >>out, Obj.GetId() + '\t' + doc.DocNo + '\t' + json.dumps(hDocObjFeature)

        #q obj
        for Obj, hQObjFeature in zip(lObj,lhQObjFeature):
            print >>out, 'q_%s' %(qid) + '\t' + Obj.GetId() + json.dumps(hQObjFeature)
            
        #obj obj
        for i in range(len(lObj)):
            for j in range(len(lObj)):
                if i == j:
                    continue
                print >>out, lObj[i].GetId() + '\t' + lObj[j].GetId() + '\t' + json.dumps(llhObjObjFeature[i][j])

        logging.info('q[%s] doc [%s] graph dumped to file [%s]',qid,doc.DocNo,OutName)
        return True
    

            
        
        
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print "I extract graph features for given query and node dir"
        GraphFullFeatureExtractCenterC.ShowConf()
        print 'in\noutdir'
        sys.exit()
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)       
        
    Extractor = GraphFullFeatureExtractCenterC(sys.argv[1])
    
    conf = cxConfC(sys.argv[1])
    QInName = conf.GetConf('in')
    OutDir = conf.GetConf('outdir')
    
    Extractor.PipeRun(QInName, OutDir)
    
            
            
        
        
        
   
        
        
        
        
        
        
        
    
        
        
        
        
        
        
        
        
        
        
        
