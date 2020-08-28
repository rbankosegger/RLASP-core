from typing import Dict, Tuple, Set
import random

from mdp import MarkovDecisionProcedure

State = Set[str]
Action = str

class SimpleMonteCarloControl:
    def __init__(self, initial_value_estimate: float = 0.0, update_every_visit: bool = False):

        self.initial_value_estimate: float = initial_value_estimate
        self.update_every_visit: bool = update_every_visit

        self.visits: Dict[State, Dict[Action, int]] = dict()
        self.action_value_estimates: Dict[State, Dict[Action, float]] = dict()
        self.current_best_actions: Dict[State, Action] = dict()
        self.available_actions: Dict[State, Set[Action]] = dict()

    def initialize_unexplored_state(self, state: State, available_actions: Set[Action]):

        self.visits[state] = dict()
        self.action_value_estimates[state] = dict()

        for action in available_actions:
            self.visits[state][action] = 0
            self.action_value_estimates[state][action] = self.initial_value_estimate

    def suggest_action_for_state(self, state: State) -> Action:
        return self.current_best_actions.get(state, None) 

    def iterate_policy_with_episode(self, mdp):

        visited_state_action_pairs = set()

        for state, action, return_ in zip(mdp.state_history, mdp.action_history, mdp.return_history):

            is_first_visit = (state, action) not in visited_state_action_pairs

            if is_first_visit or self.update_every_visit:

                self.evaluate_policy(state, action, return_) 
                self.improve_policy(state, action)

                visited_state_action_pairs.add((state, action))

    def evaluate_policy(self, state: State, action: Action, return_: float):

        self.visits[state][action] += 1

        q = self.action_value_estimates[state][action]
        v = float(self.visits[state][action])
        self.action_value_estimates[state][action] += (return_ - q) / v 

    def improve_policy(self, state: State, action: Action):

        available_estimates = self.action_value_estimates[state].items()

        current_maximal_estimate = max(v for _,v in available_estimates) 

        current_optimal_actions = [a for (a, v) in available_estimates if v==current_maximal_estimate]

        self.current_best_actions[state] = random.choice(current_optimal_actions)


class SgdMonteCarloControl:

    def __init__(self, step_size_parameter: float, initial_value_estimate: float = 0.0) :

        self.initial_value_estimate: float = initial_value_estimate
        self.step_size_parameter: float = step_size_parameter

        self.action_value_estimates: Dict[State, Dict[Action, float]] = dict()
        self.current_best_actions: Dict[State, Action] = dict()
        self.available_actions: Dict[State, Set[Action]] = dict()

    def initialize_unexplored_state(self, state: State, available_actions):

        self.action_value_estimates[state] = dict()

        for action in available_actions:
            self.action_value_estimates[state][action] = self.initial_value_estimate

    def suggest_action_for_state(self, state: State) -> Action:

        return self.current_best_actions.get(state, None) 

    def iterate_policy_with_episode(self, states, actions, returns):

        for state, action, return_ in zip(states, actions, returns):

            self.evaluate_policy(state, action, return_) 
            self.improve_policy(state, action)

    def evaluate_policy(self, state: State, action: Action, return_: float):

        q = self.action_value_estimates[state][action]
        self.action_value_estimates[state][action] += self.step_size_parameter * (return_ - q) * 1 
        #TODO: Double-check if gradient is 1!

    def improve_policy(self, state: State, action: Action):

        available_estimates = self.action_value_estimates[state].items()

        current_maximal_estimate = max(v for _,v in available_estimates) 

        current_optimal_actions = [a for (a, v) in available_estimates if v==current_maximal_estimate]

        self.current_best_actions[state] = random.choice(current_optimal_actions)

