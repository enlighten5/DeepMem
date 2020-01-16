from pyswip.core import *
from pyswip import *
from time import gmtime, strftime
import random
def main():
    idx = [0, 8, 16, 24, 32, 72, 112, 120, 128, 136]
    idx2 = [0, 4, 8]
    with open("./pages/kb_file.pl", "w") as kb_file:
        for val in idx:
            kb_file.write("ispointer(" + str(val) + ")." + "\n")
        for val in idx2:
            kb_file.write("isint(" + str(val) + ")." + '\n')

    assertz = Functor("assertz")
    ispointer = Functor("ispointer", 1)
    isint = Functor("isint", 1)
    print str(isint.name)
    kb = construct_kb(assertz, ispointer, idx, random.random())
    kb2 = construct_kb(assertz, ispointer, idx, "test")
    kb2 = construct_kb(assertz, isint, idx2, "test")
    X = Variable()
    q = Query(ispointer(X), module = kb)
    while q.nextSolution():
        #print(X.value)
        pass
    q.closeQuery()


    Y = Variable()
    print ("")
    registerForeign(atom_checksum, arity=2)
    q = Query(ispointer(Y), module = kb2)
    while q.nextSolution():
        #print(Y.value)
        pass
    q.closeQuery()
    p = Prolog()
    listing = Functor("listing", 1)
    p.consult("./pages/kb_file.pl", kb2)
    p.consult("./pages/rules.pl", kb2)
    Pid_offset = Variable()
    Comm_offset = Variable()
    possible_task_struct = Functor("possible_task_struct", 5)
    for s in p.query("possible_task_struct(Pid_offset, Comm_offset, MM_offset, MM_offset2)", catcherrors=False):
        print(s["Pid_offset"])

    #call(listing(ispointer))



def atom_checksum(*a):
    v = str(a[0])
    print "test", v
    return True
def construct_kb(assertz, func, dicts, kb_name, paddr=0):
    kb = newModule(str(kb_name))
    for key in dicts:
        call(assertz(func(str(key))), module=kb)
    return kb

if __name__ == "__main__":
    main()
   