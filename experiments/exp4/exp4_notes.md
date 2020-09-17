
# Experiment 4

In this experiment we introduce other control algorithms and compare them to each other:

## Control algorithms

* First-Visit Monte Carlo
	* On-Policy
* Standard Q-Learning
	* Off-Policy
	* Updates occur after every step in every episode (online)
	* Parameter: Learning rate $\alpha \in \{0.1, 0.2, 0.3, 0.4\}$
* Reversed-Update Q-Learning (update at the 
	* Off-Policy
	* Updates occur at the end of every episode, and are applied chronologically reversed.
		* We hypothesize that this will propagate high-reward states faster to the start states than standard QL
	* Parameter: Learing rate $\alpha \in \{0.1, 0.2, 0.3, 0.4\}$

# Experiment 4
## Policies

* Exploring-starts q-table
* Exploring-starts q-table with planning on first visit of states

# Experiment 4a

Comparison of algorithms and policies in a 5-blocks world with an episode length limit of 20.

# Experiment 4a

![](./exp4a_04_plot_1.pdf)


# Experiment 4a

![](./exp4a_04_plot_2.pdf)


# Experiment 4a

![](./exp4a_04_plot_3.pdf)


# Experiment 4a

![](./exp4a_04_plot_4.pdf)


# Experiment 4a
## Observations


