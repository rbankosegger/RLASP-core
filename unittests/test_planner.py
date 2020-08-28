import os
import sys
import unittest

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Framework imports
from mdp import BlocksWorld
from planner import Planner

class TestPlanner(unittest.TestCase):

    def test_blocksworld_1(self):
        
        mdp = BlocksWorld(initial_state={'on(b0,table)', 'on(b1,table)'},
                          goal_state={'on(b1,b0)'})
        planner = Planner(planning_horizon=1)
        suggested_action, expected_return = planner.suggest_next_action(mdp)
        mdp.transition(suggested_action)

        self.assertEqual('move(b1,b0)', suggested_action)
        self.assertEqual(mdp.return_history[0], expected_return)

    def test_blocksworld_2(self):
        
        mdp = BlocksWorld(initial_state={'on(b0,b1)', 'on(b1,table)'},
                          goal_state={'on(b1,b0)'})
        planner = Planner(planning_horizon=2)

        suggested_action_0, expected_return_0 = planner.suggest_next_action(mdp)
        mdp.transition(suggested_action_0)

        suggested_action_1, expected_return_1 = planner.suggest_next_action(mdp)
        mdp.transition(suggested_action_1)

        self.assertEqual('move(b0,table)', suggested_action_0)
        self.assertEqual(mdp.return_history[0], expected_return_0)

        self.assertEqual('move(b1,b0)', suggested_action_1)
        self.assertEqual(mdp.return_history[1], expected_return_1)
