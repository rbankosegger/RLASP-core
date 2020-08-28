% current(F) ... F is an uninterpreted function representing (part of) the current state.
tic(F, 0) :- current(F).

% action(T) ... T is an uninterpreted function representing (part of) the current action.
act(F, 0) :- action(F).

% executable(X) ... X is term representation of an action that is executable in the follow-up state
executable(F) :- executable(F,1), t > 0.
executable(F) :- executable(F,0), t = 0.

% state(X) ... X is a term representation of a state predicate that holds in the follow-up state
state(F) :- tic(F,1).

% nextReward(N) ... N is the reward the agents gets after performing a given action
nextReward(S) :- S = #sum { R : reward(R, 1) }.

% bestAction(X) ... X is a term representation of the next action that yields maximal reward within t steps
bestAction(F) :- act(F, 0).

% consider t planning steps, provided by markov_decision_procedure.py
time(0..t).

% background knowledge ****************************************************************************

executable(move(left), T) :- tic(robot(right), T).
executable(move(right), T) :- tic(robot(left), T).
executable(vacuum, T) :- tic(robot(Location), T), tic(dirty(Location), T).
{ act(F, T) : executable(F, T)} = 1 :- time(T), T < t, not goal(T).

tic(robot(Location), T+1) :- tic(robot(Location), T), not act(move(_), T), time(T).
tic(dirty(Location), T+1) :- tic(dirty(Location), T), not act(vacuum, T), time(T).
tic(dirty(Location), T+1) :- tic(dirty(Location), T), not tic(robot(Location), T), time(T).
tic(robot(Location), T+1) :- act(move(Location), T), time(T).

goal(T) :- not tic(dirty(left), T), not tic(dirty(right), T), time(T).
reward(100, T) :- goal(T), not goal(T-1).
reward(-1, T) :- act(F, T-1).

maxReward(S) :- S = #sum { R,T : reward(R,T) }.
#maximize { S: maxReward(S) }.
