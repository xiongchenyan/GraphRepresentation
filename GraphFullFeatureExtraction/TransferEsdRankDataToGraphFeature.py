'''
Created on Aug 9, 2015 4:14:34 PM
@author: cx

what I do:
    I transfer EsdRank data to graph data
what's my input:
    EsdRank data dir + query in
what's my output:
    a HCCRF data format dir

'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')

from HCCRF.DocGraph import DocGraphC
import logging

import sys,os

if 4 != len(sys.argv):
    print 'q in + esd rank data dir + out dir'
    sys.exit()
    
    
root = logging.getLogger()
root.setLevel(logging.DEBUG)
    
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)           

InDir = sys.argv[2]
OutDir = sys.argv[3]
    
lQid = [line.split('\t')[0] for line in open(sys.argv[1]).read().splitlines()]

llGraphData = [DocGraphC.LoadEsdRankOneQGraph(InDir, qid) for qid in lQid]

logging.info('loaded')

llGraphData = DocGraphC.FeatureMinMaxNormalization(llGraphData)

logging.info('normalized')

for qid,lGraphData in zip(lQid,llGraphData):
    QDir = OutDir + '/' + qid
    if not os.path.exists(QDir):
        os.makedirs(QDir)
    for GraphData in lGraphData:
        OutName = QDir + '/' + GraphData.DocNo
        GraphData.dump(OutName)
        
 
logging.info('dumped')    


