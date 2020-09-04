
# Experiment 3

This experiment is for profiling the framework and identifying possible bottlenecks.


# Experiment 3a

Tabula-rasa agent in a 7-blocks world, 150 episodes


\tiny
~~~ {#exp3a_profile.txt}
~~~

# Experiment 3b

Planning agent (on empty policy, ph=5) in a 7-blocks world, 150 episodes

\tiny
~~~ {#exp3b_profile.txt}
~~~

# Experiment 3

## Observations

* Let's compare these results to the last implementation:

	* The tabular rasa agents runtime decreased from $17.9s$ to $7.0s$ ($-60\%$)
	* The planning agent runtime decreased from $34.5s$ to $22.7s$ (-$34\%$)

* The tabula-rasa agent spent ~5s in transition to next states and ~1s iterating all 7-blocks world states.
* The planning agent spent ~5s in transition, ~1s iterating all states and ~15s planning.
