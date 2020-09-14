import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Framework imports
from mdp import BlocksWorld, VacuumCleanerWorldBuilder
from policy import QTablePolicy 
import random

class TestQTablePolicy(unittest.TestCase):

    def test_new_state(self):

        policy = QTablePolicy()

        self.assertTrue(policy.is_new_state(state='s1'))

        policy.initialize_state(state='s1', available_actions={'a(1)', 'a(2)'})
        self.assertFalse(policy.is_new_state('s1'))

    def test_initialized_state_action_values(self):

        current_state = 's1'
        available_actions = {'a1', 'a2'}
        policy = QTablePolicy()

        policy.initialize_state('s1', {'a1', 'a2'})
        self.assertEqual(0.0, policy.value_for('s1', 'a1'))
        self.assertEqual(0.0, policy.value_for('s1', 'a2'))

    def test_initialized_random_action_suggestion(self):

        current_state = 's1'
        available_actions = {'a1', 'a2'}
        policy = QTablePolicy()

        policy.initialize_state(current_state, available_actions)

        # If the state is not yet known, a random available action is returned.
        # We use a mock method that replaces `random.choice` for testing.
        mocked_random_choice = MagicMock(return_value='a2')
        with patch('random.choice', mocked_random_choice):

            a0 = policy.suggest_action_for_state(current_state)

            # Result is determined by the mocked "random" choice
            self.assertEqual('a2', a0)
            self.assertTrue(a0 in available_actions)

            # Arguments of the mocked "random" choice should be all available actions
            mocked_random_choice.assert_called_with(list(available_actions))

    def test_update(self):

        current_state = 's0'
        available_actions = {'a1', 'a2'}

        policy = QTablePolicy()
        policy.initialize_state('s0', {'a1', 'a2'})

        # An update of 5 for (s0, a2) should make a2 the greedy choice.
        # TODO Is this update an "abstract" one or something fixed like "reward"???
        policy.update(state='s0', action='a2', delta=5.0)
        self.assertEqual(0.0, policy.value_for('s0', 'a1'))
        self.assertEqual(5.0, policy.value_for('s0', 'a2'))
        self.assertEqual('a2', policy.suggest_action_for_state('s0'))

        # An update of 4 for (s0, a1) should keep a2 as the greedy choice.
        policy.update(state='s0', action='a1', delta=4.0)
        self.assertEqual(4.0, policy.value_for('s0', 'a1'))
        self.assertEqual(5.0, policy.value_for('s0', 'a2'))
        self.assertEqual('a2', policy.suggest_action_for_state('s0'))

        # An update of -2 for (s0, a2) should make a1 the greedy choice.
        policy.update(state='s0', action='a2', delta=-2.6)
        self.assertEqual(4.0, policy.value_for('s0', 'a1'))
        self.assertEqual(2.4, policy.value_for('s0', 'a2'))
        self.assertEqual('a1', policy.suggest_action_for_state('s0'))

    def test_tie_breaking(self):

        policy = QTablePolicy()
        policy.initialize_state('s0', ['a1', 'a2', 'a3', 'a4', 'a5', 'a6'])
        policy.update(state='s0', action='a1', delta=5.2)
        policy.update(state='s0', action='a2', delta=3.2)
        policy.update(state='s0', action='a3', delta=5.2)
        policy.update(state='s0', action='a4', delta=-6.9)
        policy.update(state='s0', action='a6', delta=5.2)

        # Multiple actions have the same state-value-estimate:
        self.assertEqual(5.2, policy.value_for('s0', 'a1'))
        self.assertEqual(5.2, policy.value_for('s0', 'a3'))
        self.assertEqual(5.2, policy.value_for('s0', 'a6'))

        # When choosing the greedy action, this tie will be broken randomly.
        # We test this by creating a mock `random.choice` and check if the
        # random choice is made between the correct options {a1, a3, a6}.
        mocked_random_choice = MagicMock(return_value='a6')
        with patch('random.choice', mocked_random_choice):

            a0 = policy.suggest_action_for_state('s0')

            # Result is determined by the mocked "random" choice
            self.assertEqual('a6', a0)

            # The random choice should only happen between optimal actions.
            mocked_random_choice.assert_called_with(['a1', 'a3', 'a6'])

    def test_terminal_state(self):

        policy = QTablePolicy()
        policy.initialize_state('s0', set()) # s0 is terminal because it has no available actions.
        
        action = policy.suggest_action_for_state('s0')
        self.assertIsNone(action)

        value = policy.value_for('s0', None)
        self.assertEqual(0, value) # Terminal states always have a value of zero.

#    def test_random_recommendation_in_available_actions(self):
#
#        s0 = {'on(b0,table)', 'on(b1,table)', 'on(b2,b1)'}
#
#        mdp = BlocksWorld(state_initial=s0, state_static={'subgoal(b1,b0)', 'subgoal(b2, b1)'})
#        pol = QTablePolicy()
#
#        a0 = pol.suggest_next_action(s0, mdp.available_actions)
#        self.assertTrue(a0 in mdp.available_actions)

#    def test_random_recommendation_update_interface(self):
#
#        s0 = {'on(b0,table)', 'on(b1,table)', 'on(b2,b1)'}
#        a0 = 'move(b2, b0)'
#
#        q_delta = -3 # A fictional update for Q(s0, a0)
#
#        pol = RandomPolicy()
#        # There are no parameters to adjust for this policy, therefore the update
#        # won't do anything. Still, the interface should be accessible.
#        pol.update(s0, a0, q_delta) 
