'''
Created on my MAC Jun 9, 2015-5:14:58 PM
What I do:
I collect given query's initial retrieved document's content from boilerpipe
What's my input:
query, search dir
boilerpipe result
What's my output:
a folder, contains one file for each query, which is:
    DocNo \t text
@author: chenyanxiong
'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')


import os
from cxBase.Conf import cxConfC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC

import logging


def PrepareTargetDocNo(lQidQuery,IndriSearcher):
    hDocNoToQuery = {}
    
    for qid,query in lQidQuery:
        lDoc = IndriSearcher.RunQuery(query)
        lDocNo = [doc.DocNo for doc in lDoc]
        for DocNo in lDocNo:
            if not DocNo in hDocNoToQuery:
                hDocNoToQuery[DocNo] = [query]
            else:
                hDocNoToQuery[DocNo].append(query)
                
    logging.info('prepare target doc no for given queries finished')
    return hDocNoToQuery
    

def FetchBoilerPipeText(BoilerPipeInName, hDocNoToQuery):
    hQueryDocText = {}   #query->[[DocNo,text]]
    FetchedCnt = 0
    for cnt,line in enumerate(open(BoilerPipeInName)):
        if 0 == (cnt % 1000):
            logging.info('traversing boiler pipe [%d] line',cnt)
        
        vCol = line.strip().split()
        if len(vCol) < 2:
            continue
        DocNo = vCol[0]
        if not DocNo in hDocNoToQuery:
            continue
        text = ' '.join(vCol[1:])
        FetchedCnt += 1
        for query in hDocNoToQuery[DocNo]:
            if not query in hQueryDocText:
                hQueryDocText[query] = [[DocNo,text]]
            else:
                hQueryDocText[query].append([DocNo,text])
                
    logging.info('all target doc text fetched, found [%d/%d]',FetchedCnt,len(hDocNoToQuery))
    return hQueryDocText

def OutputDocText(hQueryDocText,OutDir):
    for query,lDocNoText in hQueryDocText.items():
        out = open(OutDir + '/' + IndriSearchCenterC.GenerateQueryTargetName(query),'w')
        for DocNo,text in lDocNoText:
            print >>out, DocNo + '\t'+ text
        logging.info('query [%s] [%d] doc text  outputed',query,len(lDocNoText))
        out.close()
    logging.info('doc text dumped to [%s]',OutDir)
    return True


import sys,os

if 2 != len(sys.argv):
    print 'I fetch boilerpipe text for given queries retrieved docs'
    print 'qin\nboilerpipein\noutdir'
    IndriSearchCenterC.ShowConf()
    sys.exit()

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
ch.setFormatter(formatter)
    
    
    
IndriSearcher = IndriSearchCenterC(sys.argv[1])
conf = cxConfC(sys.argv[1])
QueryInName = conf.GetConf('qin')
BoilerInName = conf.GetConf('boilerpipein')
OutDir = conf.GetConf('outdir')
if not os.path.exists(OutDir):
    os.makedirs(OutDir)

lQidQuery = [line.strip().split('\t') for line in open(QueryInName)]
hDocNoToQuery = PrepareTargetDocNo(lQidQuery, IndriSearcher)
hQueryDocText = FetchBoilerPipeText(BoilerInName,hDocNoToQuery)
OutputDocText(hQueryDocText, OutDir)
logging.info('finished') 
    
                   
        
        

