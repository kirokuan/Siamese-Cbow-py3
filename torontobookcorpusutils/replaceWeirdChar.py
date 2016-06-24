import codecs
import sys

if __name__ == "__main__":
  import argparse
  oArgsParser = argparse.ArgumentParser(description='Get rid of some weird characters which are irrelevant, but that do mess things up.')
  oArgsParser.add_argument("TORONTO_BOOK_CORPUS_FILE")
  oArgs = oArgsParser.parse_args()
  
  fhFile = codecs.open(oArgs.TORONTO_BOOK_CORPUS_FILE,
                       mode="r", encoding="utf8")
  sFile = fhFile.read()
  fhFile.close()

  # The next two characters cause newlines to be entered
  sFile = sFile.replace(u"\x1c", '')
  sFile = sFile.replace(u"\x1d", '')
  # Single quotes
  sFile = sFile.replace(u"\x19", " '")
  sFile = sFile.replace(u"\x18", "' ")

  sys.stdout.write(sFile)
