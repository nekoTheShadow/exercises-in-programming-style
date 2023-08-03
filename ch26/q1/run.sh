#!/bin/bash

if [[ -f tf.db ]]; then
  rm -v tf.db
fi
bundle exec ruby q1.rb ../../pride-and-prejudice.txt