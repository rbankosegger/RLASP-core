% Use ASP to generate the state space of MultiRoom-N2-S4-v0

width(25).
height(25).

% Configuration MiniGrid-MultiRoom-N2-S4-v0
% Add more rooms of different sizes as needed
room(0).
room(1).
prevRoom(0,1).
roomSize(0,(4,4)).
roomSize(1,(4,4)).

% Place the first room
1 = { roomTop(R,(X,Y)) : X=0..W-SX, Y=0..H-SY} :- room(R), R=0, width(W), height(H), roomSize(R,(SX,SY)).

% Place consecutive rooms
dir(n;s;e;w).
opposing(n,s).
opposing(s,n).
opposing(w,e).
opposing(e,w).
1 = { exitDoorWall(R,D) : dir(D) } :- room(R), prevRoom(R,_).
1 = { exitDoorPos(R,(X,Y)) : X=TX+SX-1, Y=TY+1..TY+SY-2 } :- exitDoorWall(R,e), roomSize(R,(SX,SY)), roomTop(R,(TX,TY)).
1 = { exitDoorPos(R,(X,Y)) : X=TX+1..TX+SX-2, Y=TY+SY-1 } :- exitDoorWall(R,s), roomSize(R,(SX,SY)), roomTop(R,(TX,TY)).
1 = { exitDoorPos(R,(X,Y)) : X=TX, Y=TY+1..TY+SY-2 } :- exitDoorWall(R,w), roomSize(R,(SX,SY)), roomTop(R,(TX,TY)).
1 = { exitDoorPos(R,(X,Y)) : X=TX+1..TX+SX-2, Y=TY } :- exitDoorWall(R,n), roomSize(R,(SX,SY)), roomTop(R,(TX,TY)).
entryDoorWall(R2,W2) :- exitDoorWall(R1,W1), opposing(W1,W2), prevRoom(R1,R2).
entryDoorPos(R2,XY) :- exitDoorPos(R1,XY), prevRoom(R1,R2).
1 = { roomTop(R,(X,Y)) : X=EX-SX+1, Y=EY-SY+2..EY-1 }  :- entryDoorWall(R,e), entryDoorPos(R,(EX,EY)), roomSize(R,(SX,SY)).
1 = { roomTop(R,(X,Y)) : X=EX-SX+2..EX-1, Y=EY-SY+1 }  :- entryDoorWall(R,s), entryDoorPos(R,(EX,EY)), roomSize(R,(SX,SY)).
1 = { roomTop(R,(X,Y)) : X=EX, Y=EY-SY+2..EY-1 }  :- entryDoorWall(R,w), entryDoorPos(R,(EX,EY)), roomSize(R,(SX,SY)).
1 = { roomTop(R,(X,Y)) : X=EX-SX+2..EX-1, Y=EY }  :- entryDoorWall(R,n), entryDoorPos(R,(EX,EY)), roomSize(R,(SX,SY)).

% Rooms must be contained in the grid
:- roomTop(R,(X,Y)), X<0.
:- roomTop(R,(X,Y)), Y<0.
:- roomTop(R,(X,Y)), width(W), roomSize(R,(SX,SY)), X+SX > W.
:- roomTop(R,(X,Y)), height(H), roomSize(R,(SX,SY)), Y+SY > H.

% Rooms cannot overlap. 
nonOverlap(R1,R2) :- 
	roomTop(R1,(T1X,T1Y)), roomSize(R1,(S1X,S1Y)),
	roomTop(R2,(T2X,T2Y)), roomSize(R2,(S2X,S2Y)),
	T1X+S1X <= T2X.
nonOverlap(R1,R2) :- 
	roomTop(R1,(T1X,T1Y)), roomSize(R1,(S1X,S1Y)),
	roomTop(R2,(T2X,T2Y)), roomSize(R2,(S2X,S2Y)),
	T2X+S2X <= T1X.
nonOverlap(R1,R2) :- 
	roomTop(R1,(T1X,T1Y)), roomSize(R1,(S1X,S1Y)),
	roomTop(R2,(T2X,T2Y)), roomSize(R2,(S2X,S2Y)),
	T1Y+S1Y <= T2Y.
nonOverlap(R1,R2) :- 
	roomTop(R1,(T1X,T1Y)), roomSize(R1,(S1X,S1Y)),
	roomTop(R2,(T2X,T2Y)), roomSize(R2,(S2X,S2Y)),
	T2Y+S2Y <= T1Y.
:- room(R1), room(R2), R1<R2, not nonOverlap(R1,R2), not prevRoom(R1,R2), not prevRoom(R2,R1).

% Place agent and goal inside the rooms.
insideRoom(R, (X,Y)) :- roomTop(R, (TX,TY)), roomSize(R, (SX,SY)), X=TX+1..TX+SX-2, Y=TY+1..TY+SY-2.
1 = { doorState(XY, o;c) } :- exitDoorPos(_,XY).
1 = { goalPos(XY) : insideRoom(R, XY) } :- room(R), not prevRoom(R,_).
canEnter(XY) :- insideRoom(_, XY).
canEnter(XY) :- exitDoorPos(_, XY), doorState(XY, o).
1 = { agentPos(XY) : canEnter(XY) }.
1 = { agentDir(n;w;s;e)}.

% Uncomment this line to generate only initial states!
% It constrains the agent position to the first room.
1 = { agentPos(XY) : insideRoom(R, XY) } :- room(R), not prevRoom(_,R).

#show goalPos/1.
#show roomTop/2.
#show agentPos/1.
