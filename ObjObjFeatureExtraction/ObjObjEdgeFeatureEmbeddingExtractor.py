'''
Created on Sep 9, 2015 10:46:10 AM
@author: cx

what I do:
    get the embedding sim between a given obj pair
what's my input:
    I am a subclass of ObjObjEdgeFeatureExtractorC
what's my output:
    {EmbCos:score}

'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')
import gensim
import os
import logging
from ObjObjFeatureExtraction.ObjObjEdgeFeatureExtractor import ObjObjEdgeFeatureExtractorC

class ObjObjEdgeFeatureEmbSimExtractorC(ObjObjEdgeFeatureExtractorC):
    
    def Init(self):
        ObjObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'EmbSim'
        self.Word2VecModel = None
        
    def SetConf(self, ConfIn):
        ObjObjEdgeFeatureExtractorC.SetConf(self, ConfIn)
        Word2VecIn = self.conf.GetConf('word2vecin')
        logging.info('start load word2vec from [%s]',Word2VecIn)
        self.Word2VecModel = gensim.models.Word2Vec.load_word2vec_format(Word2VecIn)
        logging.info('loaded')
        
    @staticmethod
    def ShowConf():
        ObjObjEdgeFeatureExtractorC.ShowConf()
        print 'word2vecin'    
        
        
    def process(self, ObjA, ObjB):
        hFeature = {}
        hFeature.update(self.ExtractEmbSimFeature(ObjA,ObjB))
#         logging.debug('[%s]-[%s] obj emb sim features extracted %s',ObjA.GetId(),ObjB.GetId(),json.dumps(hFeature))
        return hFeature
    
    def ExtractEmbSimFeature(self,ObjA,ObjB):
        hFeature = {}
        
        score = 0
        if (ObjA.GetId() in self.Word2VecModel) & (ObjB.GetId() in self.Word2VecModel):
            score = self.Word2VecModel.similarity(ObjA.GetId(),ObjB.GetId())
        hFeature[self.FeatureName +'Cosine'] = score    
        return hFeature



