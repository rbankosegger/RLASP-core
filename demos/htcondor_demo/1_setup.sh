#!/bin/bash

python -m venv env-rlasp
source env-rlasp/bin/activate
pip install git+https://github.com/rbankosegger/RLASP-core.git
deactivate

# Generate scripts
python 1a_generate_scripts.py

# For every batch
for dir in htcondor_workspace/*/; do

	# Make generated scripts executable
	chmod +x $dir/*.sh

	# Copy submitfile 
	cp 1b_submitfile.sub $dir/submitfile.sub

	# Copy python environment
	cp -r env-rlasp $dir/env-rlasp

done
