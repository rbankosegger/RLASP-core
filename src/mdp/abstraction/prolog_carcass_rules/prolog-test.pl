subgoal(0,table).
subgoal(1,0).
subgoal(2,1).

on(0,table).
on(1,table).
on(2,0).

% Domain knowledge
goalRelevantBlock(A) :- subgoal(A, _).
goalRelevantBlock(A) :- subgoal(_, A).

above(A,B) :- on(A,B).
above(A,B) :- on(A,C), above(C,B).

goodPartialTowerBase(TowerBase) :- subgoal(_, TowerBase), \+ subgoal(TowerBase, _), aggregate_all(count, towerBaseAboveGoalRelevantBlock(TowerBase,_), 0).
% 0 = #count { A : above(TowerBase, A), goalRelevantBlock(A) }.
%
towerBaseAboveGoalRelevantBlock(Base, Block) :- above(Base,Block), goalRelevantBlock(Block).

goodPartialTower(TowerBase, TowerBase) :-  goodPartialTowerBase(TowerBase).
goodPartialTower(TowerBase, B) :- goodPartialTower(TowerBase, B2), on(B,B2), subgoal(B,B2).
goodPartialTowerTop(TowerBase, TopBlock) :- subgoal(B, TopBlock), \+ on(B,TopBlock), goodPartialTower(TowerBase, TopBlock).

clear(A) :- on(A,_), \+ on(_,A).
clear(table).
