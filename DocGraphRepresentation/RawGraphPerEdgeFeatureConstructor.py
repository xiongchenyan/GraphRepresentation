'''
Created on Sep 9, 2015 11:13:10 AM
@author: cx

what I do:
    I construct graph with nodes the same as SearchResDocGraphConstructorC
        but add edge-edge mtx with obj-obj edge features
        will output one dir for each edge feature dimension
what's my input:
    query and serp cache
    resources needed by DocKGUnsupervisedFormer
    resources needed by ObjObj edge feature
    

what's my output:
    a directory
        one directory for each edge feature dimension
            /qid/DocNo
                each file is the dump of DocKg
                    with edge matrix


'''


import site
import logging

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC
# from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC
import os
# from DocKGUnsupervisedFormer import DocKGTagMeFormerC,DocKGFaccFormerC,DocKGUnsupervisedFormerC
# from DocGraphRepresentation.DocKnowledgeGraph import DocKnowledgeGraphC
from ObjObjFeatureExtraction.ObjObjFeatureExtractCenter import ObjObjFeatureExtractCenterC
import numpy as np
from ConstructSearchResDocGraph import SearchResDocGraphConstructorC


class RawGraphPerEdgeFeatureConstructorC(SearchResDocGraphConstructorC):
    
    def Init(self):
        SearchResDocGraphConstructorC.Init(self)
        self.EdgeFeatureCenter = ObjObjFeatureExtractCenterC()
        self.ObjCenter = FbObjCacheCenterC()
        
        
        
        
    def SetConf(self, ConfIn):
        SearchResDocGraphConstructorC.SetConf(self, ConfIn)
        self.EdgeFeatureCenter.SetConf(ConfIn)
        self.ObjCenter.SetConf(ConfIn)
        
        
    @staticmethod
    def ShowConf():
        SearchResDocGraphConstructorC.ShowConf()
        ObjObjFeatureExtractCenterC.ShowConf()
        FbObjCacheCenterC.ShowConf()
        
        
    def FormForOneQ(self,qid,query):
        lDoc = self.Searcher.RunQuery(query, qid)
        lDocKg = [self.GraphFormer.FillDocGraph(doc.DocNo) for doc in lDoc]
        
        
        for DocKg in lDocKg:
            lObjId = DocKg.hNodeId
            lObj = [self.ObjCenter.FetchObj(ObjId) for ObjId in lObjId]
            mhFeature = self.EdgeFeatureCenter.ExtractObjObjFeature(lObj, query) 
            for FeatureName in self.EdgeFeatureCenter.FeatureDims():
                OutDir = self.OutDir + '/' + FeatureName + '/' + qid
                if not os.path.exists(OutDir):
                    os.makedirs(OutDir)
                
                llEdgeFeatureScore = [[ hFeature[FeatureName] for hFeature in lhFeature] for lhFeature in mhFeature ]
                DocKg.mEdgeMatrix = np.array(llEdgeFeatureScore)
                DocKg.dump(OutDir + '/' + DocKg.DocNo)
                logging.debug('[%s] feature for doc [%s] dummped',FeatureName,DocKg.DocNo)
                
            logging.debug('[%s] dummped [%d] node',DocKg.DocNo,len(DocKg))
        logging.info('[%s-%s] doc kg formed',qid,query)
        return True
    
    
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        print 'I construct query search result doc kg with each edge features'
        print 'in'
        RawGraphPerEdgeFeatureConstructorC.ShowConf()
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)          
    
    Processor = RawGraphPerEdgeFeatureConstructorC(sys.argv[1])
    
    conf = cxConfC(sys.argv[1])
    QInName = conf.GetConf('in', '/bos/usr0/cx/tmp/data/WebTrackQ09')
    Processor.Process(QInName)    
