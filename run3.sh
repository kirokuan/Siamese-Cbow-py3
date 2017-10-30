#!/bin/bash

#source py3/bin/activate
path="/tmp2/yckuan/data/textOnly/"
vocab="/tmp2/yckuan/data/vocab/"
finalVocab="/tmp2/yckuan/weeks.small.vocab.txt"
mkdir -p $vocab
cd torontobookcorpusutils
wk=52
rm -rf $vocab
mkdir $vocab
for((i=1;i<$wk;i++))
do
   x="$path/week$i.txt"
   vocabFile="$vocab/week$i.vocab.txt"
   python3 file2positions.py $x $path
   python3 makeVocab.py $x >  $vocabFile

done
echo "combine vocab"
cd ../inexutils
python3 combineVocabs.py $vocab $finalVocab
cd ..
echo $wk

python3 siamese-cbow.py -v -share_weights -vocab $finalVocab -wk $wk -epochs 5 -neg 2 -embedding_size 100 $path /tmp2/yckuan/output/

