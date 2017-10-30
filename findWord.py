# coding=utf-8
import wordEmbeddings as we
import sys

filename= sys.argv[1]
PPDB = we.wordEmbeddings(filename)
word = sys.argv[2]
word2 = sys.argv[3]
#xx=PPDB.dump()

#for i in xx:
#  print(xx)

for i,j in PPDB.most_similar(word):
  print(i) 
  print(j) 

print(PPDB.sentence_similarity(word,word2))

print()
