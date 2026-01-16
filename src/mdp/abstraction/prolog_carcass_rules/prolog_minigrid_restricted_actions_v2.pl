% Domain knowledge


% Carcass rules
%
% rule(R,N)										... rule R is the Nth rule to choose from
% applicable(R, (arg1, arg2, ...)) 				... rule $ is applicable with args
% choose(R) 									... rule R was chosen
% abstractAction(abstract(...), ground(...))	... abstract action `abstract(...)` is available and has a corresponding ground action `ground(...)`.

obj(wall(grey),(8,0)).
obj(agent(west),(15,3)).
obj(wall(grey),(9,5)).
obj(wall(grey),(0,5)).
obj(wall(grey),(18,6)).
obj(wall(grey),(18,7)).
obj(wall(grey),(13,9)).
obj(wall(grey),(0,10)).
obj(wall(grey),(18,10)).
obj(wall(grey),(3,0)).
obj(wall(grey),(18,16)).
obj(wall(grey),(18,14)).
obj(wall(grey),(7,9)).
obj(wall(grey),(9,7)).
obj(wall(grey),(0,15)).
obj(wall(grey),(8,9)).
obj(wall(grey),(5,9)).
obj(wall(grey),(14,18)).
obj(wall(grey),(2,9)).
obj(wall(grey),(18,13)).
obj(wall(grey),(4,0)).
obj(wall(grey),(9,18)).
obj(wall(grey),(17,0)).
obj(wall(grey),(3,18)).
obj(wall(grey),(6,0)).
obj(wall(grey),(0,18)).
obj(wall(grey),(1,0)).
obj(wall(grey),(16,18)).
obj(wall(grey),(18,9)).
obj(wall(grey),(18,1)).
obj(wall(grey),(0,7)).
obj(wall(grey),(12,0)).
obj(wall(grey),(9,12)).
obj(wall(grey),(15,0)).
obj(wall(grey),(18,4)).
obj(wall(grey),(9,10)).
obj(wall(grey),(16,9)).
obj(wall(grey),(0,11)).
obj(wall(grey),(18,8)).
obj(wall(grey),(9,17)).
obj(wall(grey),(11,18)).
obj(wall(grey),(4,18)).
obj(wall(grey),(1,18)).
obj(wall(grey),(18,15)).
obj(wall(grey),(0,4)).
obj(wall(grey),(0,6)).
obj(wall(grey),(18,17)).
obj(wall(grey),(5,18)).
obj(wall(grey),(18,5)).
obj(wall(grey),(14,0)).
obj(wall(grey),(9,1)).
obj(wall(grey),(10,0)).
obj(wall(grey),(8,18)).
obj(wall(grey),(17,18)).
obj(wall(grey),(2,18)).
obj(wall(grey),(9,14)).
obj(wall(grey),(1,9)).
obj(wall(grey),(16,0)).
obj(wall(grey),(18,2)).
obj(wall(grey),(3,9)).
obj(wall(grey),(14,9)).
obj(wall(grey),(0,1)).
obj(wall(grey),(9,15)).
obj(wall(grey),(18,3)).
obj(wall(grey),(6,18)).
obj(wall(grey),(0,2)).
obj(wall(grey),(0,13)).
obj(wall(grey),(10,18)).
obj(wall(grey),(0,14)).
obj(wall(grey),(9,0)).
obj(wall(grey),(0,12)).
obj(wall(grey),(9,6)).
obj(wall(grey),(9,3)).
obj(wall(grey),(0,8)).
obj(wall(grey),(18,11)).
obj(wall(grey),(7,18)).
obj(wall(grey),(7,0)).
obj(wall(grey),(9,9)).
obj(wall(grey),(9,11)).
obj(wall(grey),(11,0)).
obj(wall(grey),(2,0)).
obj(wall(grey),(15,18)).
obj(wall(grey),(18,18)).
obj(wall(grey),(0,3)).
obj(wall(grey),(11,9)).
obj(wall(grey),(6,9)).
obj(wall(grey),(12,18)).
obj(wall(grey),(0,16)).
obj(wall(grey),(18,12)).
obj(wall(grey),(9,16)).
obj(wall(grey),(0,17)).
obj(wall(grey),(9,8)).
obj(wall(grey),(0,9)).
obj(wall(grey),(18,0)).
obj(goal,(2,11)).
obj(wall(grey),(5,0)).
obj(wall(grey),(9,4)).
obj(wall(grey),(13,0)).
obj(wall(grey),(13,18)).
obj(wall(grey),(12,9)).
obj(wall(grey),(10,9)).
obj(wall(grey),(0,0)).
obj(wall(grey),(15,9)).

