'''
Created on my MAC Jun 9, 2015-7:26:01 PM
What I do:
I collect nodes that associate with query
nodes are represented solely by id
I am a virtual class, each specific class is a sub class of me
What's my input:
qid query + other required data
What's my output:
lObjId = [[mid,score]]
@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')


import os
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
import logging


class QueryNodeCollectorC(cxBaseC):
    
    def process(self,qid, query):
        lNodeScore = []
        
        
        return lNodeScore
