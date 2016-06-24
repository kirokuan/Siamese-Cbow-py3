import os
import sys
import cPickle as pickle
import codecs
import gensim
import random
import numpy as np

import ppdbUtils
sys.path.append("../word2vec_scripts")
import stopWords

def generateOutputFileName(sOutputDir, sInputFile, bNoStopWords, iVectorSize):
  # We can't just chop off the extension as files can also be called
  # ppdb-1.0-s-phrasal
  sBasename = os.path.basename(sBasename)
  sBasename = sBasename[:-4] if sBasename.endswith(".txt") else sBasename
  sBasename = sBasename[:-3] if sBasename.endswith(".gz") else sBasename

  sStopWords = 'noStopWords' if bNoStopWords else 'withStopWords'

  return os.path.join(sOutputDir,
                      "%s.%dd.%s.txt" % (sBasename, iVectorSize, sStopWords))

def getIndices(fhOut, aTokens, oW2vModel, dStopWords):
  aPrintTokens = [] 
  aIndices = []

  for sToken in aTokens:
    if (dStopWords is not None) and (sToken in dStopWords):
      aPrintTokens.append("<stopWord>%s</stopWord>" % sToken)
    else:
      try:
        aIndices.append(oW2vModel.vocab[sToken].index)
        aPrintTokens.append(sToken)
      except KeyError:
        # Unknown word.  Don't do anything.
        aPrintTokens.append("<unknown>%s</unknown>" % sToken)

  return aIndices, aPrintTokens

def printEmbeddingIndices(sOutputFile, oMsrpc, oW2vModel, sW2vFile,
                          dStopWords):
  fhOut = codecs.open(sOutputFile, mode='w', encoding='utf8')
  fhOut.write("# %dd embeddings from %s\n" % (oW2vModel.vector_size, sW2vFile))
  iSentenceIndex = 0
  for dSentencePair in oMsrpc.yieldSentences():
    aIndices1, aPrintTokens1 = getIndices(fhOut, dSentencePair['aTokens1'],
                                          oW2vModel, dStopWords)
    aIndices2, aPrintTokens2 = getIndices(fhOut, dSentencePair['aTokens2'],
                                          oW2vModel, dStopWords)
    if (len(aIndices1) > 0) and (len(aIndices2) > 0):
      fhOut.write("%d %s # %s\n" % (dSentencePair['iLabel'],
                                    ' '.join(["%d" % x for x in aIndices1]),
                                    ' '.join(aPrintTokens1)))
      fhOut.write("%d %s # %s\n" % (dSentencePair['iLabel'],
                                    ' '.join(["%d" % x for x in aIndices2]),
                                    ' '.join(aPrintTokens2)))

  fhOut.close()

if __name__ == "__main__":
  import argparse
  oArgsParser = argparse.ArgumentParser(description='Convert every word in the input to its index in the word2vec model. Unknwon words are simply ignored')
  oArgsParser.add_argument('INPUT_FILE', help="PPDB paraphrase corpus file")
  oArgsParser.add_argument('OUTPUT_DIR',
                           help="Directory to store the output to")
  oArgsParser.add_argument('W2V_MODEL',
                           help="File path of a word2vec model file (has to in binary format).")
  oArgsParser.add_argument('-no_stop_words', dest='bNoStopWords',
                           help="Filter out stop words.", action="store_true")
  oArgsParser.add_argument('-d', dest="bDebug", help="Debugging mode",
                           action="store_true")
  oArgsParser.add_argument('-v', dest="bVerbose", help="Be verbose",
                           action="store_true")
  oArgs = oArgsParser.parse_args()

  if oArgs.bVerbose:
    print "Loading word2vec model"
  oW2vModel = \
      gensim.models.word2vec.Word2Vec.load_word2vec_format(oArgs.W2V_MODEL, \
                                                             binary=True)

  sOutputFile = \
      generateOutputFileName(oArgs.OUTPUT_DIR, oArgs.INPUT_FILE,
                             oArgs.bNoStopWords, oW2vModel.vector_size)


  if oArgs.bVerbose:
    print "Output file %s" % sOutputFile

  if oArgs.bVerbose:
    print "reading %s" % oArgs.INPUT_FILE
  oPPDB = ppdbUtils.ppdb(oArgs.INPUT_FILE)

  dStopWords = {}
  if oArgs.bNoStopWords:
    dStopWords = stopWords.dStopWords_nonVerbs

  if oArgs.bVerbose:
    print "Writing features to %s" % sOutputFile

  printEmbeddingIndices(sOutputFile, oPPDB, oW2vModel, oArgs.W2V_MODEL,
                        dStopWords)

  if oArgs.bVerbose:
    print "Closing"

    
