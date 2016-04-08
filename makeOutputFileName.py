import siamese_cbowUtils as scbowUtils
import os

if __name__ == "__main__":
  ''' This is a very simple helper script that can be called from a bash script
      to get an output file name for a call to siamese-cbow.
  '''
  oArgs = scbowUtils.parseArguments()

  # The second two options are guesses. It might be that the vocabulary is 
  # in fact smaller than iMaxNrOfVocabWords.
  sOutputFile = scbowUtils_el.makeOutputFileName(oArgs,
                                                 oArgs.iMaxNrOfVocabWords,
                                                 oArgs.iEmbeddingSize)

  print os.path.basename(sOutputFile.replace(".pickle", ''))
