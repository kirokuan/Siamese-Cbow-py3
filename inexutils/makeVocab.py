import collections
import codecs

import inexUtils

if __name__ == "__main__":
  import argparse
  oArgsParser = argparse.ArgumentParser(description='Bla bla')
  oArgsParser.add_argument('INEX_DIRECTORY')
  oArgsParser.add_argument('OUTPUT_FILE')
  oArgsParser.add_argument('-glob_pattern', metavar="GLOB_PATTERN",
                           dest='sGlobPattern',
                           help="A glob pattern, like '00*' for the first 10 directories. By default, all directories are considered ('*').",
                           action='store', default='*')
  oArgsParser.add_argument('-dont_lowercase', dest='bDontLowercase',
                           help="By default, all input text is lowercased. Use this option to prevent this.",
                           action='store_true')
  oArgsParser.add_argument("-d", dest="bDebug", action="store_true")
  oArgsParser.add_argument("-v", dest="bVerbose", action="store_true")
  oArgs = oArgsParser.parse_args()

  oSingleSentenceIterator = \
      inexUtils.InexIterator(oArgs.INEX_DIRECTORY, sName='ssIt',
                             sGlobPattern=oArgs.sGlobPattern,
                             bSingleSentence=True,
                             bVerbose=oArgs.bVerbose)

  oCounter = collections.Counter()

  # We assume the files are preprocessed with the -paragraph option
  for sSentence in oSingleSentenceIterator:
    oCounter.update(sSentence.split(' '))

  if oArgs.bVerbose:
    print "Storing to %s" % oArgs.sOutputFile
  fhOut = codecs.open(oArgs.OUTPUT_FILE, mode='w', encoding='utf8')
  for sKey, iFreq in oCounter.iteritems():
    fhOut.write("%s\t%d\n" % (sKey, iFreq))
  fhOut.close()
