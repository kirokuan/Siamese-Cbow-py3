import sys

import pickle
import cPickle

filename=sys.argv[0]
dDict={}
with open(filename,mode='rb')  as f:
  f.seek(0)
  dDict=pickle.load(f)

  print(dDict)
