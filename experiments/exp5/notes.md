
# Experiment 4

In this experiment we introduce and compare other control algorithms:

## Control algorithms

* First-Visit Monte Carlo
	* On-Policy
* Standard Q-Learning
	* Off-Policy
	* Updates occur after every step in every episode (online)
	* Parameter: Learning rate $\alpha \in \{0.1, 0.3, 0.6\}$
* Reversed-Update Q-Learning
	* Off-Policy
	* Updates occur at the end of every episode, and are applied chronologically reversed.
		* We hypothesize that this will propagate high-reward states faster to the start states than standard QL
	* Parameter: Learing rate $\alpha \in \{0.1, 0.3, 0.6\}$

# Experiment 4
## Target Policies

* Q-Table

## MDPs and Behavior Policies

* 5-Blocks world MDP
	* Q-Table, exploring starts
	* Q-Table, exploring starts, planning on first visit of new states

* Sokoban (suitcase-05-01)
	* Q-Table, $\epsilon$-greedy
	* Q-Table, $\epsilon$-greedy, planning on first visit of new states

# Experiment 4
## Setup: Target vs. Behavior policy

We generate every episode twice. We start with the given MDP in a random start state.
Based on this start state, we first generate an episode using the target policy and without learning.
Second, we reset the MDP to that start state and generate another episode using the behavior policy with learning.

Thus, the target policy return indicates how the agent would have performed for this episode with previous knowledge only.

# Experiment 4 - Results Blocks World
![](./exp4.5-Blocks World.1.pdf)

# Experiment 4 - Results Blocks World
![](./exp4.5-Blocks World.2.pdf)

# Experiment 4 - Results Blocks World
![](./exp4.5-Blocks World.3.pdf)

# Experiment 4 - Results Blocks World
![](./exp4.5-Blocks World.4.pdf)

# Experiment 4 - Results Blocks world
## Observations
* Both Q-Learning algorithms outperform First-Visit Monte Carlo
* Planning agents do better than non-planning agents
	* Consistent with previous results
* Higher learning rates do better
	* We believe that higher learning rates work especially well for the reversed-update QL agent since it makes positive rewards propagate further.
* The Reversed-Update Q-Learning drastically outperforms Standard Q-Learning in combination with the planner

# Experiment 4 - Results Blocks world
## Observations
* Behavior policy vs. target policy
	* For Monte-carlo there is no significant difference
		* Since MC is on-policy, both policies are the same, except for some random decisions
	* For Standard Q-Learning, the target policy lags behind the behavior policy
		* The target policy is expected to lag behind because it does not use the planer and because positive rewards need some time to propagate back to the start state.
	* For Reversed-Update Q-Learning, the target policy lags behind only for the planning agent.
		* The target policy does not use a planner, thus it is expected to lag behind first
		* Results are propagated back to the start state much faster, thus no lag for the tabula-rasa agent.
		

# Experiment 4 - Results Sokoban
![](./exp4.Sokoban (suitcase-05-01).1.pdf)

# Experiment 4 - Results Sokoban
![](./exp4.Sokoban (suitcase-05-01).2.pdf)

# Experiment 4 - Results Sokoban
![](./exp4.Sokoban (suitcase-05-01).3.pdf)

# Experiment 4 - Results Sokoban
![](./exp4.Sokoban (suitcase-05-01).4.pdf)

# Experiment 4 - Results Sokoban
## Observations
* For off-policy methods, the target policy converges. The behavior policy however does not converge.
	* Probably due to the influence of random actions within the behavior policy.
	* This shows the delicate nature of the sokoban problem. Most missteps are irreversible.
		* (on the other hand, $\epsilon=0.3$ might be too much randomness)
	* The Monte Carlo agent performs badly for the same reasons.
* Planning has a big impact on convergence time
* The reversed-update QL agent easily outperforms the standard QL agent.
	* Even without a planner, convergence happens much quicker.


# Experiment 4 - Conclusions
* In all scenarios, the reversed-update q-learning agent with help of a planner outperformed all others.

# Experiment 4 - Next steps
* Explore more difficult sokoban levels, see how far we can go.
* Experiment with dynamic learning rates
* Introduce generalization capability with state abstraction / tilings
