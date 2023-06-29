:- not cStateChoice("s1").
%:- not cActionChoice("a11").
:- not cActionCovers("a11",_).

% Not needed because this is already constrained when generating covered actions.
% An action can only be covered if it exists!
	%	:- actionChoice(move(1,2)), not move(1,2).
	%	:- actionChoice(move(1,3)), not move(1,3).
	%	:- actionChoice(move(2,1)), not move(2,1).
	%	:- actionChoice(move(2,3)), not move(2,3).
	%	:- actionChoice(move(3,1)), not move(3,1).
	%	:- actionChoice(move(3,2)), not move(3,2).

