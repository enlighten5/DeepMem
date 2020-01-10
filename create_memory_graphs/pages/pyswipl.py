from __future__ import print_function
from pyswip import Prolog, registerForeign

def hello(t):
    print("Hello,", t)
hello.arity = 1

registerForeign(hello)

prolog = Prolog()
prolog.assertz("father(michael,john)")
prolog.assertz("father(michael,gina)")
print(list(prolog.query("father(michael,X), hello(X)")))