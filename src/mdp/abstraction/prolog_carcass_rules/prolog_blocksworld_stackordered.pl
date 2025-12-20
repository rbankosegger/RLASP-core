% Domain knowledge
goalRelevantBlock(A) :- subgoal(A, _).
goalRelevantBlock(A) :- subgoal(_, A).

block(A) :- on(A,_).

above(A,B) :- on(A,B).
above(A,B) :- on(A,C), above(C,B).

%final(table).
%finalBelow(A) :- above(A,B), final(B).
notFinal(A) :- subgoal(A,B), \+ on(A,B).
notFinal(A) :- above(A,B), notFinal(B).
final(A) :- block(A), \+ notFinal(A).
final(table).

%not_final(A) :- on(A,B), not_final(B).

goodPartialTowerBase(TowerBase) :- subgoal(_, TowerBase), \+ subgoal(TowerBase, _), final(TowerBase).
goodPartialTower(TowerBase, TowerBase) :-  goodPartialTowerBase(TowerBase).
goodPartialTower(TowerBase, B) :- on(B,B2), subgoal(B,B2), goodPartialTower(TowerBase, B2).
goodPartialTowerTop(TowerBase, TopBlock) :- subgoal(B, TopBlock), \+ on(B,TopBlock), goodPartialTower(TowerBase, TopBlock).

clear(A) :- on(A,_), \+ on(_,A).
clear(table).

% Carcass rules
%
% rule(R,N)										... rule R is the Nth rule to choose from
% applicable(R, (arg1, arg2, ...)) 				... rule $ is applicable with args
% choose(R) 									... rule R was chosen
% abstractAction(abstract(...), ground(...))	... abstract action `abstract(...)` is available and has a corresponding ground action `ground(...)`.

% Informs the system that the clauses of the specified predicate(s) might not be together in the source file.
:- discontiguous applicable/2.
:- discontiguous rule/2.
:- discontiguous abstractAction/2.

not_min_choice(R1) :- applicable(R1,_), rule(R1,I1), applicable(R2,_), rule(R2,I2), I2<I1.
choose(R) :- rule(R,_), applicable(R,_), \+ not_min_choice(R), !.


% Rule 0: a goal-tower exists and is clear, next goal block is clear
rule(r0,0).
applicable(r0, (GoodTowerTop, NextGoalBlock)) :- goodPartialTowerTop(_, GoodTowerTop),clear(GoodTowerTop),subgoal(NextGoalBlock, GoodTowerTop), clear(NextGoalBlock).
abstractAction(move(nextGoalBlock, goodTowerTop), move(NextGoalBlock, GoodTowerTop)) :- choose(r0), applicable(r0, (GoodTowerTop, NextGoalBlock)).
													 
	
% Rule 1: A goal tower exists and has other blocks on top. 
rule(r1, 1).
applicable(r1, (GoodTowerBase, GoodTowerTop, BadTopBlock)) :- goodPartialTowerTop(GoodTowerBase, GoodTowerTop), \+ clear(GoodTowerTop), above(BadTopBlock, GoodTowerTop), clear(BadTopBlock).
abstractAction(move(badTopBlock, table), move(BadTopBlock, table)) :- choose(r1), applicable(r1, (_, _, BadTopBlock)).
abstractAction(move(badTopBlock, otherTowerTop), move(BadTopBlock, OtherTowerTop)) :- choose(r1), applicable(r1, (_, _, BadTopBlock)), clear(OtherTowerTop), \+ OtherTowerTop=BadTopBlock, \+ OtherTowerTop=table.



% Rule 2:     a goal-tower exists and is clear, next goal block is not clear.
rule(r2,2).
applicable(r2, (GoodTowerTop, BadTopBlock)) :- 	goodPartialTowerTop(_, GoodTowerTop),clear(GoodTowerTop), subgoal(NextGoalBlock, GoodTowerTop), \+ clear(NextGoalBlock), above(BadTopBlock,NextGoalBlock), clear(BadTopBlock).
abstractAction(move(badTopBlock, table), move(BadTopBlock, table)) :- choose(r2), applicable(r2, (_, BadTopBlock)).
abstractAction(move(badTopBlock, otherTowerTop), move(BadTopBlock, OtherTowerTop)) :- choose(r2), applicable(r2, (GoodTowerTop, BadTopBlock)), clear(OtherTowerTop), \+ OtherTowerTop=GoodTowerTop, \+ OtherTowerTop=BadTopBlock, \+ OtherTowerTop=table.

% Rule 3:	No gloal tower exists, first goal block is not clear.
rule(r3,3).
applicable(r3, (BadTopBlock)) :- \+ goodPartialTowerBase(_), subgoal(_, TowerBase), \+ subgoal(TowerBase, _), \+ clear(TowerBase), above(BadTopBlock, TowerBase), clear(BadTopBlock).
abstractAction(move(badTopBlock, table), move(BadTopBlock, table)) :- choose(r3), applicable(r3, (BadTopBlock)).
abstractAction(move(badTopBlock, otherTowerTop), move(BadTopBlock, OtherTowerTop)) :- choose(r3), applicable(r3, (BadTopBlock)), clear(OtherTowerTop), \+OtherTowerTop=BadTopBlock, \+OtherTowerTop=table.


% Rule 4:	No goal tower exists, first goal block is clear.
rule(r4,4).
applicable(r4, (TowerBase)) :- \+ goodPartialTowerBase(_), subgoal(_, TowerBase), \+ subgoal(TowerBase, _), clear(TowerBase).
abstractAction(move(towerBase, table), move(TowerBase, table)) :- choose(r4), applicable(r4, (TowerBase)).

% The gutter action is available in every state and collects all available actions that were not covered by the rule-specific abstract actions.
abstractAction(gutterAction, move(X, Y)) :- clear(X), clear(Y), \+ abstractAction(move(_,_),move(X,Y)), \+ on(X,Y), \+ X=Y, \+ X=table.

% The gutter state collects all states not covered by some rule.
rule(gutter, 1.0Inf).	
applicable(gutter, []).
