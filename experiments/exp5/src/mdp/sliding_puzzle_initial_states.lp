% enumerate all valid states for the sliding puzzle given some pieces

% input predicates ********************************************************************************
% size(S) ... Size of the sliding puzzle
% piece(P) ... Piece in the sliding puzzle
% *************************************************************************************************
% size(2).
% piece(1..N) :- size(S), N = S*S-2.

% state/1 with state(X) if X is a term representation of a state predicate
state(on(P,X,Y)) :- on(P,X,Y).

% a position X,Y is a location
location(0..S-1,0..S-1) :- size(S).

% every piece is placed on exactly one location
{ on(P,X,Y) : location(X,Y)  } = 1  :- piece(P).

% there cannot be more than one piece in a location
% :- piece(P), { on(P,X,Y) : piece(P) } > 1.
:- on(P1,X,Y), on(P2,X,Y), P1 != P2.
