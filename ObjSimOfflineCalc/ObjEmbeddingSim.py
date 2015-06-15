'''
Created on my MAC Jun 10, 2015-7:43:14 PM
What I do:
calc the embedding sim
What's my input:
a dir: each dir is a query's target obj
What's my output:
id-id sim (id is sorted)
@author: chenyanxiong
'''

import gensim
import sys
import logging
import pickle

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.Vector import VectorC
from ObjSimBaseFunction import LoadPerQObjIdFromDir


def CalcSim(ObjInDir,OutName,Word2VecModel):
    lhQObjId = LoadPerQObjIdFromDir(ObjInDir)
    
    out = open(OutName,'w')
    hObjPairSim = {}
    
    for hQObjId in lhQObjId:
        lObjId = hQObjId.keys()
        lObjId.sort()
        for i in range(len(lObjId)):
            a = lObjId[i]
            if not a in Word2VecModel:
                continue
            vA = VectorC(list(Word2VecModel[a]))
            for j in range(i + 1,len(lObjId)):
                b = lObjId[j]
                if not b in Word2VecModel:
                    continue
                vB = VectorC(list(Word2VecModel[b]))
                score = VectorC.Similarity(vA, vB, 'cosine')
                hObjPairSim[a + '\t' + b] = score
    
    pickle.dump(out,hObjPairSim)
    logging.info('word2vec sim for [%s] finished, dump to',ObjInDir,OutName)
    return


if 4 != len(sys.argv):
    print 'I calculate obj embedding similarity'
    print '3 para: target obj dir in+ freebase word2vec in + out'
    sys.exit()
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)   

ObjDirInName = sys.argv[1]
OutName = sys.argv[3]

logging.info('start load freebase word2vec [%s]',sys.argv[2])
Word2VecModel = gensim.models.Word2Vec.load_word2vec_format(sys.argv[2])
logging.info('loaded')

CalcSim(ObjDirInName, OutName, Word2VecModel)

            
            
    
    
