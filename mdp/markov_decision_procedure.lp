% MARKOV DECISION PROCESS INTERFACE
% Describes abstract knowledge which is valid for all MDP's

% GENERAL MDP DOMAIN ***********************************************************

%	CONSTANTS:
%	T			... describes a point in time. 
%					`T=0` is always the current time ("now").

%	INPUT PREDICATES (added to the domain programmatically):
%	current(S(...)) ... describes a part of the current state, where `S(...)` is an 
%						uninterpreted function with zero or more arguments.
%	action(A(...)) 	... describes an action taken in the current state, 
%						where `A(...)` is an uninterpreted function with zero or
%						more arguments.
%	subgoal(S(...)) ...	describes a part of the goal state of the MDP, 
%						where `S(...)` is an uninterpreted function with zero or 
%						more arguments.


%	INTERNAL PREDICATES (used to add problem-specific details, used e.g. by the planner)
%	time(T)			...	defines `T >= 0` to be a point in time.
%	tic(S(...), T)	... desribes a part of the state at time `T`, with `S(...)` being a
%						function just as for `current(S(...))`.
%						Note that `current(S(...))` iff `tic(S(...), 0)`.
%	act(A(...), T)	... desribes an action taken at time `T`, with `A(...)` being a
%						function just as for `action(A(...))`.
%	partialReward(R, T) ... describes part of the reward or punishment `R` received
%							at time `T`. All partial rewards will be summed per time
%							step to end up with a total reward (see `nextReward(R)`)
%	terminal(T)		...	describes that a terminal state has been reached at timestep `T`.


%	OUTPUT PREDICATES (used by the python program to read out information)
%	state(S(...))		... describes the state of the world after executing 
%							the current action described by `action(A(...))`.
%							Note that `state(S(...))` iff `tic(S(...), 1)`.
% 	executable(A(...))	... describes actions `A(...)` executable from 
%							the current state or next state (depending on `t`).
%	nextReward(S)		...	describes the total reward `S` to be received at the next time step.
%	bestAction(A(...))	...	describes the optimal action to take in the current state.
%	maxReturn(R)		...	describes the expected return when taking the optimal path to the goal.


% GENERAL KNOWLEDGE ************************************************************

% Describe the current state and action (if any)
tic(F, 0) :- current(F).
act(F, 0) :- action(F).
#defined action/1.

% Describe the next state
state(F) :- tic(F,1).

% Describe which actions are executable in the current or next state.
executable(F) :- executable(F,1), t > 0.
executable(F) :- executable(F,0), t = 0.

% Describe the reward for the next time step
nextReward(S) :- S = #sum { R : partialReward(R, 1) }.

time(0).
time(1) :- action(_).
