'''
Created on my MAC Mar 4, 2015-10:57:12 AM
What I do:
I calculate the most sim objects for each input objects
via text similarity

1, get name
2, search in object index, get top 1000 result
3, get both descriptions (if no, discard)
4, rank by description's KL divergence
What's my input:
objid \t name
What's my output:
objid objid score name1 name2
@author: chenyanxiong
'''


import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')

from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from ObjCenter.FbObjCacheCenter import FbObjCacheCenterC
from cxBase.Vector import VectorC
from cxBase.TextBase import TextBaseC
from IndriRelate.IndriInferencer import LmBaseC
import json
class EntityCorrelationFromTextSimC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.Searcher = IndriSearchCenterC()
        self.ObjCenter = FbObjCacheCenterC()
        self.NeighborNum = 50
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.Searcher.SetConf(ConfIn)
        self.ObjCenter.SetConf(ConfIn)
        self.NeighborNum = self.conf.GetConf('neighbornum', self.NeighborNum)
        
        
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        IndriSearchCenterC.ShowConf()
        FbObjCacheCenterC.ShowConf()
        print 'neighbornum'
        
        
    
    
    def ProcessOneObj(self,ObjId,name):
        '''
        return lObjNeighbor=[objid,KL score] top self.NeighborNum
        '''
        
        #search in index, get top 1000
        query = TextBaseC.RawClean(name)
        if "" == query:
            return []
        lObjDoc = self.Searcher.RunQuery(query)
        
        lObjNeighbor = []
        
        ThisDesp = self.ObjCenter.FetchObjDesp(ObjId)
        ThisLm = LmBaseC(ThisDesp)
        ThisVec = VectorC(ThisLm.hTermTF)
#         print '[%s:%s] desp : [%s]' %(ObjId,name,ThisDesp)
        if len(ThisLm.hTermTF) == 0:
            return []
        for ObjDoc in lObjDoc:
            Id = ObjDoc.DocNo
            if Id == ObjId:
                continue
            if not Id.startswith('/m/'):
                print "[%s %s] neighbor id [%s] format error" %(ObjId,name,Id)
                continue 
#             print "get neighbor [%s] [%s]" %(Id,ObjDoc.GetContent())
#             NeighborDesp = ObjDoc.GetContent()
            NeighborLm = LmBaseC(ObjDoc)
            NeighborVec = VectorC(NeighborLm.hTermTF)
            if len(NeighborVec.hDim) == 0:
                continue
            score = VectorC.KL(ThisVec, NeighborVec)
            lObjNeighbor.append([Id,-score])
#             print "[%s %s] KL [%f]" %(ObjId,Id,score)
#             print "%s\n%s" %(json.dumps(ThisVec.hDim),json.dumps(NeighborVec.hDim))
            
        lObjNeighbor.sort(key=lambda item:item[1],reverse = True)
        print "[%s:%s] neighbor id score get" %(ObjId,name)
        return lObjNeighbor
    
    def Process(self,ObjInName,OutName):
        out = open(OutName,'w')
        
        for line in open(ObjInName):
            vCol = line.strip().split('\t')
            if len(vCol) < 2:
                continue
            lObjNeighbor = self.ProcessOneObj(vCol[0], vCol[1])
            for NeighborId,score in lObjNeighbor[:self.NeighborNum]:
                print >>out, '%s\t%s\t%f\t%s\t%s' %(vCol[0],NeighborId,score,vCol[1],self.ObjCenter.FetchObjName(NeighborId))
            print "[%s:%s] done" %(vCol[0],vCol[1])
        
        out.close()
        print "finished"
        
        
import sys

if 2 != len(sys.argv):
    EntityCorrelationFromTextSimC.ShowConf()
    print "in\nout"
    sys.exit()
    
Generator = EntityCorrelationFromTextSimC(sys.argv[1])
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')
Generator.Process(InName, OutName)

        
        

                
             
            
        
        
        

