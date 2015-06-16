'''
Created on my MAC Jun 10, 2015-3:13:59 PM
What I do:
    I am the center for edge feature extraction
What's my input:
    qid,query,lDoc,lQObj,lDocObj
What's my output:
    the features between any two
        call all edge feature extractors to complete the job
            maybe one center for each of them? (no)

TBD:
    think about how to store these features in a tensor or so
        so that they can be used in numpy+sckipy based graph ranking model
@author: chenyanxiong
'''

'''
pipeline:
    get input:
    fill the objid to obj (APIBase etc.)
    call feature extraction for:
        q-obj
        doc-obj
        obj-obj features
        and pack them into numpy format (TBD:study how)
    output

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
import pickle

from EdgeFeatureExtraction.QueryObjEdgeFeatureTagMeExtractor import QueryObjEdgeFeatureTagMeExtractorC
from EdgeFeatureExtraction.DocObjEdgeFeatureFaccExtractor import DocObjEdgeFeatureFaccExtractorC
from EdgeFeatureExtraction.ObjObjEdgeFeatureKGExtractor import ObjObjEdgeFeatureKGExtractorC
from EdgeFeatureExtraction.ObjObjEdgeFeaturePreCalcSimExtractor import ObjObjEdgeFeaturePreCalcSimExtractorC
from EdgeFeatureExtraction.ObjObjEdgeFeatureTextSimExtractor import ObjObjEdgeFeatureTextSimExtractorC

from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC


class EdgeFeatureExtractCenterC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        
        self.lQObjFeatureGroup = []
        self.lObjObjFeatureGroup = []
        self.lDocObjFeatureGroup = []
        
        self.QObjTagMeExtractor = QueryObjEdgeFeatureTagMeExtractorC()
        self.DocObjFaccExtractor = DocObjEdgeFeatureFaccExtractorC()
        self.ObjObjKGExtractor = ObjObjEdgeFeatureKGExtractorC()
        self.ObjObjPreCalcExtractor = ObjObjEdgeFeaturePreCalcSimExtractorC()
        self.ObjObjTextSimExtractor = ObjObjEdgeFeatureTextSimExtractorC()
        
        self.Searcher = IndriSearchCenterC()
        self.ObjCenter = FbObjCacheCenterC()
        self.NodeDir = ""
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.Searcher.SetConf(ConfIn)
        self.ObjCenter.SetConf(ConfIn)
        
        self.NodeDir = self.conf.GetConf('nodedir') + '/' 
        
        
        self.lQObjFeatureGroup = self.conf.GetConf('qobjfeaturegroup', self.lQObjFeatureGroup)
        self.lDocObjFeatureGroup = self.conf.GetConf('docobjfeaturegroup', self.lDocObjFeatureGroup)
        self.lObjObjFeatureGroup = self.conf.GetConf('objobjfeaturegroup', self.lObjObjFeatureGroup)
        
        if 'tagme' in self.lQObjFeatureGroup:
            self.QObjTagMeExtractor.SetConf(ConfIn)
        if 'facc' in self.lQObjFeatureGroup:
            self.DocObjFaccExtractor.SetConf(ConfIn)
        
        if 'kg' in self.lObjObjFeatureGroup:
            self.ObjObjKGExtractor.SetConf(ConfIn)
        if 'precalc' in self.lObjObjFeatureGroup: 
            self.ObjObjPreCalcExtractor.SetConf(ConfIn)
        if 'textsim' in self.lObjObjFeatureGroup:
            self.ObjObjTextSimExtractor.SetConf(ConfIn)
            
        logging.info('edge feature center confs setted')
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        IndriSearchCenterC.ShowConf()
        FbObjCacheCenterC.ShowConf()
        
        print 'nodedir\nqobjfeaturegroup\ndocobjfeaturegroup\nobjobjfeaturegroup'
        
        QueryObjEdgeFeatureTagMeExtractorC.ShowConf()
        DocObjEdgeFeatureFaccExtractorC.ShowConf()
        ObjObjEdgeFeatureKGExtractorC.ShowConf()
        ObjObjEdgeFeaturePreCalcSimExtractorC.ShowConf()
        ObjObjEdgeFeatureTextSimExtractorC.ShowConf()
        
        
    def FormulateNodes(self,qid,query):
        '''
        get ldoc and read lObjId
        fill lObjId
        '''
        lDoc = self.Searcher.RunQuery(query, qid)
        
        lObjId = open(self.NodeDir + IndriSearchCenterC.GenerateQueryTargetName(query)).read().splitlines()
        
        lObj = [self.ObjCenter.FetchObj(ObjId) for ObjId in lObjId]
        
        return lDoc,lObj
    
    
    def ExtractPerQObj(self,qid,query,obj):
        hFeature = {}
        if 'tagme' in self.lQObjFeatureGroup:
            hFeature.update(self.QObjTagMeExtractor.process(qid, query, obj))
        return hFeature
    
    def ExtractQObjFeature(self,qid,query,lObj):
        lhFeature = {}
        
        for obj in lObj:
            hFeature = self.ExtractPerQObj(qid, query, obj)
            lhFeature.append(hFeature)
        logging.info('q obj feature extracted')
        return lhFeature
    
    
    
    def ExtractPerDocObj(self,doc,obj):
        hFeature = {}
        if 'facc' in self.lDocObjFeatureGroup:
            hFeature.update(self.DocObjFaccExtractor.process(doc, obj))
        
        return hFeature
    
    def ExtractDocObjFeature(self,lDoc,lObj):
        llhFeature = {}   #doc \times obj
        for doc in lDoc:
            lhFeature = {}
            for obj in lObj:
                hFeature = self.ExtractPerDocObj(doc,obj)
                lhFeature.append(hFeature)
            llhFeature.append(lhFeature)
        logging.info('doc obj feature extracted')
        return llhFeature
    
    
    def ExtractPerObjObj(self,ObjA,ObjB):
        hFeature = {}
        if 'kg' in self.lObjObjFeatureGroup:
            hFeature.update(self.ObjObjKGExtractor.process(ObjA, ObjB))
        if 'precalc' in self.lObjObjFeatureGroup:
            hFeature.update(self.ObjObjPreCalcExtractor.process(ObjA, ObjB))
        if 'textsim' in self.lObjObjFeatureGroup:
            hFeature.update(self.ObjObjTextSimExtractor.process(ObjA, ObjB))
            
        return hFeature
    
    def ExtractObjObjFeature(self,lObj):
        llhFeature = {}   #obj -> obj, diagonal is empty
        for ObjA in lObj:
            lhFeature = {}
            for ObjB in lObj:
                if ObjA.GetId() == ObjB.GetId():
                    continue
                hFeature = self.ExtractPerObjObj(ObjA, ObjB)
                lhFeature.append(hFeature)
            llhFeature.append(lhFeature)
        
        logging.info('obj obj feature extracted')
        return llhFeature
    
    
    def Process(self,qid,query):
        
        lDoc,lObj = self.FormulateNodes(qid, query)
        logging.info('nodes fetched')
        
        lQObjFeature = self.ExtractQObjFeature(qid, query, lObj)
        
        llDocObjFeature = self.ExtractDocObjFeature(lDoc, lObj)
        
        llObjObjFeature = self.ExtractObjObjFeature(lObj)
        
        return lDoc,lObj,lQObjFeature,llDocObjFeature,llObjObjFeature
    
    
    
    def DumpRes(self,OutName, query, lDoc,lObj,lQObjFeature,llDocObjFeature,llObjObjFeature):
        out = open(OutName,'w')
        
        for obj, hFeature in zip(lObj,lQObjFeature):
            print >> out,query + '\t' + obj.GetId() + '\t' + json.dumps(hFeature)
            
        for doc,lhFeature in zip(lDoc,llDocObjFeature):
            for obj,hFeature in zip(lObj,lhFeature):
                print >>out, doc.DocNo + '\t' + obj.GetId() + '\t' + json.dumps(hFeature)
            
            
        for ObjA,lhFeature in zip(lObj,llObjObjFeature):
            for ObjB,hFeature in zip(lObj,lhFeature):
                print >>out, ObjA.GetId() + '\t' + ObjB.GetId() + '\t' + json.dumps(hFeature)
                
        out.close()
        logging.info('query [%s] feature dumped',query)
        
        
        
    def PipeRun(self,QInName,OutDir):
        '''
        for now:
            output raw type
            each file is a query's edge features
                each line is query|doc|obj \t obj \t json.dumps(hFeature)
        '''
        
        lQidQuery = [line.split() for line in open(QInName).read().splitlines()]
        
        for qid,query in lQidQuery:
            logging.info('start extracting for [%s][%s]',qid,query)
            lDoc,lObj, lQObjFeature,llDocObjFeature,llObjObjFeature = self.Process(qid, query)
            OutName = OutDir + '/' + IndriSearchCenterC.GenerateQueryTargetName(query)
            self.DumpRes(OutName, lDoc,lObj,lQObjFeature,llDocObjFeature,llObjObjFeature)
        
        logging.info('all finished')
        return
    
    
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print "I extract edge features for given query and node dir"
        EdgeFeatureExtractCenterC.ShowConf()
        print 'in\noutdir'
        sys.exit()
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)       
        
    Extractor = EdgeFeatureExtractCenterC(sys.argv[1])
    
    conf = cxConfC(sys.argv[1])
    QInName = conf.GetConf('in')
    OutDir = conf.GetConf('outdir')
    
    Extractor.PipeRun(QInName, OutDir)
    
            
            
        
        
        
        
    
    
    
        
        
                
        
        
        
        
        
        
        
    
        
        





