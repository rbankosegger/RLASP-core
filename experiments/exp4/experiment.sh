#!/bin/bash

export PATH
. env/bin/activate 

cd src
python main.py $@
mv experiment.csv ../
cd ..