% obj(wall(grey),(4,7)).
% obj(wall(grey),(5,6)).
% obj(wall(grey),(0,6)).
% obj(wall(grey),(2,7)).
% obj(wall(grey),(5,2)).
% obj(wall(grey),(7,7)).
% obj(wall(grey),(0,7)).
% obj(wall(grey),(5,7)).
% obj(wall(grey),(5,3)).
% obj(door(yellow,locked),(5,5)).
% obj(wall(grey),(7,0)).
% obj(wall(grey),(0,2)).
% obj(wall(grey),(7,4)).
% obj(wall(grey),(0,5)).
% obj(wall(grey),(0,3)).
% obj(wall(grey),(0,0)).
% obj(wall(grey),(6,0)).
% obj(key(yellow),(2,3)).
% obj(wall(grey),(0,4)).
% obj(agent(east),(2,6)).
% obj(wall(grey),(7,5)).
% obj(wall(grey),(0,1)).
% obj(wall(grey),(2,0)).
% obj(wall(grey),(7,6)).
% obj(wall(grey),(1,0)).
% obj(wall(grey),(3,0)).
% obj(wall(grey),(4,0)).
% obj(wall(grey),(7,1)).
% obj(wall(grey),(5,4)).
% obj(wall(grey),(5,0)).
% obj(wall(grey),(1,7)).
% obj(goal,(6,6)).
% obj(wall(grey),(7,3)).
% obj(wall(grey),(3,7)).
% obj(wall(grey),(5,1)).
% obj(wall(grey),(7,2)).
% obj(wall(grey),(6,7)).

%obj(wall(grey),(2,0)).
%obj(wall(grey),(4,3)).
%obj(wall(grey),(4,0)).
%obj(key(yellow),(1,2)).
%obj(goal,(3,3)).
%obj(wall(grey),(1,0)).
%obj(wall(grey),(2,3)).
%obj(wall(grey),(0,1)).
%obj(agent(north),(1,3)).
%obj(wall(grey),(4,4)).
%obj(wall(grey),(0,2)).
%obj(door(yellow,locked),(2,2)).
%obj(wall(grey),(0,0)).
%obj(wall(grey),(2,1)).
%obj(wall(grey),(1,4)).
%obj(wall(grey),(2,4)).
%obj(wall(grey),(4,1)).
%obj(wall(grey),(4,2)).
%obj(wall(grey),(0,3)).
%obj(wall(grey),(0,4)).
%obj(wall(grey),(3,4)).
%obj(wall(grey),(3,0)).

