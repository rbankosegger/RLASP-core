% Domain knowledge


% Carcass rules
%
% rule(R,N)										... rule R is the Nth rule to choose from
% applicable(R, (arg1, arg2, ...)) 				... rule $ is applicable with args
% choose(R) 									... rule R was chosen
% abstractAction(abstract(...), ground(...))	... abstract action `abstract(...)` is available and has a corresponding ground action `ground(...)`.

% carries defines items that are carried by the agent.
#defined carries/1.

agent(XY) :- obj(agent(_), XY).
dangerous(XY) :- obj(ball(blue), XY).
dangerous(XY) :- obj(lava, XY).

blocked(XY) :- obj(wall(_), XY).
blocked(XY) :- obj(lava, XY). 
gap((X,Y), horizontal) :- not blocked((X,Y)), blocked((X,Y-1)), blocked((X,Y+1)).
gap((X,Y), vertical) :- not blocked((X,Y)), blocked((X-1,Y)), blocked((X+1,Y)).

alley((X,Y)) :- gap((X,Y), horizontal), gap((X+1,Y), horizontal). 
alley((X,Y)) :- gap((X,Y), horizontal), gap((X-1,Y), horizontal). 
alley((X,Y)) :- gap((X,Y), vertical), gap((X,Y+1), vertical). 
alley((X,Y)) :- gap((X,Y), vertical), gap((X,Y-1), vertical). 

possibleCornerPiece(U) :- blocked(U).
possibleCornerPiece(U) :- gap(U,_), not alley(U).

rtl((X,Y)) :- possibleCornerPiece((X,Y)), possibleCornerPiece((X+1,Y)), possibleCornerPiece((X,Y+1)). % Rectangle Top Left etc.
rbl((X,Y)) :- possibleCornerPiece((X,Y)), possibleCornerPiece((X+1,Y)), possibleCornerPiece((X,Y-1)).
rtr((X,Y)) :- possibleCornerPiece((X,Y)), possibleCornerPiece((X-1,Y)), possibleCornerPiece((X,Y+1)).
rbr((X,Y)) :- possibleCornerPiece((X,Y)), possibleCornerPiece((X-1,Y)), possibleCornerPiece((X,Y-1)).

rect(((X1,Y1), (X2,Y2))) :- rtl((X1,Y1)), rbl((X1,Y2)), rtr((X2,Y1)), rbr((X2,Y2)), X2-X1>0, Y2-Y1>0.
contains(((X11,Y11), (X12,Y12)), ((X21,Y21),(X22,Y22))) :- rect(((X11,Y11),(X12,Y12))), rect(((X21,Y21),(X22,Y22))),
	X11 <= X21, Y11 <= Y21, X12 >= X22, Y12 >= Y22, ((X11,Y11),(X12,Y12))!=((X21,Y21),(X22,Y22)).
room(R) :- rect(R), not contains(R,_).

v(U) :- obj(door(_,_), U).
v(U) :- obj(goal, U).
v(U) :- obj(agent(_), U).
v(U) :- obj(key(_), U).
v(U) :- obj(ball(C), U), not C = blue.
v(U) :- gap(U,_), not alley(U).

inRoom((X,Y),((X1,Y1),(X2,Y2))) :- v((X,Y)), room(((X1,Y1), (X2,Y2))), X1<=X, Y1<=Y, X2>=X,Y2>=Y.
e(U,V) :- v(U), v(V), inRoom(U,R), inRoom(V,R), U!=V.

p(0, U) :- obj(agent(_), U).
0 { p(T+1, V) : e(U,V) } 1 :- p(T,U), T<#count{ X : v(X) }.
:- obj(goal,_), 0 = #count{ U : p(_,U), obj(goal,U) }.
:~ p(T,_). [1@2, T]
:~ p(1,(X1,Y1)), agent((X2,Y2)), D=|X2-X1|+|Y2-Y1|. [D@1]

% Make sure the agent gets the key before.
needsKeyBefore(C,T) :- p(T, U), obj(door(C,locked), U), not carries(key(C)).
keyOnPath(C,T) :- p(T,U), obj(key(C), U).
:- 0 = #count{ T : keyOnPath(C,T), T<T1}, needsKeyBefore(C,T1).

