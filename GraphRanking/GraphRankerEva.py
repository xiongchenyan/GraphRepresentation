'''
Created on Sep 9, 2015 1:38:11 PM
@author: cx

what I do:
    I evaluate graph ranker
what's my input:
    stuff required by GraphRanker
    stuff required by RankEvaluator
    ranker name
what's my output:
    evaluation results of ranker

'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GraphRepresentation')


from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC

import sys,os
from AdhocEva.RankerEvaluator import RankerEvaluatorC
import logging

from GraphRanker import GraphRankerC
from InDegreeRanker import InDegreeRankerC
from BoeLanguageModel.BoeLmRanker import BoeLmRankerC

def ChooseRanker(RankerName):
    if RankerName == 'boe':
        return BoeLmRankerC
    if RankerName == 'indegree':
        return InDegreeRankerC
    if RankerName == 'pr':
        raise NotImplementedError
    
    logging.error('[%s] not implemented',RankerName)
    raise NotImplementedError
    


if 2 != len(sys.argv):
    print 'I evaluate Boe lm '
    print 'in\nout'
    GraphRankerC.ShowConf()
    RankerEvaluatorC.ShowConf()
    print 'ranker indegree|boe|pr(not implemented yet)'
    InDegreeRankerC.ShowConf()
    BoeLmRankerC.ShowConf()
    sys.exit()

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
ch.setFormatter(formatter)



conf = cxConfC(sys.argv[1])   
QIn = conf.GetConf('in')
EvaOut = conf.GetConf('out')
RankerName = conf.GetConf('ranker')

Ranker = ChooseRanker(RankerName)(sys.argv[1])

Evaluator = RankerEvaluatorC(sys.argv[1])
Evaluator.Evaluate(QIn, Ranker.Rank, EvaOut)

