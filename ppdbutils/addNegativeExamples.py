import os
import codecs
import numpy as np

# The file comes as:
# label_s_1_1 idx1 idx2 idx3 # Comment
# label_s_1_2 idx1 idx2 idx3 # Comment
# label_s_2_1 idx1 idx2 idx3 # Comment
# label_s_1_2 idx1 idx2 idx3 # Comment
#
def readFile(sFile):
  aLabels, aWordEmbeddingIndices, aComments = [], [], []

  fhFile = codecs.open(sFile, mode='r', encoding='utf8')
  for sLine in fhFile:
    if sLine.startswith('#'):
      continue

    sFirstPart, sComment = sLine.strip().split(' # ')
    aFirstPart = sFirstPart.split(' ')

    aLabels.append(aFirstPart[0])
    aWordEmbeddingIndices.append(' '.join(aFirstPart[1:]))
    aComments.append(sComment)

  fhFile.close()

  return aLabels, aWordEmbeddingIndices, aComments

def printLine(fhOut, sLabel, sWordEmbeddingIndices, sComment):
  fhOut.write("%s %s # %s\n" % (sLabel, sWordEmbeddingIndices, sComment))

def writeFeatures(sInputFile, aLabels, aWordEmbeddingIndices, aComments,
                  sOutputFile, iNeg):
  npaRandomIndices = np.arange(len(aLabels))
  np.random.shuffle(npaRandomIndices)
  iRandIndex = 0

  fhOut = codecs.open(sOutputFile, mode='w', encoding='utf8')
  fhOut.write("# Generated from %s\n" % sInputFile)

  for i in range(0, len(aLabels), 2):
    # First, print the genuine example
    printLine(fhOut, aLabels[i], aWordEmbeddingIndices[i], aComments[i])
    printLine(fhOut, aLabels[i+1], aWordEmbeddingIndices[i+1], aComments[i+1])

    # Now, print some random examples
    for j in range(iNeg):
      printLine(fhOut, "0", aWordEmbeddingIndices[i], aComments[i])
      printLine(fhOut, "0",
                aWordEmbeddingIndices[npaRandomIndices[iRandIndex]],
                aComments[npaRandomIndices[iRandIndex]])

      iRandIndex += 1
      if iRandIndex == npaRandomIndices.shape[0]:
        # If we reached the end, reshuffle and start again
        np.random.shuffle(npaRandomIndices)
        iRandIndex = 0

  fhOut.close()

def generateOutputFileName(sOutputDir, sInputFile, iNeg):
  # We can't just chop off the extension as files can also be called
  # ppdb-1.0-s-phrasal
  sBasename = os.path.basename(sInputFile)
  sBasename = sBasename[:-4] if sBasename.endswith(".txt") else sBasename

  return os.path.join(sOutputDir, "%s.neg_%d.txt" % (sBasename, iNeg))

if __name__ == "__main__":
  import argparse
  oArgsParser = argparse.ArgumentParser(description='Add random examples to an all positive training set')
  oArgsParser.add_argument('INPUT_FILE', help="PPDB feature file")
  oArgsParser.add_argument('OUTPUT_DIR',
                           help="Directory to store the output to")
  oArgsParser.add_argument('-neg', dest='iNeg', metavar='INT',
                           help="Number of negative examples",
                           action="store", type=int, required=True)
  oArgsParser.add_argument('-d', dest="bDebug", help="Debugging mode",
                           action="store_true")
  oArgsParser.add_argument('-v', dest="bVerbose", help="Be verbose",
                           action="store_true")
  oArgs = oArgsParser.parse_args()

  sOutputFile = \
      generateOutputFileName(oArgs.OUTPUT_DIR, oArgs.INPUT_FILE, oArgs.iNeg)

  if oArgs.bVerbose:
    print "reading %s" % oArgs.INPUT_FILE
  aLabels, aWordEmbeddingIndices, aComments = readFile(oArgs.INPUT_FILE)

  if oArgs.bVerbose:
    print "Writing features to %s" % sOutputFile

  writeFeatures(oArgs.INPUT_FILE, aLabels, aWordEmbeddingIndices, aComments,
                sOutputFile, oArgs.iNeg)

  if oArgs.bVerbose:
    print "Closing"
