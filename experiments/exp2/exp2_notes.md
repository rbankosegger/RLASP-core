# Experiment 2

To compare the mean-based First-visit Monte-Carlo method from the bachelor's thesis with a gradient-based every-visit monte-carlo method.

# Experiment 2a
![](./exp2a_fig.pdf)

The original output (left) is too messy. Used running average to smooth the result and make it more readable (right).

# Experiment 2a
## Remarks
* The gradient-based algorithm at its best outperforms the mean-based algorithm.

	* This effect is caused by the difference between first-visit and every-visit Monte-Carlo methods, as can be shown when comparing a first-visit mean-based agent to a every-visit mean-based agent (which achieves similar performance as the gradient-based algorithm)

* There seems to be no significant difference in performance for $\alpha \in \{0.3, 0.03\}$
* However, there seems to be a decrease in performance for higher values ($\alpha \geq 0.8$)

# Experiment 2b
![](./exp2b_fig.pdf){width=100%}

The original output (left) is too messy. Used running average to smooth the result and make it more readable (right).

# Experiment 2b
## Remarks
* The low performance is disappointing, compared to the results of the bachelor's project (Experiment 1b, Comparison), where $pH=4$ achieves positive results for two of the four runs.
	* With such a low sample size ($n=4$), some randomness is expected. Maybe the result changes with larger sample sizes? 
	* The low sample size is chosen because the experiment was expensive to compute (~ 13 hours for $n=4$).

* The mean-based agent is equally bad. However, the mean-based agent worked fine in Experiment 1. This suggests that the result is not due to a programming error.

* Probably a good idea to repeat the experiment with a bigger planning horizon and more samples.

# Conclusions
* Overall, the gradient-based method seems to work well.
* In combination with planning, the results are ambigous and should be refined.
* Low sample sizes are a problem, but it takes very long to run trials with larger sample sizes.
