'''
Created on my MAC Jun 10, 2015-2:59:26 PM
What I do:
edge features between q-obj
    basically only tagme rho for now
What's my input:
query + obj
What's my output:
hFeature
@author: chenyanxiong
'''

'''
I am the virtual class
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')


from cxBase.base import cxBaseC
import logging


class QueryObjEdgeFeatureExtractorC(cxBaseC):
    
    def Init(self):
        self.FeatureName = 'QObjEdge'
    
    def process(self,qid,query,obj):
        hFeature = {}
        logging.error('please call my subclass QueryObjEdgeFEatureExtractorC')
        return hFeature