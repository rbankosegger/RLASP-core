# RLASP
This program combines reinforcement learning (RL) with answer set programming (ASP) to evaluate policies for solving blocks world problems.

## Install and use for development

I would recommend setting up a virtual environment to work with.

To install:

	python -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt	
	deactivate
	
Before starting a development session:

	source .venv/bin/activate
	
To run the core functions:

	python -m src.train --db_file=test.csv blocksworld
	python -m src.plot test.csv
	
After the development session:

	deactivate
	
## Install and use for experiments (e.g. on a server)

Again, I would suggest creating a new virtual environment.
This time, we can install everything directly from the github source!
	
	python -m venv env-rlasp
	source env-rlasp/bin/activate
	pip install git+https://github.com/rbankosegger/RLASP-core.git
	deactivate
	
After install, as long as `env-rlasp` is activated, you will have access to binaries that can be directly executed or embedded into a `.sh` file.

	rlasp-train --db_file=test.csv blocksworld
	rlasp-plot test.csv

You can also look at all the available options for training by executing

	rlasp-train -h
	

## Reference

 * [potassco](https://potassco.org)
 * [clingo_python_api](https://potassco.org/clingo/#packages)
 * [Gym](http://gym.openai.com/)
 * [Gym Minigrid](https://github.com/maximecb/gym-minigrid)
 * [Elias' Bachelor's thesis (2020)](https://fuxgeist.com/thesis.pdf)
