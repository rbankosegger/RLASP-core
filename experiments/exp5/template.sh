#!/bin/bash

export PATH
. ~/miniconda3/bin/activate rlasp 

cd src
python main.py {args_imported_by_python}
mv *.csv ../
cd ..
