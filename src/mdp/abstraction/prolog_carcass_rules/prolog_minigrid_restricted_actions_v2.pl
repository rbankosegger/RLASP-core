% Domain knowledge

:- dynamic obj/2.
:- dynamic carries/1.

blocked(XY) :- obj(wall(_), XY).
blocked(XY) :- obj(lava, XY). 

gap((X,Y2), horizontal) :- blocked((X,Y1)), Y2 is Y1+1, \+ blocked((X,Y2)), Y3 is Y2+1, blocked((X,Y3)).
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

% Collect edges by computing the cross product of edges in the same room, for every room
collectEdges(_,[],[]).
collectEdges(Vertices,[R|Rooms],Result) :-
	verticesInRoom(Vertices,R,InRoom),
	product(InRoom,InRoom,NewEdges),
	collectEdges(Vertices,Rooms,Edges),
	append(Edges,NewEdges,Result).
verticesInRoom([],_,[]).
verticesInRoom([V|Vs],R,[V|Result]) :-
	inRoom(V,R),
	verticesInRoom(Vs,R,Result).
verticesInRoom([V|Vs],R,Result) :-
	\+ inRoom(V,R),
	verticesInRoom(Vs,R,Result).
inRoom((X,Y),[[X1,Y1],[X2,Y2]]) :- X>=X1, Y>=Y1, X2>=X,Y2>=Y.
product([],_,[]).
product([A|As],Bs,Result) :- product2(A,Bs,Result1), product(As,Bs,Result2), append(Result1,Result2,Result).
product2(_,[],[]).
product2(A,[B|Bs],[[A,B]|Result]) :- 
		\+ A=B,
		product2(A,Bs,Result).
product2(A,[B|Bs],Result) :- 
		A=B,
		product2(A,Bs,Result).

% Use breath-first search to find the shortest path
% BFS Algorithm as in https://book.simply-logical.space/src/text/2_part_ii/5.3.html
bfs(_, [[XY|Path]|_],[XY|Path]) :- obj(goal,XY).
bfs(SortedEdges, [Current|Rest],Goal) :- 
		filteredChildPaths(SortedEdges,Current,_,Filtered), 
		append(Rest,Filtered,NewAgenda),
		bfs(SortedEdges,NewAgenda,Goal).
filteredChildPaths(Edges,[U|Path],Children,Filtered) :- 
		allChildPaths(Edges,[U|Path],Children),
		removeLockedDoors(Children,Filtered).
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
getSortedEdges(Sorted) :-
	findall(U,v(U),Vertices), 
	findall(R,room(R),Rooms), 
	collectEdges(Vertices,Rooms,Edges),
	sortEdges(Edges,Sorted).
sortEdges(Edges,Sorted):-
	distList(Edges,DistMap),
	keysort(DistMap,SortedWithKey),
	pairs_values(SortedWithKey,Sorted).
distList([],[]).
distList([[U,V]|Others], [D-[U,V]|Result]) :- distToAgent(V,D), distList(Others,Result).
distToAgent(U,D) :- obj(agent(_),V), dist(U,V,D).
dist((X1,Y1),(X2,Y2),D) :- D is abs(X2-X1)+abs(Y2-Y1).

% Choose the first valid path to the goal. BFS guarantees that it is the shortest one.
nextOnPath(U) :- p([_|[U|_]]).
p(PathToGoal) :- 
	getSortedEdges(Edges),
	obj(agent(_),U), 
	bfs(Edges,[[U]],PathToGoalReverse), 
	reverse(PathToGoalReverse,PathToGoal), !.

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

preds([facing(F),objective_x_is(OX),objective_y_is(OY),touching(T),in_gap(C)]) :- 
		obj(goal,_),
		nextOnPath(Next), 
		obj(agent(F), _),
		objective_x_is(Next,OX),
		objective_y_is(Next,OY), 
 		touching(Next,T), 
		in_gap(C).
preds([]) :- \+ obj(goal,_).

%	%%%%%%%%%%%%%%%%%%% CARCASS RULES %%%%%%%%%%%%%%%%%%%

% Informs the system that the clauses of the specified predicate(s) might not be together in the source file.
:- discontiguous applicable/3.
:- discontiguous rule/3.
:- discontiguous abstractAction/2.

not_min_choice(Preds, I1) :- rule(Preds,R2,I2), I2<I1, applicable(Preds,R2,_). 
choose(R) :- preds(Preds), rule(Preds,R,I), applicable(Preds,R,_), \+ not_min_choice(Preds,I), !.
	
rule(_,facing_danger, 1).
	
dangerous(XY) :- obj(ball(blue), XY).
dangerous(XY) :- obj(lava, XY).
applicable(_,facing_danger, []) :- facing(T), dangerous(T).
	
rule(Preds,Preds,2).
applicable(Preds, Preds, []) :- \+ Preds=[], rule(Preds,Preds,2).

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
rule(_,gutter_custom_actions, 1.0Inf).	
applicable(_,gutter_custom_actions, []).
