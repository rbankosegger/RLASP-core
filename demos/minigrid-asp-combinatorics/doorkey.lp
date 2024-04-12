% Use ASP to generate the state space of DoorKey 8x8 v0

width(8).
height(8).
x(0..W-1) :- width(W).
y(0..H-1) :- height(H).
xy(X,Y) :- x(X), y(Y).

% Layout generation
wall(X,0) :- x(X).
wall(X,H-1) :- height(H), x(X).
wall(0,Y) :- y(Y).
wall(W-1,Y) :- width(W), y(Y).
1 = { doorPos(X,Y) : X=2..W-3, Y=1..H-3} :- width(W), height(H).
wall(X,Y1) :- y(Y1), doorPos(X,Y2), Y1!=Y2.

% State generation
1 = { doorState(o;c;l) }.
1 = { agentPos(X,Y) : x(X), y(Y)}.
1 = { agentDir(n;s;e;a) }.
1 >= { keyPos(X,Y) : x(X), y(Y)}.
keyInInventory :- not keyPos(_,_).

% Objects can't be in the same location:
:- wall(X,Y), agentPos(X,Y).
:- wall(X,Y), keyPos(X,Y).
:- wall(X,Y), doorPos(X,Y).
:- agentPos(X,Y), keyPos(X,Y).
:- agentPos(X,Y), doorPos(X,Y), not doorState(o).
:- keyPos(X,Y), doorPos(X,Y).

% If the door is still locked, the agent can't be on the right side.
:- agentPos(X1,_), doorPos(X2,_), X1>=X2, doorState(l).
:- keyPos(X1,_), doorPos(X2,_), X1>=X2, doorState(l).

% Uncomment these to get initial states
% In initial states, the key can't be picked up and the door must be locked.
:- keyInInventory.
doorState(l).

%:- doorPos(N,_), N!=5.

#show agentPos/2.
#show keyPos/2.
#show doorPos/2.
%#show wall/2.
#show agentDir/1.
#show doorState/1.
