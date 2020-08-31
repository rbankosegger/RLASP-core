% MDP specification for the blocks world

% input predicates ********************************************************************************
% current(X) ...	X is a term representation of a state predicate, provided by BlocksWorld.py, optional
% action(X) ...  	X is term representation of an action that has been chosen, provided by BlocksWorld.py, optional
% subgoal(X,Y) ... 	X is on top of Y in goal state
% constant t representing the planning horizon
% *************************************************************************************************

#defined action/1. % silence warning that action does not appear in rule head

% executable(X) ... X is term representation of an action that is executable in the follow-up state
executable(F) :- executable(F,1), t > 0.
executable(F) :- executable(F,0), t = 0.

tic(F, 0) :- current(F).
act(F, 0) :- action(F).

% state(X) ... X is a term representation of a state predicate that holds in the follow-up state
state(on(X,Y)) :- tic(on(X,Y), 1).

% nextReward(N) ... N is the reward the agents gets after performing a given action
nextReward(S) :- S = #sum {R : reward(R, 1) }.

% bestAction(X) ... X is a term representation of the next action that yields maximal reward within t steps
bestAction(F) :- act(F, 0).

% consider t planning steps, provided by BlocksWorld.py
time(0..t).

goal(T) :- time(T), { not tic(F, T) : subgoal(F) } = 0.    
 
% rewards depending on the current state, the chosen action, and the follow-up state
reward(100,T) :- goal(T), not goal(T-1).        % big reward for reaching the goal the first time
reward(-1,T)  :- act(_,T-1).                 % small penalty for each move

% background knowledge ****************************************************************************

% the table and every block is a location
block(X) :- current(on(X,_)).

location(table).
location(X) :- block(X).

tic(occupied(X), T) :- block(X), tic(on(_,X), T).
tic(free(X), T) :- location(X), time(T), not tic(occupied(X), T).

% at each time point, make one move unless the goal has been reached

executable(move(X,Y), T) :- block(X), tic(free(X), T), tic(free(Y), T), not tic(on(X,Y), T), X != Y, not goal(T).

{ act(F, T) : executable(F, T)} = 1 :- time(T), T < t, not goal(T).

% by default, blocks do not change location (frame axiom)
tic(on(X,Y), T+1) :- tic(on(X,Y), T), not -tic(on(X,Y),T+1), time(T).

% effects of action move
-tic(on(X,Y), T+1) :- act(move(X,_), T), tic(on(X,Y), T), time(T).
tic(on(X,Y), T+1) :- act(move(X,Y),T), time(T).

% maximize the reward function
maxReward(S)     :- S = #sum { R,T : reward(R,T) }.
#maximize { S : maxReward(S) }.
