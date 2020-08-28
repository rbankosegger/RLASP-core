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
nextReward(N) :- totalReward(N,1). 

% consider t planning steps, provided by BlocksWorld.py
time(0..t).

% background knowledge ****************************************************************************

executable(move(left), T) :- tic(robot(right), T).
executable(move(right), T) :- tic(robot(left), T).
executable(vacuum, T) :- tic(robot(Location), T), tic(dirty(Location), T).

tic(robot(Location), 1) :- tic(robot(Location), 0), not act(move(_), 0).
tic(dirty(Location), 1) :- tic(dirty(Location), 0), not act(vacuum, 0).
tic(dirty(Location), 1) :- tic(dirty(Location), 0), not tic(robot(Location), 0).
tic(robot(Location), 1) :- act(move(Location), 0).

reward(100, T) :- not tic(dirty(left), T), not tic(dirty(right), T), time(T).
reward(-1, T) :- tic(dirty(left), T).
reward(-1, T) :- tic(dirty(right), T).

totalReward(S,T) :- time(T), S = #sum { R : reward(R,T) }.
