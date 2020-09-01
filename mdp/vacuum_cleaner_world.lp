% VACUUM CLEANER WORLD
% A very simple MDP for testing and understanding purposes.


% PROBLEM-SPECIFIC DOMAIN (UNINTERPRETED FUNCTIONS) ****************************

%	VARIABLES:
%	L			... describes a location `L`, either `left` or `right`

% 	STATE FUNCTIONS S(...):
%	robot(L)	... describes the location `L` of the cleaning robot 
%	dirty(L)	... describes whether the location `L` is dirty.

%	ACTION FUNCTIONS A(...):
%	move(L)		...	the robot moves to location `L`
%	vacuum 		... the robot vacuums at its current location, after which that 
%					location is no longer dirty.

%	STATIC STATE (ATOMS):
%	(none for this mdp)

% KNOWLEDGE ********************************************************************

% Describe which actions are executable in a given state
% 	INPUT:		tic(S(...), T)
% 	INPUT:		terminal(T)
% 	OUTPUT: 	executable(A(...), T)
			
executable(move(left), T) :- tic(robot(right), T), not terminal(T).
executable(move(right), T) :- tic(robot(left), T), not terminal(T).
executable(vacuum, T) :- tic(robot(Location), T), tic(dirty(Location), T), 
						 not terminal(T).

% Describe the effects of state transitions
%	INPUT:		tic(S(...), T)
%	INPUT: 		act(A(...), T)
%	INPUT: 		time(T)
%	OUTPUT:		tic(S(...), T+1)

tic(robot(Location), T+1) :- tic(robot(Location), T), not act(move(_), T), time(T).
tic(dirty(Location), T+1) :- tic(dirty(Location), T), not act(vacuum, T), time(T).
tic(dirty(Location), T+1) :- tic(dirty(Location), T), not tic(robot(Location), T), 
							 time(T).
tic(robot(Location), T+1) :- act(move(Location), T), time(T).

% Describe the rewards for each state
%	INPUT: 		tic(S(...), T)
%	OUTPUT: 	partialReward(R, T)

all_clean(T) :- not tic(dirty(left), T), not tic(dirty(right), T), time(T).
partialReward(100, T) :- all_clean(T), not all_clean(T-1).
partialReward(-1, T) :- act(_, T-1).

% Describe terminal states
%	INPUT: 		tic(S(...), T)
%	OUTPUT: 	terminal(T)

terminal(T) :- all_clean(T).