nextOnPath(V) :- p(1,V).

facing((X,Y-1)) :- obj(agent(north),(X,Y)).
facing((X,Y+1)) :- obj(agent(south),(X,Y)).
facing((X+1,Y)):- obj(agent(east),(X,Y)).
facing((X-1,Y)):- obj(agent(west),(X,Y)).

objective_y_is(north) :- agent((AX,AY)), nextOnPath((GX,GY)), AY > GY.
objective_y_is(south) :- agent((AX,AY)), nextOnPath((GX,GY)), AY < GY.
objective_y_is(on_axis) :- agent((AX,AY)), nextOnPath((GX,GY)), AY = GY.

objective_x_is(east) :- agent((AX,AY)), nextOnPath((GX,GY)), AX < GX.
objective_x_is(west) :- agent((AX,AY)), nextOnPath((GX,GY)), AX > GX.
objective_x_is(on_axis) :- agent((AX,AY)), nextOnPath((GX,GY)), AX = GX.

adj((X+1, Y)) :- agent((X,Y)).
adj((X-1, Y)) :- agent((X,Y)).
adj((X, Y+1)) :- agent((X,Y)).
adj((X, Y-1)) :- agent((X,Y)).

touching(goal) :- nextOnPath(G), adj(G), obj(goal, G).
touching(key) :- nextOnPath(G), adj(G), obj(key(_),G).
touching(door(S)) :- nextOnPath(G), adj(G), obj(door(_, S), G).
touching(gap) :- nextOnPath(G), adj(G), gap(G,_), not alley(G), not touching(goal), not touching(door(_)), not touching(key).
touching(none) :- not touching(goal), not touching(door(_)), not touching(gap), not touching(key).

in_gap(D) :- agent(XY), gap(XY,D), not alley(XY).
in_gap(none) :- not in_gap(horizontal), not in_gap(vertical).


%%%%%%%%%%%%%%%%%%% CARCASS RULES %%%%%%%%%%%%%%%%%%%

1 { choose(R) : applicable(R, _) } 1.
:- choose(R), rule(R,N), rule(R2,N2), applicable(R2, _), N2 < N.

rule(facing_danger, 1).

applicable(facing_danger, ()) :- facing(T), dangerous(T).

%rule((facing(north;south;east;west),
%	  objective_x_is(east;west;on_axis),
%      objective_y_is(north;south;on_axis),
%      touching(goal;door(closed;open;locked);gap;none;key),
%	  in_gap(horizontal;vertical;none),
%	 ), 2).

preds((facing(F),
			objective_x_is(OX),
			objective_y_is(OY),
			touching(T),
			in_gap(C)
		   )) :- obj(agent(F), _), objective_y_is(OY), objective_x_is(OX), touching(T), in_gap(C).
rule(C, 2) :- preds(C).
applicable(C, ()) :- preds(C).



% Turing left, right is always possible
abstractAction(left, left). 
abstractAction(right, right). 

% Moving forward is only possible when there are no obstacles in the way
forwardMoveBlocked :- facing(XY), obj(wall(_), XY).
forwardMoveBlocked :- facing(XY), obj(door(_, closed), XY).
forwardMoveBlocked :- facing(XY), obj(door(_, locked), XY).
forwardMoveBlocked :- facing(XY), obj(key(_), XY).
%	forwardMoveBlocked :- facing(XY), not tile(XY).
abstractAction(forward, forward) :- not forwardMoveBlocked.

% Picking up action makes sense only if agent is facing a key or other object.
abstractAction(pickup, pickup) :- facing(XY), obj(key(_), XY). 

% Toggle action only makes sense in front of the door (or other items)
abstractAction(toggle, toggle) :- facing(XY), obj(door(_, _), XY). 

% Drop action makes only sense when an item (e.g. key) is carried and when there is free space.
abstractAction(drop, drop) :- carries(_), not forwardMoveBlocked. 

% `Done` action never does anything -> Ignore it completely!
% abstractAction(gutterAction, done). 

% The gutter state collects all states not covered by some rule.
rule(gutterState, #sup).	
applicable(gutterState, ()).

#show choose/1.
#show abstractAction/2.

% #show applicable/2.
% #show rule/2.
% #show touching/1.
% #show p/2.

