from .markov_decision_procedure import MarkovDecisionProcedure

class VacuumCleanerWorld(MarkovDecisionProcedure):

    def __init__(self):

        # Start state, goal state and discount rate are all fixed for this MDP
        state_initial = {'robot(left)', 'dirty(left)', 'dirty(right)'}
        state_static = {} # No static components for this MDP.
        discount_rate = 1

        super().__init__(state_initial, state_static, discount_rate, 'vacuum_cleaner_world.lp')

class VacuumCleanerWorldBuilder:

    def build_mdp(self):
        return VacuumCleanerWorld()
