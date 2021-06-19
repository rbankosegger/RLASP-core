% Domain knowledge


% Carcass rules
%
% rule(R,N)										... rule R is the Nth rule to choose from
% applicable(R, (arg1, arg2, ...)) 				... rule $ is applicable with args
% choose(R) 									... rule R was chosen
% abstractAction(abstract(...), ground(...))	... abstract action `abstract(...)` is available and has a corresponding ground action `ground(...)`.

width(W) :- W = #max { X : obj(_, X, _) }.
height(H) :- H = #max { Y : obj(_, _, Y) }.

tile((0..W, 0..H)) :- width(W), height(H).

blocked((X,Y)) :- obj(wall(_), X, Y).
blocked((X,Y)) :- obj(door(_,_), X, Y).
blocked((X,Y)) :- obj(lava, X, Y).

empty(T) :- tile(T), not blocked(T).

choke((X,Y)) :- empty((X,Y)), blocked((X-1,Y)), blocked((X+1,Y)).
choke((X,Y)) :- empty((X,Y)), blocked((X,Y-1)), blocked((X,Y+1)).

adjacent((X1,Y1), (X2,Y2)) :- tile((X1,Y1)), tile((X2,Y2)), X1=X2+1, Y1=Y2.
adjacent((X1,Y1), (X2,Y2)) :- tile((X1,Y1)), tile((X2,Y2)), X1=X2-1, Y1=Y2.
adjacent((X1,Y1), (X2,Y2)) :- tile((X1,Y1)), tile((X2,Y2)), X1=X2, Y1=Y2+1.
adjacent((X1,Y1), (X2,Y2)) :- tile((X1,Y1)), tile((X2,Y2)), X1=X2, Y1=Y2-1.

sameRoom(T, T) :- empty(T), not choke(T).
sameRoom(T1,T2) :- sameRoom(T2,T1).
sameRoom(T1, T2) :- sameRoom(T1, U), adjacent(U, T2), empty(T2), not choke(T2).


linkable((X,Y)) :- obj(door(_,_), X, Y).
linkable((X,Y)) :- obj(goal, X, Y).
linkable((X,Y)) :- obj(agent(_), X, Y).
linkable((X,Y)) :- obj(key(_), X, Y).
linkable((X,Y)) :- obj(ball(_), X, Y).
linkable(T) :- choke(T).

linked((XO1, YO1), (XO2,YO2)) :- linkable((XO1, YO1)), adjacent(T1, (XO1, YO1)),
				 				 linkable((XO2, YO2)), adjacent(T2, (XO2, YO2)),
				                 sameRoom(T1,T2).


%accessible((X,Y)) :- obj(agent(_), X, Y).
%accessible(T2) :- accessible(T1), linked(T1,T2), T2=(X,Y), not obj(door(_,locked), X, Y).


path(0, (XA,YA)) :- obj(agent(_), XA, YA).
0 { path(N+1, T1) : linked(T0,T1), T0 != T1 } 1 :- path(N, T0), N < 10.
:~ obj(goal, X, Y), not path(_, (X, Y)). [ 1@2 ]
#minimize { 1@1, N : path(N, _) }.

nextGoal(T) :- path(1, T).

% Generate drawables for debug purposes. They are by default not shown in the answer set!
highlight(X,Y,cyan) :- sameRoom((XA,YA), (X,Y)), obj(agent(_), XA, YA).
highlight(X,Y,white) :- nextGoal((X,Y)).
line(T0, T1, lightgrey) :- linked(T0, T1), not arrow(T0, T1, _), not arrow(T1,T0, _).
arrow(T0, T1, cyan) :- path(N, T0), path(N+1, T1).

% Dir 0: >
% Dir 1: V
% Dir 2: <
% Dir 3: ^
facing(east) :- obj(agent(0)).
facing(south) :- obj(agent(1)).
facing(west) :- obj(agent(2)).
facing(north) :- obj(agent(3)).

agent((X,Y)) :- obj(agent(_),X,Y).

orientation(north) :- agent((AX,AY)), nextGoal((GX,GY)), AY > GY.
orientation(south) :- agent((AX,AY)), nextGoal((GX,GY)), AY < GY.
orientation(east) :- agent((AX,AY)), nextGoal((GX,GY)), AX < GX.
orientation(west) :- agent((AX,AY)), nextGoal((GX,GY)), AX > GX.

direction(north;south;east;west).

%%%%%%%%%%%%%%%%%%% CARCASS RULES %%%%%%%%%%%%%%%%%%%

1 { choose(R) : applicable(R, _) } 1.
:- choose(R), rule(R,N), rule(R2,N2), applicable(R2, _), N2 < N.


% Rule 1: Touching and facing a goal, which is anything but a locked door.
rule(touching_and_facing_notlocked, 1).
applicable(touching_and_facing_notlocked, ()) :- nextGoal(G), agent(A), adjacent(G,A), facing(D), orientation(D), not obj(door(_,locked), GX, GY), G=(GX,GY).

% Rule 2: Touching and facing a goal, which can only be a locked door (otherwise, rule 1 would have applied).
rule(touching_and_facing_locked, 2).
applicable(touching_and_facing_locked, ()) :- nextGoal(G), agent(A), adjacent(G,A), facing(D), orientation(D).

% Rule 3: Touching a goal but not facing it
rule(touching, 3).
applicable(touching, ()) :- nextGoal(G), agent(A), adjacent(G, A).

% TODO: Rules for facing north northwest, etc...
%rule(northwest_facing, 4

% Rule 4: Agent is north of goal and facing towards the goal
%rule(north_facing, 4) :- nextGoal((GX,GY)), obj(agent(1), AX, AY), GX=AX, GX < GY.

% Rule 5: Agent is north of goal and facing any direction
%rule(north, 5) :- nextGoal((GX,GY)), obj(agent(_), AX, AY), GX=AX, GX < GY.

% Northeast
% East
% Southeast
% South 
% Southwest
% West
% Northwest


% The gutter action is available in every state and collects all available actions that were not covered by the rule-specific abstract actions.
abstractAction(R, left) :- choose(R). 
abstractAction(R, right) :- choose(R). 
abstractAction(R, forward) :- choose(R). 
abstractAction(R, pickup) :- choose(R). 
abstractAction(R, drop) :- choose(R). 
abstractAction(R, toggle) :- choose(R). 
abstractAction(R, done) :- choose(R). 

% The gutter state collects all states not covered by some rule.
rule(gutterState, #sup).	
applicable(gutterState(), ()).

#show choose/1.
#show abstractAction/2.
#show applicable/2.
