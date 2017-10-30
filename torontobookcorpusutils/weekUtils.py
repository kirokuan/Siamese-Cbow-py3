'''
Copyright 2016 Tom Kenter

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.
'''

import codecs
import os
import _pickle as cPickle
import numpy as np
from functools import reduce

class weekUtils:
  def __init__(self, sCorpusDir=None, sSentencePositionsDir=None, 
               sName=None, bVerbose=False,wk=1):
    self.bVerbose = bVerbose
    self.sName = sName
    aFiles = [ "week%i.txt" % i  for i in range(1,int(wk))]
    self.aFiles = []
    self.iTotalNrOfSentences = 0

    for sFile in aFiles:
      sPickleFile = os.path.join(sSentencePositionsDir, "%s.pickle" % sFile)
      if self.bVerbose:
        print("Loading %s" % sPickleFile)

      fhSentencePositions = open(sPickleFile, mode='rb')
      npaSentencePositions = cPickle.load(fhSentencePositions)
      fhSentencePositions.close()

      sFileName = os.path.join(sCorpusDir, sFile)
      self.aFiles.append({"sFileName": sFileName,
                          "fhFile": \
                            codecs.open(sFileName, mode="r", encoding="utf8"),
                          "npaSentencePositions": npaSentencePositions,
                          "npaIndicesForTuples": \
                            np.array(range(npaSentencePositions.shape[0])),
                          "npaIndicesForRandom": \
                            np.array(range(npaSentencePositions.shape[0])),
                          "iYieldedTuple": 0,
                          "iYieldedRandom": 0
                          })

      self.iTotalNrOfSentences += npaSentencePositions.shape[0]

    self.aNonTokens = ['.', "''", '``', ',', ':', ';', '?', '!', '-', '_']

  def __iter__(self): # Simple wrapper
    for t in self.yieldTuple():
      yield t

  def yieldSentence(self):
    # NOTE that we (ab)use the random indices, which were not shuffled yet
    for iFileIndex in range(len(self.aFiles)):
      # Get the next index for the sentence position array
      for iSentencePosition in self.aFiles[iFileIndex]["npaSentencePositions"]:
        # Go to that position in the file
        self.aFiles[iFileIndex]["fhFile"].seek(iSentencePosition)
        # Read the sentence
        yield self.toTokens(self.aFiles[iFileIndex]["fhFile"].readline())

  def yieldRandomSentence(self):
    '''
    NOTE that this iterator will yield FOREVER
    '''
    # Every time this iterator is started, we shuffle
    for i in range(len(self.aFiles)):
      np.random.shuffle(self.aFiles[i]["npaIndicesForRandom"])
   
    #np.random.shuffle(self.aFiles[1]["npaIndicesForRandom"])

    # And we reset
    for i in range(len(self.aFiles)):
      self.aFiles[i]["iYieldedRandom"] = 0
   
    #self.aFiles[1]["iYieldedRandom"] = 0

    while(1):
      iFileIndex = np.random.randint(0,len(self.aFiles)) # Choose file 0 or 1
      
      # If we yielded as many indices as there are, shuffle again
      if self.aFiles[iFileIndex]["iYieldedRandom"] == \
            self.aFiles[iFileIndex]["npaIndicesForRandom"].shape[0]:
        np.random.shuffle(self.aFiles[iFileIndex]["npaIndicesForRandom"])
        self.aFiles[iFileIndex]["iYieldedRandom"] = 0
      
      # Get a random index for the sentence position array
      iSentencePositionIndex = \
          self.aFiles[iFileIndex]["npaIndicesForRandom"][self.aFiles[iFileIndex]["iYieldedRandom"]]
      # Get the position where the sentence starts
      iSentencePosition = self.aFiles[iFileIndex]["npaSentencePositions"][iSentencePositionIndex]
      # Go to that position in the file
      self.aFiles[iFileIndex]["fhFile"].seek(iSentencePosition)
      # Read the sentence
      yield self.toTokens(self.aFiles[iFileIndex]["fhFile"].readline())

      self.aFiles[iFileIndex]["iYieldedRandom"] += 1

  def yieldTuple(self):
    '''
    This yields a random tuple, until all tuples are yielded
    '''
    # Every time this iterator is started, we shuffle
    for i in range(len(self.aFiles)):
      np.random.shuffle(self.aFiles[0]["npaIndicesForTuples"])
 
    #np.random.shuffle(self.aFiles[1]["npaIndicesForTuples"])

    # And we reset
    for i in range(len(self.aFiles)):
      self.aFiles[i]["iYieldedTuple"] = 0
    #self.aFiles[1]["iYieldedTuple"] = 0
    
    
    while( reduce((lambda x,y: x or y),map((lambda x:x['iYieldedTuple']<x['npaIndicesForTuples'].shape[0]),self.aFiles))
 #  (self.aFiles[0]["iYieldedTuple"] < \
 #            self.aFiles[0]["npaIndicesForTuples"].shape[0]) \
 #	or       (self.aFiles[1]["iYieldedTuple"] < 
 #             self.aFiles[1]["npaIndicesForTuples"].shape[0])
     ):
     # iFileIndex=0
      #i=0
      #while i<len(self.aFiles) and self.aFiles[i]["iYieldedTuple"] >=self.aFiles[i]["npaIndicesForTuples"].shape[0]:
      #  if self.bVerbose:
      #    print("i shape:%i" % self.aFiles[i]["iYieldedTuple"])
      #    print("shape: %i" % self.aFiles[i]["npaIndicesForTuples"].shape[0])
      #  i+=1
      #if self.bVerbose:
      #  print("i is %i" % i)
      #iFileIndex =i
      #if iFileIndex==len(self.aFiles) and self.aFiles[i-1]["iYieldedTuple"] >= \
      #      self.aFiles[i-1]["npaIndicesForTuples"].shape[0]:
      #  iFileIndex = 0
      #elif iFileIndex==len(self.aFiles): # We haven't reached the end for any of the two
      iFileIndex = np.random.randint(0,len(self.aFiles)) # Choose file 0 or 1
      while self.aFiles[iFileIndex]["iYieldedTuple"]>= self.aFiles[iFileIndex]["npaIndicesForTuples"].shape[0]:
        iFileIndex=np.random.randint(0,len(self.aFiles))
      #iFileIndex=0
      if self.bVerbose:
        print("iFileIndex:%i" % iFileIndex)
      #print(str(len(self.aFiles)))     
      # Get a random position in the sentence position array
      # We don't want the very first or last sentence
      bDone = False
      iSentencePositionIndex = 0
      while (iSentencePositionIndex == 0) or \
            (iSentencePositionIndex == \
               (self.aFiles[iFileIndex]["npaIndicesForTuples"].shape[0] - 1)):
        if self.aFiles[iFileIndex]["iYieldedTuple"] == \
              self.aFiles[iFileIndex]["npaIndicesForTuples"].shape[0]:
          bDone = True
          break

        iSentencePositionIndex = \
            self.aFiles[iFileIndex]["npaIndicesForTuples"][self.aFiles[iFileIndex]["iYieldedTuple"]]
        self.aFiles[iFileIndex]["iYieldedTuple"] += 1

      if bDone:
        continue

      # Get the position of the sentence BEFORE it
      iSentencePosition = self.aFiles[iFileIndex]["npaSentencePositions"][iSentencePositionIndex-1]
      # Go to that position
      self.aFiles[iFileIndex]["fhFile"].seek(iSentencePosition)
      # Read three sentences
      aSentence_n_min_1 = \
          self.toTokens(self.aFiles[iFileIndex]["fhFile"].readline())
      aSentence_n = self.toTokens(self.aFiles[iFileIndex]["fhFile"].readline())
      aSentence_n_plus_1 = \
          self.toTokens(self.aFiles[iFileIndex]["fhFile"].readline())

      # Yield the tuple, sentence n first
      yield (aSentence_n, aSentence_n_min_1, aSentence_n_plus_1)

  def toTokens(self, sLine):
    return [x for x in sLine.strip().split(' ') if x not in self.aNonTokens]

