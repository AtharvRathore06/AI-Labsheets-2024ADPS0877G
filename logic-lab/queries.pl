:- consult('planner.pl').
t(G) :- ( call(G) -> R = true ; R = false ), format("?- ~w.  ~w~n", [G, R]).
:- t(can_move(a,b)), t(can_move(a,c)),
   t(valid_move(a,b)), t(valid_move(b,c)), t(valid_move(a,c)),
   t(valid_plan([a,b,c])), t(valid_plan([a,c])),
   t(reduce_speed).
:- halt.