%obj(wall(grey),(0,1)).
%obj(wall(grey),(2,0)).
%obj(wall(grey),(2,2)).
%obj(wall(grey),(0,6)).
%obj(goal,(6,6)).
%obj(wall(grey),(7,2)).
%obj(wall(grey),(4,7)).
%obj(wall(grey),(3,0)).
%obj(wall(grey),(2,5)).
%obj(wall(grey),(3,7)).
%obj(key(yellow),(1,6)).
%obj(agent(south),(1,3)).
%obj(wall(grey),(7,6)).
%obj(door(yellow,locked),(2,4)).
%%carries(key(yellow)).
%obj(wall(grey),(7,0)).
%obj(wall(grey),(0,2)).
%obj(wall(grey),(0,0)).
%obj(wall(grey),(7,5)).
%obj(wall(grey),(6,0)).
%obj(wall(grey),(0,4)).
%obj(wall(grey),(0,3)).
%obj(wall(grey),(5,0)).
%obj(wall(grey),(4,0)).
%obj(wall(grey),(2,3)).
%obj(wall(grey),(5,7)).
%obj(wall(grey),(1,0)).
%obj(wall(grey),(7,7)).
%obj(wall(grey),(2,1)).
%obj(wall(grey),(1,7)).
%obj(wall(grey),(7,1)).
%obj(wall(grey),(2,7)).
%obj(wall(grey),(0,7)).
%obj(wall(grey),(6,7)).
%obj(wall(grey),(7,3)).
%obj(wall(grey),(7,4)).
%obj(wall(grey),(2,6)).
%obj(wall(grey),(0,5)).

:- dynamic obj/2.
:- dynamic carries/1.

blocked(XY) :- obj(wall(_), XY).
blocked(XY) :- obj(lava, XY). 

%gap((X,Y), horizontal) :- \+ blocked((X,Y)), blocked((X,Y1)), Y1 is Y-1, blocked((X,Y2)), Y2 is Y+1.
gap((X,Y2), horizontal) :- blocked((X,Y1)), Y2 is Y1+1, \+ blocked((X,Y2)), Y3 is Y2+1, blocked((X,Y3)).
%gap((X,Y), vertical) :- blocked((X-1,Y)), blocked((X+1,Y)), \+ blocked((X,Y)).
gap((X2,Y), vertical) :- blocked((X1,Y)), X2 is X1+1, \+ blocked((X2,Y)), X3 is X2+1, blocked((X3,Y)).

alley((X,Y)) :- gap((X,Y), horizontal), X1 is X+1, gap((X1,Y), horizontal). 
alley((X,Y)) :- gap((X,Y), horizontal), X1 is X-1, gap((X1,Y), horizontal). 
alley((X,Y)) :- gap((X,Y), vertical), Y1 is Y+1, gap((X,Y1), vertical). 
alley((X,Y)) :- gap((X,Y), vertical), Y1 is Y-1, gap((X,Y1), vertical). 

% pcp = possibleCornerPiece
pcp(U) :- blocked(U).
pcp(U) :- gap(U,_), \+ alley(U).

rtl((X,Y)) :- pcp((X,Y)), X1 is X+1, pcp((X1,Y)), Y1 is Y+1, pcp((X,Y1)). % Rectangle Top Left etc.
rbl((X,Y)) :- pcp((X,Y)), X1 is X+1, pcp((X1,Y)), Y1 is Y-1, pcp((X,Y1)).
rtr((X,Y)) :- pcp((X,Y)), X1 is X-1, pcp((X1,Y)), Y1 is Y+1, pcp((X,Y1)).
rbr((X,Y)) :- pcp((X,Y)), X1 is X-1, pcp((X1,Y)), Y1 is Y-1, pcp((X,Y1)).

rect([[X1,Y1], [X2,Y2]]) :- rtl((X1,Y1)), rbl((X1,Y2)), rtr((X2,Y1)), rbr((X2,Y2)), X2-X1>0, Y2-Y1>0.
contains([[X11,Y11],[X12,Y12]], [[X21,Y21],[X22,Y22]]) :- rect([[X11,Y11],[X12,Y12]]), rect([[X21,Y21],[X22,Y22]]), \+ [[X11,Y11],[X12,Y12]]=[[X21,Y21],[X22,Y22]], X21>=X11, Y21>=Y11, X12>=X22, Y12>=Y22.
room(R) :- rect(R), \+ contains(R,_).

v(U) :- obj(door(_,_), U).
v(U) :- obj(goal, U).
v(U) :- obj(agent(_), U).
v(U) :- obj(key(_), U).
v(U) :- obj(ball(C), U), \+ C=blue.
v(U) :- gap(U,_), \+ alley(U), \+ obj(door(_,_), U).

