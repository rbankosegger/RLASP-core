from pyswip.prolog import Prolog
from multiprocessing import Process, Queue

class PrologInterface:

    def run_query(self, knowledge_base, query):
        """
        Starts second process to run the query.
        This is to ensure that the knowledge base is wiped clean after every query!
        """

        def worker(kb,query,outq):

            p = Prolog()
            for formula in knowledge_base:
                p.assertz(formula)

            computed_answers = p.query(query)

            outq.put(list(computed_answers))

            #computed_answers = list(p.query(query))
            #return computed_answers

        mp_q = Queue()
        mp_p = Process(target=worker, args=(knowledge_base,query,mp_q))
        mp_p.start()
        mp_r = mp_q.get()
        mp_p.join()

        return mp_r

