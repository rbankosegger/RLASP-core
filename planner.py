import os
import clingo
from typing import Tuple

from mdp import MarkovDecisionProcedure

class Planner:

    def __init__(self, planning_horizon: int):
        self.planning_horizon: int = planning_horizon

        self.planner_file_name: str = 'planner.dl'
        self.planner_file_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.planner_file_name)

    def suggest_next_action(self, mdp: MarkovDecisionProcedure) -> Tuple[str, int]:

        ctl = clingo.Control()

        ctl.load(mdp.file_path(mdp.interface_file_name))
        ctl.load(mdp.file_path(mdp.file_name))
        ctl.load(self.planner_file_path)
        ctl.add('base', [], ' '.join(f'currentState({s}).' for s in mdp.state))
        ctl.add('base', [], ' '.join(f'{s}.' for s in mdp.state_static))
        ctl.add('base', [], f'#const t={self.planning_horizon}.')
        #ctl.add('base', [], f'action({action}).')
        ctl.add('base', [], '#show maxReturn/1. #show bestCurrentAction/1.')

        ctl.configuration.solve.models = 0  # create all stable models and find the optimal one
        ctl.ground(parts=[('base', [])])
        models = ctl.solve(yield_=True)

        model = list(models)[0]

        expected_return = None
        suggested_action = None
        
        for symbol in model.symbols(shown=True):
            if symbol.name == 'maxReturn':

                # Atom is of the form `maxReward(r)` and `r` is the expected return of the current state.

                expected_return = symbol.arguments[0].number 

            if symbol.name == 'bestCurrentAction':

                # Atom is of the form `bestCurrentAction(f(...))` and `f(...)` is an uninterpreted function,
                # corresponding to the suggested action

                suggested_action = str(symbol.arguments[0])

        return (suggested_action, expected_return)

    def compute_optimal_return(self, mdp):
        _, optimal_return = self.suggest_next_action(mdp)
        return optimal_return