verticesInRoom([],_,[]).
verticesInRoom([V|Vs],R,[V|Result]) :-
	inRoom2(V,R),
	verticesInRoom(Vs,R,Result).
verticesInRoom([V|Vs],R,Result) :-
	\+ inRoom2(V,R),
	verticesInRoom(Vs,R,Result).
		
collectEdges(_,[],[]).
collectEdges(Vertices,[R|Rooms],Result) :-
	verticesInRoom(Vertices,R,InRoom),
	product(InRoom,InRoom,NewEdges),
	collectEdges(Vertices,Rooms,Edges),
	append(Edges,NewEdges,Result).

product2(_,[],[]).
product2(A,[B|Bs],[[A,B]|Result]) :- 
		\+ A=B,
		product2(A,Bs,Result).
product2(A,[B|Bs],Result) :- 
		A=B,
		product2(A,Bs,Result).
product([],_,[]).
product([A|As],Bs,Result) :- product2(A,Bs,Result1), product(As,Bs,Result2), append(Result1,Result2,Result).
	

inRoom((X,Y),((X1,Y1),(X2,Y2))) :- v((X,Y)), room([[X1,Y1], [X2,Y2]]), X>=X1, Y>=Y1, X2>=X,Y2>=Y.
e(U,V) :- v(U), v(V), inRoom(U,R), inRoom(V,R), \+ U=V.

inRoom2((X,Y),[[X1,Y1],[X2,Y2]]) :- X>=X1, Y>=Y1, X2>=X,Y2>=Y.
e2(U,V,R) :- inRoom2(U,R), inRoom2(V,R), \+ U=V.

% Use breath-first search to find the shortest path
% BFS Algorithm as in https://book.simply-logical.space/src/text/2_part_ii/5.3.html
bfs([[XY|Path]|_],[XY|Path]) :- obj(goal,XY).
bfs([Current|Rest],Goal) :- childrenPaths(Current,Children), append(Rest,Children,NewAgenda),bfs(NewAgenda,Goal).
childrenPaths([U|Path],SortedChildren) :- 
		findall([V,U|Path], e(U,V), Children),
		removeLockedDoors(Children, FilteredChildren),
		sortedChildrenPaths(FilteredChildren,SortedChildren).

bfs2(_, [[XY|Path]|_],[XY|Path]) :- obj(goal,XY).
bfs2(SortedEdges, [Current|Rest],Goal) :- 
		childrenPaths2(SortedEdges,Current,_,Filtered), 
		append(Rest,Filtered,NewAgenda),
		bfs2(SortedEdges,NewAgenda,Goal).
childrenPaths2(Edges,[U|Path],Children,Filtered) :- 
		allChildPaths(Edges,[U|Path],Children),
		%findall([V,U|Path], e(U,V), Children),
		removeLockedDoors(Children,Filtered).

% bfs(Edges, [[XY|Path]|_],[XY|Path]) :- obj(goal,XY).
% bfs(Edges, [Current|Rest],Goal) :- 
% 		childrenPaths(Edges, Current,Children), 
% 		append(Rest,Children,NewAgenda),bfs(NewAgenda,Goal).
%

childrenPaths2(Edges, [U|_],SortedChildren) :- 
		childrenOf(Edges, U, SortedChildren).

childrenOf([], _, []).
childrenOf([[U,V]|Rest], U, [V|Children]) :- childrenOf(Rest, U, Children).
childrenOf([[W,_]|Rest], U, Children) :- \+ W=U, childrenOf(Rest, U, Children).

allChildPaths([], _, []).
allChildPaths([[U,V]|Edges], [U|Path], [[V,U|Path]|Children]) :- allChildPaths(Edges, [U|Path], Children).
allChildPaths([[W,_]|Edges], [U|Path], Children) :- \+ W=U, allChildPaths(Edges, [U|Path], Children).

