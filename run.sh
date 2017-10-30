#!/bin/bash

#THEANO_FLAGS=device=gpu0
python3 siamese-cbow.py -v -share_weights -vocab ppdbVocabFile.txt -epochs 3 -neg 2 -embedding_size 100 /tmp2/yckuan/data/ppdb-1.0-xl-phrasal output

