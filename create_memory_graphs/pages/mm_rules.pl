possible_mm_struct(X) :- 
    ispointer(X),
    ispointer(X1),
    X1 is X + 8,
    ispointer(X2),
    X2 is X1 + 8,
    ispointer(X3),
    X3 is X2 + 8.