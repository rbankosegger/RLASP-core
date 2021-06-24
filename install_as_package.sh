#!/bin/sh

conda install pip
conda install -c conda-forge gym
conda install -c potassco clingo

pip install build
pip install gym-minigrid

python -m build
python -m pip install . 
