PARENT_ID=$$

if [ -z "$3" ]; then
    echo
    echo " USAGE: $0 NR_OF_PROCESSES PRE_PROCESSED_INEX_DIRECTORY OUTPUT_DIR"
    echo
    exit
fi

NR_OF_PROCESSES=$1
PRE_PROCESSED_INEX_DIRECTORY=$2
OUTPUT_DIR=$3

for I in $(seq 0 9); do
    for J in $(seq 0 9); do
        for K in $(seq 0 9); do
            OUTPUT_FILE=$OUTPUT_DIR/$I$J$K.vocab.txt

            echo "Doing $I$J$K -> $OUTPUT_FILE"
            python countWords.py -glob_pattern $I$J$K $PRE_PROCESSED_INEX_DIRECTORY $OUTPUT_FILE &
            
            NUM_CHILDREN=$(pgrep -P $PARENT_ID | wc -l)
            while [ $NUM_CHILDREN -ge $NR_OF_PROCESSES ]; do
                sleep 0.1
                NUM_CHILDREN=$(($(pgrep -P $PARENT_ID | wc -l) - 1))
            done
        done
    done
done

wait