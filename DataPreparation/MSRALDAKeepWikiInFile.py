'''
Created on Sep 16, 2015 11:48:00 AM
@author: cx

what I do:
    I only keep those wikipedia lines
what's my input:
    in file + DocNo-url mapping file + output
what's my output:
    in file's wiki lines
    

'''

import sys

if 4 != len(sys.argv):
    print 'I filter out non-wiki lines'
    print 'indata + mapping data + output'
    sys.exit()
    
    
lvCol = [line.split('\t') for line in open(sys.argv[2]).read().splitlines() if line.startswith('clueweb09-enwp')]
hUrlDocNo = dict([[vCol[1],vCol[0]] for vCol in lvCol if len(vCol) >= 2])

print 'target [%d] doc' %(len(hUrlDocNo))
out = open(sys.argv[3],'w')
FindCnt = 0
for cnt,line in enumerate(open(sys.argv[1])):
    vCol = line.strip().split('\t')
    if len(vCol) < 3:
        continue
    Url = vCol[0]
    text = vCol[1]
    if Url in hUrlDocNo:
        print >> out,Url + '\t' + hUrlDocNo[Url] + '\t' + text
        FindCnt += 1
    if (cnt % 10000) == 0:
        print 'find [%d] in [%d] lines' %(FindCnt,cnt)
        
out.close()
print 'finished [%d/%d] find' %(FindCnt,len(hUrlDocNo))