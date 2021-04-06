from .markov_decision_procedure import MarkovDecisionProcedure

class VacuumCleanerWorld(MarkovDecisionProcedure):

    def __init__(self):

        # Start state, goal state and discount rate are all fixed for this MDP
        state_initial = {'robot(left)', 'dirty(left)', 'dirty(right)'}
        state_static = {} # No static components for this MDP.
        discount_rate = 1

        super().__init__(state_initial, state_static, discount_rate, 'vacuum_cleaner_world.lp')

class VacuumCleanerWorldBuilder:

    def __init__(self):
        sample_mdp = VacuumCleanerWorld()

        self.mdp_interface_file_path = sample_mdp.interface_file_path
        self.mdp_problem_file_path = sample_mdp.problem_file_path
        self.mdp_state_static = sample_mdp.state_static

    def build_mdp(self):
        return VacuumCleanerWorld()