% Filter out children nodes representing a locked door and with no fitting key on the path so far.
keysOnPath([],[]).
keysOnPath([U|Us],[key(Color)|Keys]) :- obj(key(Color), U), keysOnPath(Us, Keys).
keysOnPath([U|Us],Keys) :- \+ obj(key(_), U), keysOnPath(Us, Keys).
removeLockedDoors([], []).
removeLockedDoors([[U|Us]|RestOfPath], [[U|Us]|Filtered]) :-
	\+ obj(door(_,locked), U),
	removeLockedDoors(RestOfPath, Filtered).
removeLockedDoors([[U|Us]|RestOfPath], [[U|Us]|Filtered]) :-
	obj(door(Color,locked), U),
	carries(key(Color)),
	removeLockedDoors(RestOfPath, Filtered).
removeLockedDoors([[U|Us]|RestOfPath], [[U|Us]|Filtered]) :-
	obj(door(Color,locked), U),
	\+ carries(key(_)),
	keysOnPath(Us, Keys),
	member(key(Color),Keys),
	removeLockedDoors(RestOfPath, Filtered).
removeLockedDoors([[U|Us]|RestOfPath], Filtered) :-
	obj(door(Color,locked), U),
	\+ carries(key(Color)),
	keysOnPath(Us, Keys),
	\+ member(key(Color),Keys),
	removeLockedDoors(RestOfPath, Filtered).

% Sort children by their distance to the agent
dist((X1,Y1),(X2,Y2),D) :- D is abs(X2-X1)+abs(Y2-Y1).
distToAgent(U,D) :- obj(agent(_),V), dist(U,V,D).
distList([],[]).
distList([[U|Us]|Others], [D-[U|Us]|Result]) :- distToAgent(U,D), distList(Others,Result).
distList2([],[]).
distList2([U|Others], [D-U|Result]) :- distToAgent(U,D), distList2(Others,Result).
distList3([],[]).
distList3([[U,V]|Others], [D-[U,V]|Result]) :- distToAgent(V,D), distList3(Others,Result).
sortedNodes(Nodes,Sorted):-
		distList2(Nodes,DistMap),
		keysort(DistMap,SortedWithKey),
		pairs_values(SortedWithKey,Sorted).

sortedChildrenPaths(Children, Sorted):-
		distList(Children,DistMap),
		keysort(DistMap,SortedWithKey),
		pairs_values(SortedWithKey,Sorted).

sortEdges(Edges,Sorted):-
	distList3(Edges,DistMap),
	keysort(DistMap,SortedWithKey),
	pairs_values(SortedWithKey,Sorted).

getSortedEdges(Sorted) :-
	findall(U,v(U),Vertices), 
	findall(R,room(R),Rooms), 
	collectEdges(Vertices,Rooms,Edges),
	sortEdges(Edges,Sorted).
% Choose the first valid path to the goal. BFS guarantees that it is the shortest one.
p(PathToGoal) :- 
	getSortedEdges(Edges),
	obj(agent(_),U), 
	bfs2(Edges,[[U]],PathToGoalReverse), 
	reverse(PathToGoalReverse,PathToGoal), !.
nextOnPath(U) :- p([_|[U|_]]).

facing((X,Y1)) :- obj(agent(north),(X,Y)), Y1 is Y-1.
facing((X,Y1)) :- obj(agent(south),(X,Y)), Y1 is Y+1.
facing((X1,Y)):- obj(agent(east),(X,Y)), X1 is X+1.
facing((X1,Y)):- obj(agent(west),(X,Y)), X1 is X-1.
	
objective_y_is((_,Y), north) :- obj(agent(_),(_,AY)), AY>Y.
objective_y_is((_,Y), south) :- obj(agent(_),(_,AY)), Y>AY.
objective_y_is((_,Y), on_axis) :- obj(agent(_),(_,Y)).

objective_x_is((X,_), east) :- obj(agent(_),(AX,_)), X>AX.
objective_x_is((X,_), west) :- obj(agent(_),(AX,_)), AX>X.
objective_x_is((X,_), on_axis) :- obj(agent(_),(X,_)).

