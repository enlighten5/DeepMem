use_module(library(clpfd)).

isint(4).
isint(8).

iscomm(16).


possible_pid(Pid_offset, Tgid_offset, MM_offset) :- 
    isint(Pid_offset),
    isint(Tgid_offset),
    Tgid_offset is Pid_offset + 4,

    iscomm(MM_offset),
    MM_offset > Pid_offset.
    
