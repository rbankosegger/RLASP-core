% 3-blocks world example carcass from Otterlo's PhD thesis (2008) p. 253, example 5.2.1

cState("s1",1).
cStateCovers("s1", (A,B,C)) :- on(A,B), on(B,floor), on(C,floor), A!=B, B!=C.
cActionCovers("a11", move(A,C)) :- cStateChoice("s1"), cStateCovers("s1", (A,B,C)), move(A,C).
cActionCovers("a12", move(C,A)) :- cStateChoice("s1"), cStateCovers("s1", (A,B,C)), move(C,A).
cActionCovers("a13", move(A,floor)) :- cStateChoice("s1"), cStateCovers("s1", (A,B,C)), move(A,floor).

cState("s2",2).
cStateCovers("s2", (A,B,C)) :- on(A,floor), on(B,floor), on(C,floor), A!=B, B!=C, A!=C.
cActionCovers("a21", move(A,B)) :- cStateChoice("s2"), cStateCovers("s2", (A,B,C)), move(A,B).
cActionCovers("a22", move(B,A)) :- cStateChoice("s2"), cStateCovers("s2", (A,B,C)), move(B,A).
cActionCovers("a23", move(A,C)) :- cStateChoice("s2"), cStateCovers("s2", (A,B,C)), move(A,C).
cActionCovers("a24", move(C,A)) :- cStateChoice("s2"), cStateCovers("s2", (A,B,C)), move(C,A).
cActionCovers("a25", move(B,C)) :- cStateChoice("s2"), cStateCovers("s2", (A,B,C)), move(B,C).
cActionCovers("a26", move(C,B)) :- cStateChoice("s2"), cStateCovers("s2", (A,B,C)), move(C,B).

cState("s3",3).
cStateCovers("s3", (A,B,C)) :- on(A,B), on(B,C), on(C,floor), A!=B, B!=C, C!=floor.
cActionCovers("a31", move(A,floor)) :- cStateChoice("s3"), cStateCovers("s3", (A,B,C)), move(A,floor).

1 = { cStateChoice(R) : cStateCovers(R, _) }.
