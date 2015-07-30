'''
Created on my MAC Jul 29, 2015-9:22:33 PM
What I do:
    I fetch the most frequent k facc obj's description
What's my input:
    facc idf in + all fb desp file + top k + output
What's my output:
    the name, id and desp of top k facc obj
@author: chenyanxiong
'''


import sys,logging

def LoadTopKFaccObjId(InName,k):
    lObjId = []
    
    for line in open(InName):
        vCol = line.strip().split('\t')
        if len(vCol) != 2:
            continue
        lObjId.append(vCol[0])
        if len(lObjId) >= k:
            break
    return lObjId



def FetchTargetDesp(DespInName,lObjId,OutName):
    sObjId = set(lObjId)
    print 'target [%d] obj' %(len(sObjId))
    out = open(OutName,'w')
    for line in open(DespInName):
        line = line.strip()
        vCol = line.split('\t')
        if vCol[1] in sObjId:
            print >>out, line
            
    out.close()
    return


def Process(DespInName,FaccIdfInName,k,OutName):
    
    lObjId = LoadTopKFaccObjId(FaccIdfInName, k)
    FetchTargetDesp(DespInName, lObjId, OutName)
    print 'done'
    
    
if 5 != len(sys.argv):
    print 'I fetch facc top obj desp'
    print 'desp in name, facc idf in, k, out name'
    sys.exit()
    
    
Process(sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4])        
        
    
