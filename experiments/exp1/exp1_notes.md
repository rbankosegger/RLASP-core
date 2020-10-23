# Experiment 1

To reproduce the results from the bachelor's thesis

# Experiment 1a
![](exp1a_fig.pdf)

# Experiment 1a
## Remarks
* Results are as expected. 
* Bigger blocks worlds need much more episodes to train.

# Experiment 1b
![](exp1b_fig.pdf)

# Experiment 1b
## Remarks
* Adding a planning component clearly speeds up training.
* Already small planning horizons cause significant increase in training speed (compared to the previous experiment).
* Bigger planning horizons speed up training even more. 


# Experiment 1c
![](exp1c_fig.pdf)

The original output (left) is too messy. Used running average to smooth the result and make it more readable (right).

# Experiment 1c
## Remarks
* Planning at random times speeds up training as well.
* However, even with near-perfect planning horizons, planning at random times is not as effective as planning for new states.
	* ...except when `planning_factor=1.0`, i.e. when the planner is used at every timestep - too expensive!

# Experiment 1 - Conclusions
* Overall, the results seem to be in line with that of the bachelor's thesis.
* Planning clearly improves the training process.
