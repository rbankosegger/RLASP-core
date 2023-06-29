% CREDITS: Tobias Datler

block(1..3).
location(floor).
location(B) :- block(B).

% Generate
1 = { on(B,L) : location(L), B!=L } :- block(B).

:- block(X), { on(Y,X) : block(Y) } > 1.

supported(X) :- on(X,floor).
supported(X) :- on(X,Y), supported(Y).
:- block(X), not supported(X).

free(floor).
free(B) :- block(B), not on(_, B).

1 = { move(B,L) : free(B), block(B), free(L), B!=L, not on(B,L)}.
