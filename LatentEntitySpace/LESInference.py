'''
Created on Aug 11, 2015 6:43:18 PM
@author: cx

what I do:
    I calculate p(q|d) using LES model
what's my input:
    q,doc, lQObj,lDocObj
what's my output:
    ranking score of this doc
'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from IndriRelate.LmBase import LmBaseC
from IndriSearch.IndriDocBase import IndriDocBaseC
from IndriRelate.CtfLoader import TermCtfC

class LESInferencer(object):
    
    @classmethod
    def inference(cls,query,doc,lQObj,lDocObj):
        
        lDObjSimToQ = cls.CalcObjDistributionOnQuery(lQObj, lDocObj)
        lDocObjScore = cls.CalcDocObjDistribution(doc, lDocObj)
        
        score = sum([item[0] * item[1] for item in zip(lDocObjScore,lDObjSimToQ)])
        return score
    
    
    @classmethod
    def CalcDocObjDistribution(cls,doc,lDocObj):
        DocLm = LmBaseC(doc)
        lObjLm = [LmBaseC(obj.GetDesp()) for obj in lDocObj]
        
        lDocObjScore = [LmBaseC.Similarity(ObjLm, DocLm, TermCtfC(), 'cosine') for ObjLm in lObjLm]
        
        Z = float(sum(lDocObjScore))
        lDocObjScore = [item/Z for item in lDocObjScore]
        
        return lDocObjScore
    
    
    @classmethod
    def CalcObjDistributionOnQuery(cls,lQObj,lDocObj):
        lQObjLm = [LmBaseC(obj.GetDesp()) for obj in lQObj]
        lDocObjLm = [LmBaseC(obj.GetDesp()) for obj in lDocObj]
        
        llDObjQObjSim = [ [LmBaseC.Similarity(QLm, DLm, TermCtfC(),'cosine') for QLm in lQObjLm] for DLm in lDocObjLm]
        
        lDObjSim = [sum(lDObjQObjSim) for lDObjQObjSim in llDObjQObjSim]
        
        Z = float(sum(lDObjSim))
        lDObjSim = [item / Z for item in lDObjSim]
        return lDObjSim