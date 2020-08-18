#!/bin/sh

python -m cProfile -o exp3a_profile_raw.txt exp3a_main.py 
python exp3_stats.py exp3a_profile_raw.txt > exp3a_profile.txt

python -m cProfile -o exp3b_profile_raw.txt exp3b_main.py 
python exp3_stats.py exp3b_profile_raw.txt > exp3b_profile.txt
