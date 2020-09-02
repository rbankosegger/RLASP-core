% Sokoban
% A challenging planning problem

% PROBLEM-SPECIFIC DOMAIN (UNINTERPRETED FUNCTIONS) ****************************

%	VARIABLES:

% 	STATE FUNCTIONS S(...):

%	ACTION FUNCTIONS A(...):

% 	STATIC ATOMS:



% KNOWLEDGE ********************************************************************

% Static knowledge

% Describe which actions are executable in a given state
% 	INPUT:		tic(S(...), T)
% 	OUTPUT: 	executable(A(...), T)

free(X,Y,T) :- time(T), row(Y), col(X), not block(X,Y), not tic(box(X,Y),T).

reach(X,Y,T)   :- tic(sokoban(X,Y),T).
reach(X+1,Y,T) :- reach(X,Y,T), free(X+1,Y,T).
reach(X-1,Y,T) :- reach(X,Y,T), free(X-1,Y,T).
reach(X,Y+1,T) :- reach(X,Y,T), free(X,Y+1,T).
reach(X,Y-1,T) :- reach(X,Y,T), free(X,Y-1,T).

executable(push(X,Y,left),T)  :- tic(box(X,Y),T), free(X-1,Y,T), reach(X+1,Y,T), not terminal(T).
executable(push(X,Y,right),T) :- tic(box(X,Y),T), free(X+1,Y,T), reach(X-1,Y,T), not terminal(T).
executable(push(X,Y,up),T)    :- tic(box(X,Y),T), free(X,Y-1,T), reach(X,Y+1,T), not terminal(T).
executable(push(X,Y,down),T)  :- tic(box(X,Y),T), free(X,Y+1,T), reach(X,Y-1,T), not terminal(T).


% Describe the effect of state transitions
%	INPUT:		tic(S(...), T)
%	INPUT: 		act(A(...), T)
%	INPUT: 		time(T)
%	OUTPUT:		tic(S(...), T+1)

tic(box(X,Y),T+1) :- time(T), tic(box(X,Y),T), not -tic(box(X,Y),T+1).
tic(sokoban(X,Y),T+1) :- time(T), tic(sokoban(X,Y),T), not -tic(sokoban(X,Y),T+1).

 tic(box(X-1,Y),T+1) :- act(push(X,Y,left),T).
 tic(box(X+1,Y),T+1) :- act(push(X,Y,right),T).
 tic(box(X,Y-1),T+1) :- act(push(X,Y,up),T).
 tic(box(X,Y+1),T+1) :- act(push(X,Y,down),T).
-tic(box(X,Y),T+1)   :- act(push(X,Y,_),T).

 tic(sokoban(X,Y),T+1)   :- act(push(X,Y,_),T).
-tic(sokoban(X,Y),T+1)   :- tic(sokoban(X,Y),T), act(push(_,_,_),T).

% Describe the rewards for each state
%	INPUT: 		tic(S(...), T)
%	OUTPUT: 	partialReward(R, T)

incomplete(T) :- time(T), tic(box(X,Y),T), not dest(X,Y).

% box is stuck in a corner
fail(T, box(R,C)) :- tic(box(R,C),T), not dest(R,C), block(R+1,C), block(R,C+1).
fail(T, box(R,C)) :- tic(box(R,C),T), not dest(R,C), block(R+1,C), block(R,C-1).
fail(T, box(R,C)) :- tic(box(R,C),T), not dest(R,C), block(R-1,C), block(R,C+1).
fail(T, box(R,C)) :- tic(box(R,C),T), not dest(R,C), block(R-1,C), block(R,C-1).
fail :- fail(_, _).

partialReward(100,T) :- time(T), not incomplete(T), incomplete(T-1).
partialReward(-100,T) :- fail(T,F), not fail(T-1,F).
partialReward(-1,T)  :- act(push(_,_,_),T-1).

% Describe terminal states
%	INPUT: 		tic(S(...), T)
%	OUTPUT: 	terminal(T)
terminal(T) :- time(T), not incomplete(T).

