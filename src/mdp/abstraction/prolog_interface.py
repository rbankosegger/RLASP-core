from pyswip.prolog import Prolog
from multiprocessing import Process, Queue

class PrologInterface:

    def run_query(self, knowledge_base=[], queries=[], consult_file=None):
        """
        Starts a second process to run the queries.
        This is to ensure that the knowledge base is wiped clean after every call to `run_query`!
        """

        def worker(kb,queries,outq):

            p = Prolog()

            if consult_file:
                p.consult(consult_file)

            for formula in knowledge_base:
                p.assertz(formula)

            if isinstance(queries, list):
                
                results = []
                for q in queries:
                    computed_answers = list(p.query(q))
                    results.append(computed_answers)

                outq.put(results)

            else:
                computed_answers = p.query(queries)

                outq.put(list(computed_answers))

            #computed_answers = list(p.query(query))
            #return computed_answers

        mp_q = Queue()
        mp_p = Process(target=worker, args=(knowledge_base,queries,mp_q))
        mp_p.start()
        mp_r = mp_q.get()
        mp_p.join()
        

        return mp_r

