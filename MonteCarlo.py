# Vanilla imports
import random

# 3rd party imports
from tqdm import tqdm

# Custom imports
from control import SimpleMonteCarloControl 
from mdp import MarkovDecisionProcedure
from planner import Planner

class MonteCarlo:
    def __init__(self, mdp_builder, planner: Planner, max_episode_length: int, 
                 planning_factor: float, plan_on_empty_policy: bool, 
                 control = None):
        """Sets all required properties for the learning process.

        :param blocks_world: the blocks world
        :param max_episode_length: the maximum number of steps in an episode, should be at least 2*(n-1), n = number of blocks
        :param planning_factor: the probability for invoking the planning component at each step
        :param plan_on_empty_policy: enable/disable the use of planning on an empty policy entry
        """
        self.mdp_builder = mdp_builder
        self.planner = planner
        self.max_episode_length = max_episode_length
        self.planning_factor = planning_factor
        self.plan_on_empty_policy = plan_on_empty_policy

        if control:
            self.control = control
        else:
            self.control = SimpleMonteCarloControl(blocks_world)

        self.return_ratios = []
        self.returns = []
        self.optimal_returns = []

    def generate_episode(self) -> MarkovDecisionProcedure:
        """Generates a single episode from a start state onwards.

        :param state: the initial state
        :param policy: the current policy
        :return: a sequence of state, reward, action
        """

        mdp = self.mdp_builder.build_mdp()

        # Exploring start
        action = random.choice(list(mdp.available_actions))
        if not mdp.state in self.control.action_value_estimates:
            self.control.initialize_unexplored_state(mdp.state, mdp.available_actions)
        mdp.transition(action)
    
        
        for _ in range(self.max_episode_length - len(mdp.action_history)):

            policy_action = self.control.suggest_action_for_state(mdp.state)
            if not policy_action:
                self.control.initialize_unexplored_state(mdp.state, mdp.available_actions)

            if self.planning_factor <= random.random():
                if policy_action:
                    action = policy_action
                else:
                    self.control.initialize_unexplored_state(mdp.state, mdp.available_actions)
                    if self.plan_on_empty_policy:
                        action, _ = self.planner.suggest_next_action(mdp)
                    else:
                        action = random.choice(list(mdp.available_actions))

            else:
                action, _ = self.planner.suggest_next_action(mdp)
                if policy_action:
                    q_value_policy_action = self.control.action_value_estimates[mdp.state][policy_action]
                    q_value_planning_action = self.control.action_value_estimates[mdp.state][action]

                    if q_value_planning_action < q_value_policy_action:
                        action = policy_action


            if action is None:
                # goal reached
                break

            mdp.transition(action)

        return mdp

    def learn_policy(self, discount_rate: float, number_episodes: int, show_progress_bar: bool = False, evaluate_return_ratio = False) -> dict:
        """Uses a first-visit Exploring Starts Monte Carlo evaluation method to evaluate policy.

        :param discount_rate: the discounting factor (use only when no planning is used; set to 1 if planning is used)
        :param number_episodes: the number of episodes to run
        :param show_progress_bar: If set to true, a progress bar will be printed in the terminal to indicate how many episodes are done. This is done via the `tqdm` package.
        :param evaluate_return_ratio: If set to true, the current return is always compared to the optimal return achieved by the planner. This is an expensive computation and should be used for benchmarking only.
        :return: the learned policy as a state-action mapping
        """

        episodes = range(0, number_episodes)
        if show_progress_bar:
            episodes = tqdm(episodes, total=number_episodes, desc='Training')

        for _ in episodes:
            mdp = self.generate_episode()  # clingo IO

            if len(mdp.action_history) > 0:

                self.control.iterate_policy_with_episode(mdp.state_history, mdp.action_history, 
                                                         mdp.return_history)
    
                if evaluate_return_ratio:
                    self.evaluate_metrics_for_episode(start_state, returns[0])
                else:
                    self.returns.append(mdp.return_history[0])

    def evaluate_metrics_for_episode(self, start_state, actual_return):

        worst_case_return = -self.max_episode_length - 1
        best_case_return = self.blocks_world.optimal_return_for_state(start_state)

        return_ratio = (actual_return - worst_case_return) / float(best_case_return - worst_case_return)
        self.return_ratios.append(return_ratio)

        self.returns.append(actual_return)
        self.optimal_returns.append(best_case_return)
