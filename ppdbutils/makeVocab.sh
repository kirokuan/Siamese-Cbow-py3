#!/bin/sh

if [ -z "$1" ]; then
    echo
    echo " USAGE: $0 PPDB_FILE"
    echo
    echo " This script reads a PPDB file, and outputs a vocabulary file"
    echo " suitable to be used by Siamese CBOW".
    echo
    echo " Output is to stdout"
    echo
    exit
fi

PPDB_FILE=$1

python ppdbUtils.py -single_sentence $1 | cut -f2 | tr ' ' '\n' | sort | uniq -c | sort -nr 
