import os
import sys
import unittest
from unittest.mock import MagicMock, patch
from collections import defaultdict, deque

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Framework imports
from mdp import BlocksWorld, VacuumCleanerWorldBuilder
from policy import QTablePolicy 
from control import *
import random

class GuidedPolicy:
    """ A very simple policy for testing purposes.
    """

    def __init__(self, actions):
        self.actions = deque(actions)

    def is_new_state(self, state):
        return False

    def suggest_action_for_state(self, state):
        return self.actions.popleft() 

    def initialize_state(*args):
        return
    
    def update(*args):
        return

class TestControl(unittest.TestCase):

    def test_episode_time_limit(self):

        # If a time limit is set, the control algorithm should stop after reaching that limit.

        target_policy = QTablePolicy()
        behavior_policy = GuidedPolicy(['move(right)', 'move(left)']*100)
        control = OffPolicyControl(target_policy, behavior_policy)
        control.policy_update_after_step = MagicMock()

        mdp = VacuumCleanerWorldBuilder().build_mdp()
        mdp.transition = MagicMock(return_value = ('some_next_state', -1))
        control.learn_episode(mdp, step_limit=3)

        self.assertEqual(3, len(control.policy_update_after_step.mock_calls))
        self.assertEqual(3, len(mdp.transition.mock_calls))


    def test_qlearning_updates_both_policies(self):

        target_policy = QTablePolicy()
        behavior_policy= QTablePolicy()
        control = QLearningControl(target_policy, behavior_policy, alpha=0.2)

        mdp = VacuumCleanerWorldBuilder().build_mdp()
        control.learn_episode(mdp, step_limit=3)

        self.assertEqual(target_policy._q_table, behavior_policy._q_table)

    def test_qlearning_control_1(self):

        target_policy = QTablePolicy()
        behavior_policy = GuidedPolicy(['vacuum', 'move(right)', 'vacuum'])
        control = QLearningControl(target_policy, behavior_policy, alpha=0.3)

        mdp = VacuumCleanerWorldBuilder().build_mdp()
        control.learn_episode(mdp)

        s0 = frozenset({'robot(left)', 'dirty(left)', 'dirty(right)'})
        self.assertEqual(-0.3, target_policy.value_for(s0, 'vacuum'))
        self.assertEqual(0, target_policy.value_for(s0, 'move(right)'))

        s1 = frozenset({'robot(left)', 'dirty(right)'})
        self.assertEqual(-0.3, target_policy.value_for(s1, 'move(right)'))

        s2 = frozenset({'robot(right)', 'dirty(right)'})
        self.assertEqual(99 * 0.3, target_policy.value_for(s2, 'vacuum'))
        self.assertEqual(0, target_policy.value_for(s2, 'move(left)'))

    def test_qlearning_reversed_updates_both_policies(self):

        target_policy = QTablePolicy()
        behavior_policy= QTablePolicy()
        control = QLearningReversedUpdateControl(target_policy, behavior_policy, alpha=0.2)

        mdp = VacuumCleanerWorldBuilder().build_mdp()
        control.learn_episode(mdp, step_limit=3)

        self.assertEqual(target_policy._q_table, behavior_policy._q_table)

    def test_qlearning_reversed_update_control_1(self):

        target_policy = QTablePolicy()
        behavior_policy = GuidedPolicy(['vacuum', 'move(right)', 'vacuum'])
        control = QLearningReversedUpdateControl(target_policy, behavior_policy, alpha=0.2)

        mdp_builder = VacuumCleanerWorldBuilder()
        mdp = mdp_builder.build_mdp()
        control.learn_episode(mdp)

        s0 = frozenset({'robot(left)', 'dirty(left)', 'dirty(right)'})
        self.assertEqual(0.2 * (-1 + 0.2 * (-1 + (0.2 * 99))), target_policy.value_for(s0, 'vacuum'))
        self.assertEqual(0, target_policy.value_for(s0, 'move(right)'))

        s1 = frozenset({'robot(left)', 'dirty(right)'})
        self.assertEqual(0.2 * (-1 + (0.2 * 99)), target_policy.value_for(s1, 'move(right)'))

        s2 = frozenset({'robot(right)', 'dirty(right)'})
        self.assertEqual(0.2 * 99, target_policy.value_for(s2, 'vacuum'))
        self.assertEqual(0, target_policy.value_for(s2, 'move(left)'))

        # After being guided to the goal, the target policy should know the way to the goal.
        test_mdp = mdp_builder.build_mdp()
        self.assertSetEqual(s0, test_mdp.state)
        self.assertEqual('vacuum', target_policy.suggest_action_for_state(test_mdp.state))
        test_mdp.transition('vacuum')
        self.assertEqual('move(right)', target_policy.suggest_action_for_state(test_mdp.state))
        test_mdp.transition('move(right)')
        self.assertEqual('vacuum', target_policy.suggest_action_for_state(test_mdp.state))
        test_mdp.transition('vacuum')
        self.assertEqual(None, target_policy.suggest_action_for_state(test_mdp.state))


    def test_monte_carlo_control_1(self):

        target_policy = QTablePolicy()
        behavior_policy_1 = GuidedPolicy([
            'move(right)', 'move(left)', 
            'move(right)', 'move(left)', 
            'vacuum', 'move(right)', 'vacuum'])
        behavior_policy_2 = GuidedPolicy([
            'move(right)', 'vacuum', 
            'move(left)', 'vacuum'])

        control = FirstVisitMonteCarloControl(target_policy)

        # Even though this Monte-Carlo control is on-policy, we "cheat" for testing purposes
        # and give it a separate behavior policy.
        control.behavior_policy = behavior_policy_1

        mdp = VacuumCleanerWorldBuilder().build_mdp()
        control.learn_episode(mdp)

        s0 = frozenset({'robot(left)', 'dirty(left)', 'dirty(right)'})
        self.assertEqual(97, target_policy.value_for(s0, 'vacuum')) 
        self.assertEqual(93, target_policy.value_for(s0, 'move(right)')) # Only first visit counts

        s1 = frozenset({'robot(left)', 'dirty(right)'})
        self.assertEqual(98, target_policy.value_for(s1, 'move(right)'))

        s2 = frozenset({'robot(right)', 'dirty(right)'})
        self.assertEqual(99, target_policy.value_for(s2, 'vacuum'))
        self.assertEqual(0, target_policy.value_for(s2, 'move(left)'))

        s3 = frozenset({'robot(right)', 'dirty(left)', 'dirty(right)'})
        self.assertEqual(0, target_policy.value_for(s3, 'vacuum'))
        self.assertEqual(94, target_policy.value_for(s3, 'move(left)'))

        # Let's try a second episode with a different route

        # Even though this Monte-Carlo control is on-policy, we "cheat" for testing purposes
        # and give it a separate behavior policy.
        control.behavior_policy = behavior_policy_2

        mdp = VacuumCleanerWorldBuilder().build_mdp()
        control.learn_episode(mdp)

        s0 = frozenset({'robot(left)', 'dirty(left)', 'dirty(right)'})
        self.assertEqual(97, target_policy.value_for(s0, 'vacuum')) 
        self.assertEqual((93+96)/2.0, target_policy.value_for(s0, 'move(right)'))

        s1 = frozenset({'robot(left)', 'dirty(right)'})
        self.assertEqual(98, target_policy.value_for(s1, 'move(right)'))

        s2 = frozenset({'robot(right)', 'dirty(right)'})
        self.assertEqual(99, target_policy.value_for(s2, 'vacuum'))
        self.assertEqual(0, target_policy.value_for(s2, 'move(left)'))

        s3 = frozenset({'robot(right)', 'dirty(left)', 'dirty(right)'})
        self.assertEqual(97, target_policy.value_for(s3, 'vacuum'))
        self.assertEqual(94, target_policy.value_for(s3, 'move(left)'))

    def test_monte_carlo_sgd_control_1(self):

        target_policy = QTablePolicy()
        behavior_policy = GuidedPolicy(['vacuum', 'move(right)', 'vacuum'])
        control = MonteCarloSGDControl(target_policy, alpha=0.4)

        # Even though this Monte-Carlo control is on-policy, we "cheat" for testing purposes
        # and give it a separate behavior policy.
        control.behavior_policy = behavior_policy

        mdp = VacuumCleanerWorldBuilder().build_mdp()
        control.learn_episode(mdp)

        s0 = frozenset({'robot(left)', 'dirty(left)', 'dirty(right)'})
        self.assertEqual(0.4*97, target_policy.value_for(s0, 'vacuum'))
        self.assertEqual(0, target_policy.value_for(s0, 'move(right)'))

        s1 = frozenset({'robot(left)', 'dirty(right)'})
        self.assertEqual(0.4*98, target_policy.value_for(s1, 'move(right)'))

        s2 = frozenset({'robot(right)', 'dirty(right)'})
        self.assertEqual(0.4*99, target_policy.value_for(s2, 'vacuum'))
        self.assertEqual(0, target_policy.value_for(s2, 'move(left)'))
