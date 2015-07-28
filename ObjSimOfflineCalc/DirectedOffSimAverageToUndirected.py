'''
Created on Jul 28, 2015 2:53:00 PM
@author: cx

what I do:
    average directed edge to undirected edge
what's my input:
    the pickle dict of directed sim result
what's my output:
    the pickle of averaged udirected edge

'''

import pickle,sys
if 3 != len(sys.argv):
    print 'directed sim pickle dict + out'
    sys.exit()
    
    
hDirect = pickle.load(open(sys.argv[1]))

hUnDirect = {}

for key,score in hDirect.items():
    a,b = key.split('\t')
    NewKey = '\t'.join(sorted([a,b]))
    if not NewKey in hUnDirect:
        TheOtherKey = b + '\t' + a
        TheOtherScore = 0
        if TheOtherKey in hDirect:
            TheOtherScore = hDirect[TheOtherKey]
        hUnDirect[NewKey] = (score + TheOtherScore) / 2.0
        
pickle.dump(hUnDirect,open(sys.argv[2],'w'))

print 'finished'
         
