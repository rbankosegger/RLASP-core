
# Experiment 2

To compare the mean-based First-visit Monte-Carlo method from the bachelor's thesis with a gradient-based every-visit monte-carlo method.

# Experiment 2a
![](./exp2a_fig.pdf)

The original output (left) is too messy. Used running average to smooth the result and make it more readable (right).

# Experiment 2a
## Remarks
* There is no clear difference between the mean-based and the gradient-based algorithm at its best.
	* It may look like the gradient-based algorithm is better, but this is just a coincidence. Re-running the experiment may cause the mean-based algorithm to perform better.
	* *Note* Probably a good idea to re-run this experiment with a higher sample size.

* Both $\alpha=0.3$ and $\alpha=0.03$ seem to be good parameter choices.

* There seems to be a decrease in performance for higher values ($\alpha \geq 0.8$), which is expected.

# Experiment 2b
![](./exp2b_fig.pdf){width=100%}

The original output (left) is too messy. Used running average to smooth the result and make it more readable (right).

# Experiment 2b

* Planning still speeds up training, also for the gradient-based algorithm.
* There is no clear difference between the mean-based and gradient-based algorithms.

# Conclusions
* Overall, the gradient-based method seems to work as well as the mean-based method.
* The gradient-based method handles planning as well as the mean-based method.
