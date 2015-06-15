'''
Created on Feb 23, 2015 4:04:33 PM
@author: cx

what I do:
I generate entity correlation per file
what's my input:
    a file (with full path)
    target object id
    a type (facc|fakba)
    an output dir
what's my output:
    in the output dir, the correlation with this file name prefix
        so I will need to get the file name from the input file name

'''
'''
because it is per file, I can store the pairs in memory, and sort them in output
'''

'''
June 11
now only generate target pair's correlation
will be much smaller

need a major reconstruction.
pack it into a class
fiter function is a class function, with choices    
'''

import ntpath
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/SemanticSearch')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')


from Facc.FaccReader import FaccReaderC
from Facc.FakbaReader import FakbaReaderC
import sys
import logging


class EntityCorrelationPerDocCounterC(object):
    def __init__(self):
        self.Init()
        
    def Init(self):
        self.FilterType = 'targetpair'
        self.TargetIdInName = ""
        self.TargetPairInName = ""
        self.sTargetId = set()
        self.sTargetPair = set()
        self.InType = 'facc'
        
    
    def prepare(self):
        if self.FilterType == 'targetpair':
            self.ReadTargetPair()
        if self.FilterType == 'targetid':
            self.ReadTargetId()
    
    def ReadTargetId(self):
        if "" == self.TargetIdInName:
            return
        lId = open(self.TargetIdInName).read().splitlines()
        self.sTargetId = set(lId)
    
    def ReadTargetPair(self):
        if "" == self.TargetPairInName:
            return
        logging.info('start read tart pair from [%s]',self.TargetPairInName)
        for line in open(self.TargetPairInName):
            vCol = line.strip().split()
            vCol.sort()
            self.sTargetPair.add('\t'.join(vCol))
        logging.info('[%d] target pair read from [%s]', len(self.sTargetPair),self.TargetPairInName)
    
    def GenerateOutNameFromInName(self,InName):
        '''
        if facc: then the last two dim of directory + file name
        if fakba: just InName
        '''
        if self.InType != 'facc':
            return ntpath.basename(InName)
        
        vCol = InName.split('/')
        return '_'.join(vCol[-3:])
    
    
    
    def FormObjPairFromFile(self,InName):
        hPair = {}
        if self.InType == 'facc':
            Reader = FaccReaderC()
        else:
            Reader = FakbaReaderC()
            
        Reader.open(InName)
        cnt = 0
        PairCnt = 0
        for lAna in Reader:
            for i in range(len(lAna)):
                for j in range(i + 1,len(lAna)):       
                    if lAna[j].st - lAna[i].st > 100:
                        break
                    if lAna[i].ObjId == lAna[j].ObjId:
                        continue
                    if self.Filter(lAna[i].ObjId,lAna[j].ObjId):
                        continue
                    
                    lObjId = [lAna[i].ObjId,lAna[j].ObjId]
                    lObjId.sort()
                    key = ' '.join(lObjId)
                    if not key in hPair:
                        hPair[key] = 1
                    else:
                        hPair[key] += 1
                    PairCnt += 1
            cnt += 1
            if 0 == (cnt % 100):
                print 'processed [%d] doc' %(cnt)
        return hPair
    
    def Process(self,InName,OutDir):
        
        self.prepare()
        
        hPair = self.FormObjPairFromFile(InName)
        
        OutName = OutDir + '/' + self.GenerateOutNameFromInName(InName)
        out = open(OutName,'w')
        lPairCnt = hPair.items()
        lPairCnt.sort(key = lambda item: item[0])
        for Pair,cnt in lPairCnt:
            print >>out, Pair + ' %d' %(cnt)
        out.close()        
        print 'finished to [%s] in [%d] pair pairwise correlation' %(OutName,len(hPair))
        
        return True
        

        
        

if __name__ == '__main__':

    if 5 != len(sys.argv):
        print "InName + outdir + target pair in + intype (facc|fakba)"
        sys.exit()
        
    Calcer = EntityCorrelationPerDocCounterC()
    Calcer.FilterType = 'targetpair'
    Calcer.TargetPairInName = sys.argv[3]
    Calcer.InType = sys.argv[4]
    Calcer.Process(sys.argv[1], sys.argv[2])
    







