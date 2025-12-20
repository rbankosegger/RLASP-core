%
% 3-blocks world example carcass from Otterlo's PhD thesis (2008) p. 253, example 5.2.1
%
% rule(R,N)										... rule R is the Nth rule to choose from
% applicable(R, (arg1, arg2, ...)) 				... rule $ is applicable with args
% choose(R) 									... rule R was chosen
% abstractAction(abstract(...), ground(...))	... abstract action `abstract(...)` is available and has a corresponding ground action `ground(...)`.
%


% Informs the system that the clauses of the specified predicate(s) might not be together in the source file.
:- discontiguous applicable/2.
:- discontiguous rule/2.
:- discontiguous abstractAction/2.

% Choose minimal applicable element
not_min_choice(R1) :- applicable(R1,_), rule(R1,I1), applicable(R2,_), rule(R2,I2), I2<I1.
choose(R) :- rule(R,_), applicable(R,_), \+ not_min_choice(R).

rule(r1,1). % rule atoms not needed in the Prolog version
applicable(r1, (A,B,C)) :- on(A,B), on(B,table), on(C,table), \+ A=B, \+ B=C.
abstractAction(move(x1,x3), move(A,C)) :- choose(r1), applicable(r1, (A,_,C)).
abstractAction(move(x3,x1), move(C,A)) :- choose(r1), applicable(r1, (A,_,C)).
abstractAction(move(x1,table), move(A,table)) :- choose(r1), applicable(r1, (A,_,_)).

rule(r2,2).
applicable(r2, (A,B,C)) :- on(A,table), on(B,table), on(C,table), \+ A=B, \+ B=C, \+ A=C.
abstractAction(move(x1,x2), move(A,B)) :- choose(r2), applicable(r2, (A,B,_)).
abstractAction(move(x2,x1), move(B,A)) :- choose(r2), applicable(r2, (A,B,_)).
abstractAction(move(x1,x3), move(A,C)) :- choose(r2), applicable(r2, (A,_,C)).
abstractAction(move(x3,x1), move(C,A)) :- choose(r2), applicable(r2, (A,_,C)).
abstractAction(move(x2,x3), move(B,C)) :- choose(r2), applicable(r2, (_,B,C)).
abstractAction(move(x3,x2), move(C,B)) :- choose(r2), applicable(r2, (_,B,C)).

rule(r3,3).
applicable(r3, (A,B,C)) :- on(A,B), on(B,C), on(C,table), \+ A=B, \+ B=C, \+ C=table.
abstractAction(move(x1,table), move(A,table)) :- choose(r3), applicable(r3, (A,_,_)).

rule(gutter, 1.0Inf).	
applicable(gutter, []).