adj((X1, Y)) :- obj(agent(_),(X,Y)), X1 is X+1.
adj((X1, Y)) :- obj(agent(_),(X,Y)), X1 is X-1.
adj((X, Y1)) :- obj(agent(_),(X,Y)), Y1 is Y+1.
adj((X, Y1)) :- obj(agent(_),(X,Y)), Y1 is Y-1.

touching(G, goal) :- adj(G), obj(goal, G).
touching(G, key) :- adj(G), obj(key(_),G).
touching(G, door(S)) :- adj(G), obj(door(_, S), G).
touching(G, gap) :- adj(G), gap(G,_), \+ alley(G), \+ touching(G,goal), \+ touching(G,door(_)), \+ touching(G,key).
touching(G, none) :- \+ touching(G,goal), \+ touching(G,door(_)), \+ touching(G,gap), \+ touching(G,key).

in_gap(D) :- obj(agent(_),XY), gap(XY,D), \+ alley(XY).
in_gap(none) :- \+ in_gap(horizontal), \+ in_gap(vertical).
%	
%	
%	%%%%%%%%%%%%%%%%%%% CARCASS RULES %%%%%%%%%%%%%%%%%%%
%
% Informs the system that the clauses of the specified predicate(s) might not be together in the source file.
:- discontiguous applicable/2.
:- discontiguous rule/2.
:- discontiguous abstractAction/2.

not_min_choice(R1) :- applicable(R1,_), rule(R1,I1), applicable(R2,_), rule(R2,I2), I2<I1.
choose(R) :- rule(R,_), applicable(R,_), \+ not_min_choice(R), !.
	
rule(facing_danger, 1).
	
dangerous(XY) :- obj(ball(blue), XY).
dangerous(XY) :- obj(lava, XY).
applicable(facing_danger, []) :- facing(T), dangerous(T).
%	
%	%rule((facing(north;south;east;west),
%	%	  objective_x_is(east;west;on_axis),
%	%      objective_y_is(north;south;on_axis),
%	%      touching(goal;door(closed;open;locked);gap;none;key),
%	%	  in_gap(horizontal;vertical;none),
%	%	 ), 2).
%	
preds([facing(F),objective_x_is(OX),objective_y_is(OY),touching(T),in_gap(C)]) :- 
		nextOnPath(Next), 
		obj(agent(F), _),
		objective_x_is(Next,OX),
		objective_y_is(Next,OY), 
 		touching(Next,T), 
		in_gap(C).
rule(C, 2) :- preds(C).
applicable(C, []) :- preds(C).

% Turing left, right is always possible
abstractAction(left, left). 
abstractAction(right, right). 

% Moving forward is only possible when there are no obstacles in the way
forwardMoveBlocked :- facing(XY), obj(wall(_), XY).
forwardMoveBlocked :- facing(XY), obj(door(_, closed), XY).
forwardMoveBlocked :- facing(XY), obj(door(_, locked), XY).
forwardMoveBlocked :- facing(XY), obj(key(_), XY).
%	forwardMoveBlocked :- facing(XY), not tile(XY).
abstractAction(forward, forward) :- \+ forwardMoveBlocked.

% Picking up action makes sense only if agent is facing a key or other object.
abstractAction(pickup, pickup) :- facing(XY), obj(key(_), XY). 

% Toggle action only makes sense in front of the door (or other items)
abstractAction(toggle, toggle) :- facing(XY), obj(door(_, _), XY). 

% Drop action makes only sense when an item (e.g. key) is carried and when there is free space.
abstractAction(drop, drop) :- carries(_), \+ forwardMoveBlocked. 

% `Done` action never does anything -> Ignore it completely!
% abstractAction(gutterAction, done). 

% The gutter state collects all states not covered by some rule.
rule(gutter_custom_actions, 1.0Inf).	
applicable(gutter_custom_actions, []).
