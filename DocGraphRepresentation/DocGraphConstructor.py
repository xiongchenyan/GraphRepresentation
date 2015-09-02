'''
Created on Sep 1, 2015 8:52:13 PM
@author: cx

what I do:
    I am the root class to construct doc graph
what's my input:

what's my output:


'''

import site
import logging

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC

import os
from DocKGUnsupervisedFormer import DocKGTagMeFormerC,DocKGFaccFormerC,DocKGUnsupervisedFormerC
from DocGraphRepresentation.DocKnowledgeGraph import DocKnowledgeGraphC


'''
TBD: abstract SearchResDocGraphConstructorC to this root class
implement annotated result doc graph constructor too
be aware of the output dump dir organization
'''