# You can use the bit below to test something
if __name__ == "__main__":
  import argparse
  oArgsParser = \
      argparse.ArgumentParser(description='Toronto Book Corpus utils')
  oArgsParser.add_argument("TORONTO_BOOK_CORPUS_DIR")
  oArgsParser.add_argument("TORONTO_BOOK_CORPUS_SENTENCE_POSITIONS_DIR")
  oArgsParser.add_argument("-r", dest="bRandom", action="store_true")
  oArgsParser.add_argument("-d", dest="bDebug", action="store_true")
  oArgsParser.add_argument("-v", dest="bVerbose", action="store_true")
  oArgs = oArgsParser.parse_args()

  if oArgs.bDebug:
    import pdb
    pdb.set_trace()

  oToBoCo = \
    torontoBookCorpusIterator(oArgs.TORONTO_BOOK_CORPUS_DIR,
                              oArgs.TORONTO_BOOK_CORPUS_SENTENCE_POSITIONS_DIR,
                              bVerbose=oArgs.bVerbose)

  i = 0
  if oArgs.bRandom:
    for s in oToBoCo.yieldRandomSentence():
      print(' '.join(s))
      i += 1
      if i == 10:
        break
  else:
    funcRandomIterator = oToBoCo.yieldRandomSentence()

    for t in oToBoCo.yieldTuple():
      aRandomTokens1 = next(funcRandomIterator)
      aRandomTokens2 = next(funcRandomIterator)

      print("s  : %s\ns-1: %s\ns+1: %s\nr1 : %s\nr2 : %s\n" % (' '.join(t[0]),
                                        ' '.join(t[1]),
                                        ' '.join(t[2]),
                                        ' '.join(aRandomTokens1),
                                        ' '.join(aRandomTokens2) ))


