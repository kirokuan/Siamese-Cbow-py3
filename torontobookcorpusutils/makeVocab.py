import codecs
import collections

if __name__ == "__main__":
  import argparse
  oArgsParser = argparse.ArgumentParser(description='Make a vocabulary of a Toronto Book Corpus file')
  oArgsParser.add_argument("TORONTO_BOOK_CORPUS_FILE")
  oArgsParser.add_argument("-d", dest="bDebug", action="store_true")
  oArgsParser.add_argument("-v", dest="bVerbose", action="store_true")
  oArgs = oArgsParser.parse_args()

  aNonTokens = ['.', "''", '``', ',', ':', ';', '?', '!', '-', '_']

  oCounter = collections.Counter()

  fhFile = codecs.open(oArgs.TORONTO_BOOK_CORPUS_FILE,
                       mode="r", encoding="utf8")
  for sLine in fhFile:
    aTokens = [x for x in sLine.strip().split(' ') if x not in aNonTokens]

    oCounter.update(aTokens)

  fhFile.close()
    
  for sWord, iFreq in oCounter.iteritems():
    print "%d\t%s" % (iFreq, sWord)
