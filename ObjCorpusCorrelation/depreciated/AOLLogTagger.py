'''
Created on Feb 12, 2015 1:34:35 PM
@author: cx

what I do:
I tag all AOL query log...
Hope not too bad for TagMe API requrest
what's my input:
AOL q log + wiki->obj id dump
what's my output:
tagged AOL q log
    add to each line of AOL q log, with # as separator: Objid\tobjname\tscore\t

'''
'''
not in use
will use their code to do it.
web APi won't allow
'''

import site
# from CandidateGeneration import FbCandidateGenerator
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/SemanticSearch')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
import json
from TagMeAPI.TagMeAPIBase import TagMeAPIBaseC
from FreebaseDump.FbObjWikiMatch import FbObjWikiMatchC
import math
from time import sleep

from cxBase.Conf import cxConfC
def TagOneLine(line,Tagger, FbMatcher):
    if 'AnonID' == line[:6]:
        return ""
    query = line.split('\t')[1]
    if ('www' == query[:3]) | ('edu' == query[-3:]) | ('com' == query[-3:]):
        #skip url query
        return line
    lhAna = Tagger.TagText(query)
    TaggedRes = ""
    for hAna in lhAna:
            WikiTitle = hAna['title']
            WikiUrl = 'http://en.wikipedia.org/wiki/%s' %(WikiTitle.replace(' ','_'))
            lObjId = FbMatcher.MatchWikiToObj(WikiUrl)
            if [] == lObjId:
                continue
            ObjId = lObjId[0]
            TaggedRes += ObjId + '\t' + WikiTitle + '\t' + str(hAna['rho']) + '\t'
            
    if "" != TaggedRes:
        line += '\t#\t' + TaggedRes.strip()
    return line

import sys

if 2 != len(sys.argv):
    FbObjWikiMatchC.ShowConf()
    print "in\nout"
    sys.exit()
    
Tagger = TagMeAPIBaseC()
FbMatcher = FbObjWikiMatchC(sys.argv[1])
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')
out = open(OutName,'w')

cnt = 0
TaggedCnt = 0
for line in open(InName):
    line = TagOneLine(line.strip(), Tagger, FbMatcher)
    if "" != line:
        print >> out, line
    sleep(0.01)
    if '#' in line:
        TaggedCnt += 1
    cnt += 1
    if 0 == (cnt % 10000):
        print 'processed [%d] line [%d] tagged' %(cnt,TaggedCnt)
        
print 'finished [%d/%d]' %(TaggedCnt,cnt)
 

