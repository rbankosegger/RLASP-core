import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Framework imports
from policy import RandomPolicy
import random

class TestRandomPolicy(unittest.TestCase):

    def test_new_state(self):

        policy = RandomPolicy()

        self.assertTrue(policy.is_new_state(state='s1'))

        policy.initialize_state(state='s1', available_actions={'a(1)', 'a(2)'})
        self.assertFalse(policy.is_new_state('s1'))

    def test_random_recommendation_in_available_actions(self):

        pol = RandomPolicy()
        pol.initialize_state('s1', available_actions={'a1', 'a2', 'a3'})

        a0 = pol.suggest_action_for_state('s1')
        self.assertTrue(a0 in {'a1', 'a2', 'a3'})

    def test_random_choice_called(self):

        policy = RandomPolicy()
        policy.initialize_state('s1', available_actions=['a1', 'a2', 'a3'])

        mocked_random_choice = MagicMock(return_value='a2')

        # If the state is not yet known, a random available action is returned.
        with patch('random.choice', mocked_random_choice):

            a0 = policy.suggest_action_for_state('s1')

            # Result is determined by the mocked "random" choice
            self.assertEqual('a2', a0)

            # Arguments of the mocked "random" choice should be available actions
            mocked_random_choice.assert_called_with(['a1', 'a2', 'a3'])

    def test_random_choice_for_terminal_state(self):

        policy = RandomPolicy()
        policy.initialize_state(state='terminal', available_actions=set())
        suggestion = policy.suggest_action_for_state('terminal')

        self.assertIsNone(suggestion)

