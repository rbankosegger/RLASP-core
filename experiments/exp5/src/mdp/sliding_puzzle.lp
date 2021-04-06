% Sliding Puzzle
% Another complicated planning problem

% PROBLEM-SPECIFIC DOMAIN (UNINTERPRETED FUNCTIONS) ****************************

%	VARIABLES:
%	P			... describes a piece (`p1`, `p2`, ...) in the sliding puzzle.
%	X,Y			... describes a location to put pieces on
%					(`1,1`, `1,2`, `1,3`, ...).

% 	STATE FUNCTIONS S(...):
%	on(P,X,Y)		... describes piece `P` being on location `X,Y`.

%	ACTION FUNCTIONS A(...):
%	move(P,X,Y)	... describes the action of moving piece `P` to location `X,Y`.

%	STATIC STATE (ATOMS):
%	subgoal(P,X,Y)	... describes that `P` on position `X,Y` is
%						(part of) the goal state.


% KNOWLEDGE ********************************************************************
% currentState(on(p1,1,1)).
% currentState(on(p0,1,0)).
% subgoal(p1,0,1).
% subgoal(p1,0,1). subgoal(p0,0,0).

% Static knowledge
piece(P) :- tic(on(P,_,_), 0).

size(2..4).
square(R,S) :- size(R), S = R**2.
squareSize(S) :- N = #count{P : piece(P)}, S = #min{ R : square(T,R), R > N}.
location(0..R-1,0..R-1) :- squareSize(S), square(R,S).

% Describe which actions are executable in a given state
% 	INPUT:		tic(S(...), T)
% 	INPUT:		terminal(T)
% 	OUTPUT: 	executable(A(...), T)

occupied(X,Y, T) :- tic(on(_,X,Y), T).
free(X,Y, T) :- location(X,Y), time(T), not occupied(X,Y,T).
adjacent(X,Y1,X,Y2) :- location(X,Y1), location(X,Y2), 1 = |Y2-Y1|.
adjacent(X1,Y,X2,Y) :- location(X1,Y), location(X2,Y), 1 = |X2-X1|.
executable(move(P,X2,Y2), T) :- piece(P), tic(on(P,X1,Y1), T), free(X2,Y2,T),
                                adjacent(X1,Y1,X2,Y2), not terminal(T).

% Describe the effect of state transitions
%	INPUT:		tic(S(...), T)
%	INPUT: 		act(A(...), T)
%	INPUT: 		time(T)
%	OUTPUT:		tic(S(...), T+1)

tic(on(P,X,Y), T+1) :- tic(on(P,X,Y), T), not act(move(P,_,_), T), time(T).
tic(on(P,X,Y), T+1) :- act(move(P,X,Y),T), time(T).


% Describe the rewards for each state
%	INPUT: 		tic(S(...), T)
%	OUTPUT: 	partialReward(R, T)

goalState(T) :- time(T), { not tic(on(P,X,Y), T) : subgoal(P,X,Y) } = 0.
partialReward(100,T) :- goalState(T), not goalState(T-1).
partialReward(-1,T)  :- act(_,T-1).


% Describe terminal states
%	INPUT: 		tic(S(...), T)
%	OUTPUT: 	terminal(T)

terminal(T) :- goalState(T).
