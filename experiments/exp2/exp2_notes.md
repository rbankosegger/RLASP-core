# Experiment 2

To compare the mean-based First-visit Monte-Carlo method from the bachelor's thesis with a gradient-based every-visit monte-carlo method.

## Note

Switched to plotting return instead of return ratio due to performance reasons.

# Experiment 2a
![](./exp2a_fig.pdf)

The original output (left) is too messy. Used running average to smooth the result and make it more readable (right).

# Experiment 2a
## Remarks
* There are subtle differences between the mean-based and the gradient-based algorithm at its best.

* I expected to see an accelerating effect when switching from first-visit MC to every-visit MC, but this seems not to be the case.

* Both $\alpha=0.3$ and $\alpha=0.03$ are doing well.

	* Both show similar progress in the first 1000 episodes.

	* Towards the end, $\alpha=0.3$ gets worse again, which may indicate that $\alpha$ is too large to capture the subtleties needed to improve further.

* However, there seems to be a decrease in performance for higher values ($\alpha \geq 0.8$), which is expected.

# Experiment 2b
![](./exp2b_fig.pdf){width=100%}

The original output (left) is too messy. Used running average to smooth the result and make it more readable (right).

# Experiment 2b
## Remarks
* The low performance is disappointing, compared to the results of the bachelor's project (Experiment 1b, Comparison), where $pH=5$ almost immediately achieves satisfactory results.

* Despite that, learning is clearly happening and the results are in line with thoe of Experiment 1b.

* There is no clear difference between the mean-based and gradient-based algorithms.


# Conclusions
* Overall, the gradient-based method seems to work as well as the mean-based method.
* The gradient-based method handles planning as well as the mean-based method.
