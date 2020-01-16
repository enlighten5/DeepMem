class Prolog:
    """Easily query SWI-Prolog.
    This is a singleton class
    """

    # We keep track of open queries to avoid nested queries.
    _queryIsOpen = False

    class _QueryWrapper(object):

        def __init__(self):
            if Prolog._queryIsOpen:
                raise NestedQueryError("The last query was not closed")

        def __call__(self, *terms, **kwargs, maxresult, catcherrors, normalize):
            for key in kwargs:
                if key not in ["flags", "module"]:
                    raise Exception("Invalid kwarg: %s" % key, key)
            
            flags = kwargs.get("flags", PL_Q_NODEBUG|PL_Q_CATCH_EXCEPTION)
            module = kwargs.get("module", None)

            t = terms[0]
            for tx in terms[1:]:
                t = _comma(t, tx)
            
            f = Functor.fromTerm(t)
            p = PL_pred(f.handle, module)
            swipl_qid = PL_open_query(module, flags, p, f.a0)

            swipl_fid = PL_open_foreign_frame()
            print "Prolog query wrapper call", query, "module", module

            Prolog._queryIsOpen = True # From now on, the query will be considered open
            try:
                while maxresult and PL_next_solution(swipl_qid):
                    maxresult -= 1
                    bindings = []
                    swipl_list = PL_copy_term_ref(swipl_bindingList)
                    t = getTerm(swipl_list)
                    print "t", t
                    if normalize:
                        try:
                            v = t.value
                            print "v=t.value=", v
                        except AttributeError:
                            v = {}
                            for r in [x.value for x in t]:
                                v.update(r)
                            print "v{}", v
                        yield v
                    else:
                        yield t

                if PL_exception(swipl_qid):
                    term = getTerm(PL_exception(swipl_qid))

                    raise PrologError("".join(["Caused by: '", query, "'. ",
                                               "Returned: '", str(term), "'."]))

            finally: # This ensures that, whatever happens, we close the query
                PL_cut_query(swipl_qid)
                PL_discard_foreign_frame(swipl_fid)
                Prolog._queryIsOpen = False

    @classmethod
    def asserta(cls, assertion, catcherrors=False):
        next(cls.query(assertion.join(["asserta((", "))."]), catcherrors=catcherrors))

    @classmethod
    def assertz(cls, assertion, catcherrors=False):
        next(cls.query(assertion.join(["assertz((", "))."]), catcherrors=catcherrors))

    @classmethod
    def dynamic(cls, term, catcherrors=False):
        next(cls.query(term.join(["dynamic((", "))."]), catcherrors=catcherrors))

    @classmethod
    def retract(cls, term, catcherrors=False):
        next(cls.query(term.join(["retract((", "))."]), catcherrors=catcherrors))

    @classmethod
    def retractall(cls, term, catcherrors=False):
        next(cls.query(term.join(["retractall((", "))."]), catcherrors=catcherrors))

    @classmethod
    def consult(cls, filename, module, catcherrors=False):
        next(cls.query(filename.join(["consult('", "')"]), module, catcherrors=catcherrors))

    @classmethod
    def query(cls, *terms, **kwargs, maxresult=-1, catcherrors=True, normalize=True):
        """Run a prolog query and return a generator.
        If the query is a yes/no question, returns {} for yes, and nothing for no.
        Otherwise returns a generator of dicts with variables as keys.

        >>> prolog = Prolog()
        >>> prolog.assertz("father(michael,john)")
        >>> prolog.assertz("father(michael,gina)")
        >>> bool(list(prolog.query("father(michael,john)")))
        True
        >>> bool(list(prolog.query("father(michael,olivia)")))
        False
        >>> print sorted(prolog.query("father(michael,X)"))
        [{'X': 'gina'}, {'X': 'john'}]
        """
        return cls._QueryWrapper()(*terms, **kwargs, maxresult, catcherrors, normalize)