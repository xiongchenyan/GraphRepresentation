'''
Created on Jul 23, 2015 11:10:24 AM
@author: cx

what I do:
    quick fix the bugged data format
what's my input:
    dir
what's my output:
    overwrite the dir

'''



import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.WalkDirectory import WalkDir
import sys

def FixOneFile(FName):
    lLines = open(FName).read().splitlines()
    
    for i in range(len(lLines)):
        vCol = lLines[i].split('\t')
        if len(vCol) == 3:
            continue
        
        vCol[1].replace('{','\t{')
        lLines[i] = '\t'.join(vCol)
    
    out = open(FName,'w')
    print >> out,'\n'.join(lLines)
    
    
    
lFName = WalkDir(sys.argv[1])

for FName in lFName:
    FixOneFile(FName)
    
print 'finished'

    
