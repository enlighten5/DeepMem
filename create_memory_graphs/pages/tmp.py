class Prolog:
    """Easily query SWI-Prolog.
    This is a singleton class
    """

    # We keep track of open queries to avoid nested queries.
    #_queryIsOpen = False

    def real_query(self, query, maxresult, catcherrors, normalize):
        swipl_fid = PL_open_foreign_frame()


        swipl_head = PL_new_term_ref()
        swipl_args = PL_new_term_refs(2)
        swipl_goalCharList = swipl_args
        swipl_bindingList = swipl_args + 1

        PL_put_list_chars(swipl_goalCharList, query)

        swipl_predicate = PL_predicate("pyrun", 2, None)

        plq = catcherrors and (PL_Q_NODEBUG|PL_Q_CATCH_EXCEPTION) or PL_Q_NORMAL
        swipl_qid = PL_open_query(None, plq, swipl_predicate, swipl_args)
        #swipl_qid = PL_open_query(module, plq, swipl_predicate, swipl_args)
        #Prolog._queryIsOpen = True # From now on, the query will be considered open
        try:
            while maxresult and PL_next_solution(swipl_qid):
                maxresult -= 1
                bindings = []
                swipl_list = PL_copy_term_ref(swipl_bindingList)
                t = getTerm(swipl_list)
                if normalize:
                    try:
                        v = t.value
                    except AttributeError:
                        v = {}
                        for r in [x.value for x in t]:
                            v.update(r)
                    yield v
                else:
                    yield t

            if PL_exception(swipl_qid):
                term = getTerm(PL_exception(swipl_qid))

                raise PrologError("".join(["Caused by: '", query, "'. ",
                                               "Returned: '", str(term), "'."]))

        finally: # This ensures that, whatever happens, we close the query
            print "closing query", swipl_qid
            PL_cut_query(swipl_qid)
            PL_discard_foreign_frame(swipl_fid)
            #Prolog._queryIsOpen = False

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
    def consult(cls, filename, catcherrors=False):
        next(cls.query(filename.join(["consult('", "')"]), catcherrors=catcherrors))
    @classmethod
    def query_new(cls, query, catcherrors=False):
        next(cls.query(query, catcherrors=False))
    @classmethod
    def query(cls, query, maxresult=-1, catcherrors=True, normalize=True):
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
        return cls.real_query(query, maxresult, catcherrors, normalize)