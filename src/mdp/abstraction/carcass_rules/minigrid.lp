% Domain knowledge


% Carcass rules
%
% rule(R,N)										... rule R is the Nth rule to choose from
% applicable(R, (arg1, arg2, ...)) 				... rule $ is applicable with args
% choose(R) 									... rule R was chosen
% abstractAction(abstract(...), ground(...))	... abstract action `abstract(...)` is available and has a corresponding ground action `ground(...)`.

width(W) :- W = #max { X : obj(_, (X, _)) }.
height(H) :- H = #max { Y : obj(_, (_, Y)) }.

tile((0..W, 0..H)) :- width(W), height(H).

blocked(XY) :- obj(wall(_), XY).
blocked(XY) :- obj(door(_,_), XY).
blocked(XY) :- obj(lava, XY).

dangerous(XY) :- obj(ball(blue), XY).
dangerous(XY) :- obj(lava, XY).

empty(T) :- tile(T), not blocked(T).

choke((X,Y), vertical) :- empty((X,Y)), blocked((X-1,Y)), blocked((X+1,Y)).
choke((X,Y), horizontal) :- empty((X,Y)), blocked((X,Y-1)), blocked((X,Y+1)).

adjacent((X1,Y1), (X2,Y2)) :- tile((X1,Y1)), tile((X2,Y2)), X1=X2+1, Y1=Y2.
adjacent((X1,Y1), (X2,Y2)) :- tile((X1,Y1)), tile((X2,Y2)), X1=X2-1, Y1=Y2.
adjacent((X1,Y1), (X2,Y2)) :- tile((X1,Y1)), tile((X2,Y2)), X1=X2, Y1=Y2+1.
adjacent((X1,Y1), (X2,Y2)) :- tile((X1,Y1)), tile((X2,Y2)), X1=X2, Y1=Y2-1.

sameRoom(T, T) :- empty(T), not choke(T, _).
sameRoom(T1,T2) :- sameRoom(T2,T1).
sameRoom(T1, T2) :- sameRoom(T1, U), adjacent(U, T2), empty(T2), not choke(T2,_).


linkable(XY) :- obj(door(_,_), XY).
linkable(XY) :- obj(goal, XY).
linkable(XY) :- obj(agent(_), XY).
linkable(XY) :- obj(key(_), XY).
linkable(XY) :- obj(ball(C), XY), not C = blue.
linkable(T) :- choke(T, _).

linked(U, V) :- linkable(U), adjacent(U, P),
				linkable(V), adjacent(V, Q),
			    sameRoom(P,Q).
linked(U, V) :- linkable(U), linkable(V), adjacent(U,P), adjacent(V,P), 
				not blocked(P), not linkable(P).
linked(U, V) :- linkable(U), linkable(V), adjacent(U,V).


%accessible(XY) :- obj(agent(_), XY).
%accessible(T2) :- accessible(T1), linked(T1,T2), not obj(door(_,locked), T2).

% The goal should be the "goal" object in the world.
% Unless, there is a key to be picked up. Then, until the key is picked up, the key is the goal instead.
goal(XY) :- obj(key(_),XY).
goal(XY) :- obj(goal,XY), not obj(key(_),_).


path(0, XY) :- obj(agent(_), XY).
0 { path(N+1, T1) : linked(T0,T1), T0 != T1 } 1 :- path(N, T0), N < 20.
:~ goal(XY), not path(_, XY). [ 1@2 ]
#minimize { 1@1, N : path(N, _) }.

nextGoal(T) :- path(1, T).

% Generate drawables for debug purposes. They are by default not shown in the answer set!
highlight(X,Y,cyan) :- sameRoom(A, (X,Y)), obj(agent(_), A).
highlight(X,Y,white) :- nextGoal((X,Y)).
highlight(X,Y,purple) :- linkable((X,Y)).
highlight(X,Y,red) :- dangerous((X,Y)).
line(T0, T1, lightgrey) :- linked(T0, T1), not arrow(T0, T1, _), not arrow(T1,T0, _), not T0=T1.
arrow(T0, T1, cyan) :- path(N, T0), path(N+1, T1).

agent(XY) :- obj(agent(_), XY).

objective_y_is(north) :- agent((AX,AY)), nextGoal((GX,GY)), AY > GY.
objective_y_is(south) :- agent((AX,AY)), nextGoal((GX,GY)), AY < GY.
objective_y_is(on_axis) :- agent((AX,AY)), nextGoal((GX,GY)), AY = GY.
objective_x_is(east) :- agent((AX,AY)), nextGoal((GX,GY)), AX < GX.
objective_x_is(west) :- agent((AX,AY)), nextGoal((GX,GY)), AX > GX.
objective_x_is(on_axis) :- agent((AX,AY)), nextGoal((GX,GY)), AX = GX.

touching(goal) :- agent(A), nextGoal(G), adjacent(A,G), obj(goal, G).
touching(key(C)) :- agent(A), nextGoal(G), adjacent(A,G), obj(key(C), G).
touching(door(S)) :- agent(A), nextGoal(G), adjacent(A,G), obj(door(_, S), G).
touching(choke) :- agent(A), nextGoal(G), adjacent(A,G), choke(G,_), not touching(goal), not touching(door(_)).
touching(none) :- not touching(goal), not touching(door(_)), not touching(choke).

in_choke(D) :- agent(XY), choke(XY,D).
in_choke(none) :- not in_choke(horizontal), not in_choke(vertical).

%%%%%%%%%%%%%%%%%%% CARCASS RULES %%%%%%%%%%%%%%%%%%%

1 { choose(R) : applicable(R, _) } 1.
:- choose(R), rule(R,N), rule(R2,N2), applicable(R2, _), N2 < N.

rule(facing_danger, 1).

applicable(facing_danger, ()) :- obj(agent(north),(X,Y)), dangerous((X,Y-1)).
applicable(facing_danger, ()) :- obj(agent(south),(X,Y)), dangerous((X,Y+1)).
applicable(facing_danger, ()) :- obj(agent(east),(X,Y)), dangerous((X+1,Y)).
applicable(facing_danger, ()) :- obj(agent(west),(X,Y)), dangerous((X-1,Y)).

rule((facing(north;south;east;west),
	  objective_x_is(east;west;on_axis),
      objective_y_is(north;south;on_axis),
      touching(goal;door(closed;open);choke;none),
	  in_choke(horizontal;vertical;none),
	 ), 2).

applicable((facing(F),
			objective_x_is(OX),
			objective_y_is(OY),
			touching(T),
			in_choke(C)
		   ), ()) :- obj(agent(F), _), objective_y_is(OY), objective_x_is(OX), touching(T), in_choke(C).


% Actions are the same in every state!
abstractAction(left, left). 
abstractAction(right, right). 
abstractAction(forward, forward). 
abstractAction(pickup, pickup). 
abstractAction(drop, drop). 
abstractAction(toggle, toggle). 
abstractAction(done, done). 

% The gutter state collects all states not covered by some rule.
rule(gutterState, #sup).	
applicable(gutterState, ()).

#show choose/1.
#show abstractAction/2.

#show applicable/2.
#show nextGoal/1.
#show goal/1.
