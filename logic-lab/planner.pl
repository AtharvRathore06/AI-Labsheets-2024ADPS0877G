% Warehouse map as facts
connected(a,b).
connected(b,a).
connected(b,c).
connected(c,b).

can_move(X,Y) :- connected(X,Y).
valid_move(X,Y) :- connected(X,Y).

% Check a whole list of moves, e.g. valid_plan([a,b,c]).
valid_plan([_]).
valid_plan([X,Y|Rest]) :- valid_move(X,Y), valid_plan([Y|Rest]).

% Task 8
wet_road.
slippery :- wet_road.
reduce_speed :- slippery.
