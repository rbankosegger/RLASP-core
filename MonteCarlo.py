from BlocksWorld import *
from entities import State
from random import randint, random
from collections import deque
from tqdm import tqdm
from control import SimpleMonteCarloControl 


class MonteCarlo:
    def __init__(self, blocks_world: BlocksWorld, max_episode_length: int, planning_factor: float, plan_on_empty_policy: bool, planning_horizon: int, exploring_starts: bool = True, on_policy: bool = True, control = None):
        """Sets all required properties for the learning process.

        :param blocks_world: the blocks world
        :param max_episode_length: the maximum number of steps in an episode, should be at least 2*(n-1), n = number of blocks
        :param planning_factor: the probability for invoking the planning component at each step
        :param plan_on_empty_policy: enable/disable the use of planning on an empty policy entry
        :param planning_horizon: how far to plan ahead
        :param exploring_starts: enable/disable exploring starts
        :param on_policy: enable/disable on-policy behavior
        """
        self.blocks_world = blocks_world
        self.max_episode_length = max_episode_length
        self.planning_factor = planning_factor
        self.plan_on_empty_policy = plan_on_empty_policy
        self.planning_horizon = planning_horizon
        self.exploring_starts = exploring_starts
        self.on_policy = on_policy

        if control:
            self.control = control
        else:
            self.control = SimpleMonteCarloControl(blocks_world)

        self.return_ratios = []
        self.returns = []
        self.optimal_returns = []

    def generate_episode(self, start_state: State) -> deque:
        """Generates a single episode from a start state onwards.

        :param state: the initial state
        :param policy: the current policy
        :return: a sequence of state, reward, action
        """
        episode = deque()  # deque allows faster appending than array
        state = start_state
        actions = self.get_initial_actions(state)  # clingo IO

        count = 0
        while count <= self.max_episode_length:
            if self.planning_factor <= random():
                policy_action = self.control.suggest_action_for_state(state)
                if policy_action and self.on_policy:
                    if self.exploring_starts and count == 0:
                        action = self.get_random_action(actions)
                    else:
                        action = policy_action
                elif self.plan_on_empty_policy:
                    action = self.plan_action(state, self.planning_horizon)
                else:
                    action = self.get_random_action(actions)
            else:
                action = self.plan_action(state, self.planning_horizon)
                policy_action = self.control.suggest_action_for_state(state)
                if policy_action:
                    q_value_policy_action = self.control.action_value_estimates[state][policy_action]
                    q_value_planning_action = self.control.action_value_estimates[state][action]

                    if q_value_planning_action < q_value_policy_action:
                        action = policy_action

            if action is None:
                # goal reached
                break

            (nextState, nextActions, _, nextReward, _) = self.blocks_world.next_step(state, action, t=1)  # clingo IO
            episode.append((state, nextReward, action))
            state = nextState
            actions = nextActions
            count += 1

        return episode, state

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
            start_state = self.blocks_world.get_random_start_state()
            episode, _ = self.generate_episode(start_state)  # clingo IO

            if len(episode) > 0:

                returns = self.discounted_returns_for_episode(episode, discount_rate)

                states, _, actions = zip(*episode)
                self.control.iterate_policy_with_episode(states, actions, returns)
    
                if evaluate_return_ratio:
                    self.evaluate_metrics_for_episode(start_state, returns[0])
                else:
                    self.returns.append(returns[0])


    def discounted_returns_for_episode(self, episode, discount_rate):

        returns = []
        return_t = 0

        for state_t0, reward_t1, action_t0 in reversed(episode):
               
            # Compute discounted return according to definition: G[t] = R[t+1] + gamma * G[t+1]
            return_t = reward_t1 + discount_rate * return_t
            returns.append(return_t)

        returns.reverse()

        return(returns)

    def evaluate_metrics_for_episode(self, start_state, actual_return):

        worst_case_return = -self.max_episode_length - 1
        best_case_return = self.blocks_world.optimal_return_for_state(start_state)

        return_ratio = (actual_return - worst_case_return) / float(best_case_return - worst_case_return)
        self.return_ratios.append(return_ratio)

        self.returns.append(actual_return)
        self.optimal_returns.append(best_case_return)


    def get_initial_actions(self, state: State) -> list:
        """Retrieves the applicable actions for a given state.

        :param state: the current state
        :return: a list of applicable actions in that state
        """
        (_, availableActions, _, _, _) = self.blocks_world.next_step(state, None, t=0)  # clingo IO
        return availableActions

    def get_random_action(self, actions: list) -> Action:
        """Picks a random action from a list of actions.

        :param actions: a list of possible actions
        :return: a random action
        """
        if len(actions) > 0:
            rnd = randint(0, len(actions) - 1)
            return actions[rnd]
        return None

    def plan_action(self, state: State, planning_horizon: int) -> Action:
        """Getting an action recommended by the planning component.

        :param state: the current state
        :param planning_horizon: how many steps to plan ahead
        :return: an action recommended by the planning component
        """
        (_, _, bestAction, _, _) = self.blocks_world.next_step(state, None, t=planning_horizon)  # clingo IO
        return bestAction
