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
from PageRankRanker import PageRankRankerC
from BoeLanguageModel.BoeLmRanker import BoeLmRankerC


def ChooseRanker(RankerName):
    if RankerName == 'boe':
        return BoeLmRankerC
    if RankerName == 'indegree':
        return InDegreeRankerC
    if RankerName == 'pr':
        return PageRankRankerC
    
    logging.error('[%s] not implemented',RankerName)
    raise NotImplementedError
    


if 2 != len(sys.argv):
    print 'I evaluate graph ranking'
    print 'in\nout'
    RankerEvaluatorC.ShowConf()
    print 'ranker indegree|boe|pr'
    InDegreeRankerC.ShowConf()
    BoeLmRankerC.ShowConf()
    PageRankRankerC.ShowConf()
    sys.exit()

conf = cxConfC(sys.argv[1])  


LogLevel = logging.INFO
if conf.GetConf('loglevel') == 'debug':
    LogLevel = logging.DEBUG
root = logging.getLogger()
root.setLevel(LogLevel)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(LogLevel)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)         



 
QIn = conf.GetConf('in')
EvaOut = conf.GetConf('out')
RankerName = conf.GetConf('ranker')

Ranker = ChooseRanker(RankerName)(sys.argv[1])

Evaluator = RankerEvaluatorC(sys.argv[1])
Evaluator.Evaluate(QIn, Ranker.Rank, EvaOut)

