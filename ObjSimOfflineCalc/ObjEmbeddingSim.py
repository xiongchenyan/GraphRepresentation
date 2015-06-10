'''
Created on my MAC Jun 10, 2015-7:43:14 PM
What I do:
calc the embedding sim
What's my input:
a file:
each line is an id
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

def CalcSim(ObjInName,OutName,Word2VecModel):
    lObjId = open(ObjInName).read().splitlines()
    lObjId.sort()
    
    out = open(OutName,'w')
    hObjPairSim = {}
    for i in range(len(lObjId)):
        if not lObjId[i] in Word2VecModel:
            continue
        vA = VectorC(list(Word2VecModel[lObjId[i]]))
        for j in range(i + 1,len(lObjId)):
            if not lObjId[j] in Word2VecModel:
                continue
            vB = VectorC(list(Word2VecModel[lObjId[j]]))
            score = VectorC.Similarity(vA, vB, 'cosine')
            hObjPairSim[lObjId[i] + '\t' + lObjId[j]] = score
    
    pickle.dump(out,hObjPairSim)
    logging.info('word2vec sim for [%s] finished, dump to',ObjInName,OutName)
    return


if 4 != len(sys.argv):
    print 'I calculate obj embedding similarity'
    print '3 para: obj id + freebase word2vec in + out'
    sys.exit()
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)   

ObjInName = sys.argv[1]
OutName = sys.argv[3]

logging.info('start load freebase word2vec [%s]',sys.argv[2])
Word2VecModel = gensim.models.Word2Vec.load_word2vec_format(sys.argv[2])
logging.info('loaded')

CalcSim(ObjInName, OutName, Word2VecModel)

            
            
    
    
