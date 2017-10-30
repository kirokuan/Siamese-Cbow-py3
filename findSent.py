# coding=utf-8
import wordEmbeddings as we
import sys
import re

filename= sys.argv[1]
PPDB = we.wordEmbeddings(filename)
sent = re.split('\s+',sys.argv[2])


print(PPDB.getAggregate(sent))

print("")
