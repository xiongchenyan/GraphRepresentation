'''
Created on my MAC Jun 10, 2015-4:09:47 PM
What I do:
extract obj-obj from original knowledge graph
What's my input:
obj obj
What's my output:
hFeature
@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging
from ObjObjFeatureExtraction.ObjObjEdgeFeatureExtractor import ObjObjEdgeFeatureExtractorC
import json
class ObjObjEdgeFeatureKGExtractorC(ObjObjEdgeFeatureExtractorC):
    
    def Init(self):
        ObjObjEdgeFeatureExtractorC.Init(self)
        self.FeatureName += 'KG'
        self.lFeatureDim = [self.FeatureName + item for item in ['Connected','HasCommonNeighbor']]
        
        
    def process(self, ObjA, ObjB):
        hFeature = {}
        logging.debug('extracting kg feature for [%s]-[%s]',ObjA.GetId(),ObjB.GetId())
        hFeature.update(self.ExtractDirectConnectFeature(ObjA,ObjB))
        
        hFeature.update(self.ExtractTwoHopFeature(ObjA,ObjB))   #the longest path useful in literature is only two hop
        logging.debug('[%s]-[%s] obj kg sim features extracted %s',ObjA.GetId(),ObjB.GetId(),json.dumps(hFeature))
        return hFeature
    
    def FeatureDims(self):
        return self.lFeatureDim
    
    
    def ExtractDirectConnectFeature(self,ObjA,ObjB):
        hFeature = {}
        logging.debug('[%s-%s] direct connection features:',ObjA.GetId(),ObjB.GetId())
        
        
        lObjANeighbor = ObjA.GetNeighbor()
        sANeighborId = set([item[1] for item in lObjANeighbor])
        lObjBNeighbor = ObjB.GetNeighbor()
        sBNeighborId = set([item[1] for item in lObjBNeighbor])
        
#         logging.debug('%s neighbor: %s  target %s',ObjA.GetId(),json.dumps(list(sANeighborId)),ObjB.GetId())
        
        FeatureName = self.FeatureName + 'Connected'
        score = 0
        if (ObjB.GetId() in sANeighborId) | (ObjA.GetId() in sBNeighborId):
            score = 1
        hFeature[FeatureName] = score
        logging.debug('[%s:%f]',FeatureName,score)
        
#         FeatureName = self.FeatureName + 'HopOneProb'
#         score = 0
#         if ObjB.GetId() in sNeighborId:
#             score = 1.0 / float(len(ObjA.GetField('Neighbor')) + len(ObjB.GetField('Neighbor')))
#         hFeature[FeatureName] = score
#         logging.debug('[%s:%f]',FeatureName,score)
        return hFeature
    
    def ExtractTwoHopFeature(self,ObjA,ObjB):
        hFeature = {}
        logging.debug('[%s-%s] two hop connection features:',ObjA.GetId(),ObjB.GetId())
        
        
        lObjANeighbor = ObjA.GetNeighbor()
        sANeighborId = set([item[1] for item in lObjANeighbor])
        lObjBNeighbor = ObjB.GetNeighbor()
        sBNeighborId = set([item[1] for item in lObjBNeighbor])
        
#         FeatureName = self.FeatureName + 'CommonNeighborFrac'
#         score = 0
#             
#         
#         for ObjId in sANeighborId:
#             if ObjId in sBNeighborId:
#                 score += 1
#         if len(sANeighborId) != 0:
#             score /= len(sANeighborId)
#             
#         hFeature[FeatureName] = score
#         logging.debug('[%s:%f]',FeatureName,score)

        FeatureName = self.FeatureName + 'HasCommonNeighbor'
        score = 0
        for ObjId in sANeighborId:
            if ObjId in sBNeighborId:
                score = 1
                break
        hFeature[FeatureName] = score
        return hFeature
        
                
        
        
        
        
        
        
        
        