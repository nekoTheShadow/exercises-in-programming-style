#!/bin/bash

if [[ -f tf.db ]]; then
  rm -v tf.db
fi

python3 q2_1.py ../../pride-and-prejudice.txt
python3 q2_2.py 