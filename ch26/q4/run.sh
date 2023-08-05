#!/bin/bash

if [[ -f tf.db ]]; then
  rm -v tf.db
fi

python3 q3.py ../../pride-and-prejudice.txt  ../44534-0.txt
