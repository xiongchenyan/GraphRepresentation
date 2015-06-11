'''
Created on Feb 23, 2015 4:31:30 PM
@author: cx

what I do:
submit jobs for each annotation doc
    run EntityCorrelationPerDoc basically
what's my input:
    Annotation dir
    out dir
    targe id in
    input type
what's my output:
submit jobs for each file in annotation dir

'''


import ntpath
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/SemanticSearch')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/Geektools')

from condor.SimpleJobSubmitter import SimpleJobSubmitter
import subprocess
from cxBase.Conf import cxConfC
from cxBase.WalkDirectory import WalkDir
import sys



def Process(InDir,OutDir,TargetIdName,InType):
    
    lFName = WalkDir(InDir)
    llCmd = []
    for fname in lFName:
        lCmd = ['qsub','python','EntityCorrelationPerDoc.py',fname,OutDir,TargetIdName,InType]
        llCmd.append(lCmd)
    SimpleJobSubmitter(llCmd, MaxJob=100)
    
    print 'all finished'
    return True



if 2 != len(sys.argv):
    print "conf:\nindir\noutdir\ntype facc|fakba\ntargetobj (if needed)"
    sys.exit()
    
conf = cxConfC(sys.argv[1])
InDir = conf.GetConf('indir')
OutDir = conf.GetConf('outdir')
InType = conf.GetConf('type')
TargetIdName = conf.GetConf('targetobj')
    
Process(InDir, OutDir, TargetIdName, InType)
