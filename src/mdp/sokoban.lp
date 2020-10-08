% Sokoban
% A challenging planning problem

% PROBLEM-SPECIFIC DOMAIN (UNINTERPRETED FUNCTIONS) ****************************

%	VARIABLES:
%	X		... describes an x-position (column) in the world
%	Y		... describes a y-position (row) in the world
%	D		... describes a direction (left, right, up, down)

% 	STATE FUNCTIONS S(...):
%	box(X,Y)		... describes a box being at position X,Y.
%	sokoban(X,Y)	... describes a box being at position X,Y.

%	ACTION FUNCTIONS A(...):
%	push(X,Y,D)		... describes the action of pushing the block at position 
%						X,Y in direction D.

% 	STATIC ATOMS:
%	dest(X,Y)		... describes that X,Y is a destination for some box
%	block(X,Y)		... describes that X,Y is blocked, i.e. neither players 
%						nor boxes can enter this position.
%	row(Y)			... identifies Y as a row
%	col(X)			... identifies X as a column


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

pushable(X,Y,T) :- tic(box(X,Y),T), free(X-1,Y,T), reach(X+1,Y,T).
pushable(X,Y,T) :- tic(box(X,Y),T), free(X+1,Y,T), reach(X-1,Y,T).
pushable(X,Y,T) :- tic(box(X,Y),T), free(X,Y-1,T), reach(X,Y+1,T).
pushable(X,Y,T) :- tic(box(X,Y),T), free(X,Y+1,T), reach(X,Y-1,T).

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
fail(T) :- tic(box(R,C),T), not dest(R,C), block(R+1,C), block(R,C+1).
fail(T) :- tic(box(R,C),T), not dest(R,C), block(R+1,C), block(R,C-1).
fail(T) :- tic(box(R,C),T), not dest(R,C), block(R-1,C), block(R,C+1).
fail(T) :- tic(box(R,C),T), not dest(R,C), block(R-1,C), block(R,C-1).

% Level incomplete but no more actions are available.
fail(T) :- incomplete(T), not pushable(_,_,T).

partialReward(100,T) :- time(T), not incomplete(T), incomplete(T-1).
partialReward(-100,T) :- fail(T), not fail(T-1).
partialReward(-1,T)  :- act(push(_,_,_),T-1).

% Describe terminal states
%	INPUT: 		tic(S(...), T)
%	OUTPUT: 	terminal(T)
terminal(T) :- time(T), not incomplete(T).
terminal(T) :- fail(T).

