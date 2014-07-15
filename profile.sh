#!/bin/bash

python -O -m cProfile -s 'cumulative' run.py > `date '+%Y%m%d-%H%M'`".prof"

exit 0
