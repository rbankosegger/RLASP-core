# Experiment 3

The previous experiments took very long to complete. This experiment is for profiling the framework and identifying possible bottlenecks.

* **Update:** This experiment helped me to find redundant ASP-calls (my own fault) and increase performance 5-fold. The results below are provided with the current (improved) version of the code.

# Experiment 3a

Tabula-rasa agent in a 7-blocks world, 150 episodes

\tiny
	Wed Aug 19 10:43:36 2020    exp3a_profile_raw.txt
	
	         3637651 function calls (3629949 primitive calls) in 17.924 seconds
	
	   Ordered by: internal time
	   List reduced from 2714 to 20 due to restriction <20>
	
	   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
	     4057    9.820    0.002    9.820    0.002 {method 'ground' of 'clingo.Control' objects}
	     4057    2.046    0.001    2.046    0.001 {method 'load' of 'clingo.Control' objects}
	     4057    1.212    0.000    1.458    0.000 {method 'solve' of 'clingo.Control' objects}
	     4056    1.197    0.000   15.918    0.004 BlocksWorld.py:107(next_step)
	    14419    0.882    0.000    0.882    0.000 {method 'add' of 'clingo.Control' objects}
	   160104    0.450    0.000    0.530    0.000 BlocksWorld.py:160(parse_part_state)
	     4057    0.415    0.000    0.415    0.000 ClingoBridge.py:6(__init__)
	    41689    0.220    0.000    0.220    0.000 {method 'symbols' of 'clingo.Model' objects}
	    18816    0.177    0.000    0.758    0.000 BlocksWorld.py:185(parse_state)
	    53872    0.108    0.000    0.144    0.000 entities.py:53(<listcomp>)
	    37233    0.097    0.000    0.122    0.000 BlocksWorld.py:173(parse_action)
	   686190    0.097    0.000    0.097    0.000 entities.py:8(__eq__)
	        1    0.081    0.081    1.152    1.152 BlocksWorld.py:42(generate_all_states)
	   160111    0.059    0.000    0.081    0.000 entities.py:2(__init__)
	    53872    0.052    0.000    0.204    0.000 entities.py:52(__hash__)
	      254    0.044    0.000    0.044    0.000 {built-in method marshal.loads}
	    51/50    0.040    0.001    0.042    0.001 {built-in method _imp.create_dynamic}
	   422366    0.040    0.000    0.040    0.000 entities.py:5(__repr__)
	     4057    0.038    0.000   12.201    0.003 ClingoBridge.py:29(run)
	   448953    0.036    0.000    0.036    0.000 {method 'append' of 'list' objects}



# Experiment 3b

Planning agent (on empty policy, ph=5) in a 7-blocks world, 150 episodes

\tiny
	Wed Aug 19 10:44:10 2020    exp3b_profile_raw.txt
	
	         3844589 function calls (3836887 primitive calls) in 34.476 seconds
	
	   Ordered by: internal time
	   List reduced from 2715 to 20 due to restriction <20>
	
	   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
	     4936   18.177    0.004   18.177    0.004 {method 'ground' of 'clingo.Control' objects}
	     4936    7.226    0.001    7.489    0.002 {method 'solve' of 'clingo.Control' objects}
	     4936    2.515    0.001    2.515    0.001 {method 'load' of 'clingo.Control' objects}
	     4935    2.409    0.000   32.482    0.007 BlocksWorld.py:107(next_step)
	    16974    1.051    0.000    1.051    0.000 {method 'add' of 'clingo.Control' objects}
	     4936    0.517    0.000    0.517    0.000 ClingoBridge.py:6(__init__)
	   166257    0.461    0.000    0.546    0.000 BlocksWorld.py:160(parse_part_state)
	    42619    0.235    0.000    0.235    0.000 {method 'symbols' of 'clingo.Model' objects}
	    88278    0.207    0.000    0.257    0.000 BlocksWorld.py:173(parse_action)
	    18816    0.161    0.000    0.723    0.000 BlocksWorld.py:185(parse_state)
	    56354    0.114    0.000    0.151    0.000 entities.py:53(<listcomp>)
	        1    0.083    0.083    1.102    1.102 BlocksWorld.py:42(generate_all_states)
	   522544    0.077    0.000    0.077    0.000 entities.py:8(__eq__)
	   166264    0.062    0.000    0.085    0.000 entities.py:2(__init__)
	    56354    0.054    0.000    0.212    0.000 entities.py:52(__hash__)
	     4936    0.049    0.000   26.769    0.005 ClingoBridge.py:29(run)
	   476028    0.047    0.000    0.047    0.000 entities.py:5(__repr__)
	      254    0.045    0.000    0.045    0.000 {built-in method marshal.loads}
	   516934    0.043    0.000    0.043    0.000 {method 'append' of 'list' objects}
	    51/50    0.041    0.001    0.043    0.001 {built-in method _imp.create_dynamic}


# Experiment 3

## Observations

* For the tabula rasa agent, 16 out of the 18 seconds are spent in the `next_step` method of the `BlockWorld`.
	* This method starts the ASP-solver, so it is unsurprising that it takes time
	* Most time (10s) is spent grounding

* For the planning agent, double the time was spent in `next_step`, while the number of calls increased only by $25%$.
