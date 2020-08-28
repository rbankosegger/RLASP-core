from .markov_decision_procedure import MarkovDecisionProcedure

class VacuumCleanerWorld(MarkovDecisionProcedure):

    def __init__(self):

        # Start state, goal state and discount rate are all fixed for this MDP
        initial_state = {'robot(left)', 'dirty(left)', 'dirty(right)'}
        goal_state = {} # Goals defined in ASP
        discount_rate = 1

        super().__init__(initial_state, goal_state, discount_rate, 'vacuum_cleaner_world.lp')
