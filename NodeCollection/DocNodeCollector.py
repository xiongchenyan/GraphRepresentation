'''
Created on my MAC Jun 9, 2015-8:18:38 PM
What I do:
I am the virtual class for document node collector
What's my input:
IndriDocBaseC
What's my output:
lNodeScore
@author: chenyanxiong
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')


import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging

class DocNodeCollectorC(cxBaseC):
    
    def process(self,lDoc,qid,query):
        '''
        lDoc is packed doc res
        IndriDocBaseC
        '''
        llNodeScore = []
        logging.error('please call my sub class (DocNodeCollectorC)')
        return []
