import os
import sys
import unittest

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Framework imports
from mdp import BlocksWorld, VacuumCleanerWorld, Sokoban, SokobanBuilder
from planner import Planner 

class TestPlanner(unittest.TestCase): 

    def test_blocksworld_1(self): 

        mdp = BlocksWorld(state_initial={'on(b0,table)', 'on(b1,table)'},
                          state_static={'subgoal(b1,b0)'})

        planner = Planner(planning_horizon=1)
        suggested_action, expected_return = planner.suggest_next_action(mdp)
        mdp.transition(suggested_action)

        self.assertEqual('move(b1,b0)', suggested_action)
        self.assertEqual(mdp.return_history[0], expected_return)

    def test_blocksworld_2(self):
        
        mdp = BlocksWorld(state_initial={'on(b0,b1)', 'on(b1,table)'},
                          state_static={'subgoal(b1,b0)'})
        planner = Planner(planning_horizon=2)

        suggested_action_0, expected_return_0 = planner.suggest_next_action(mdp)
        mdp.transition(suggested_action_0)

        suggested_action_1, expected_return_1 = planner.suggest_next_action(mdp)
        mdp.transition(suggested_action_1)

        self.assertEqual('move(b0,table)', suggested_action_0)
        self.assertEqual(mdp.return_history[0], expected_return_0)

        self.assertEqual('move(b1,b0)', suggested_action_1)
        self.assertEqual(mdp.return_history[1], expected_return_1)

    def test_blocksworld_optimal_return(self):

        mdp = BlocksWorld(state_initial={'on(b2,b1)', 'on(b0,b3)', 'on(b4,table)', 'on(b1,table)', 
                                         'on(b3,table)'},
                          state_static={'subgoal(b0,table)', 'subgoal(b1,b0)', 'subgoal(b2,b1)', 
                                        'subgoal(b3,b2)', 'subgoal(b4,b3)'})

        planner = Planner(planning_horizon=2*5+1)

        self.assertEqual(94, planner.compute_optimal_return(mdp))


    def test_vacuum_cleaner_world(self):
        mdp = VacuumCleanerWorld()
        planner = Planner(planning_horizon=4)

        suggested_action_0, expected_return_0 = planner.suggest_next_action(mdp)
        mdp.transition(suggested_action_0)

        suggested_action_1, expected_return_1 = planner.suggest_next_action(mdp)
        mdp.transition(suggested_action_1)

        suggested_action_2, expected_return_2 = planner.suggest_next_action(mdp)
        mdp.transition(suggested_action_2)

        self.assertEqual('vacuum', suggested_action_0)
        self.assertEqual(mdp.return_history[0], expected_return_0)

        self.assertEqual('move(right)', suggested_action_1)
        self.assertEqual(mdp.return_history[1], expected_return_1)

        self.assertEqual('vacuum', suggested_action_2)
        self.assertEqual(mdp.return_history[2], expected_return_2)

    def test_vacuum_cleaner_world_optimal_return(self):

        mdp = VacuumCleanerWorld()
        planner = Planner(planning_horizon=4)
        self.assertEqual(-1 + -1 + 99, planner.compute_optimal_return(mdp))

    def test_sokoban_1(self):

        builder = SokobanBuilder('suitcase-05-01')
        mdp = builder.build_mdp()
        planner = Planner(planning_horizon=7)

        s0 = mdp.state

        a0, g0 = planner.suggest_next_action(mdp)
        self.assertEqual(g0, 94)

        mdp.transition('push(6,3,left)')
        s1 = s0 - { 'sokoban(4,3)', 'box(6,3)' } | { 'sokoban(6,3)', 'box(5,3)' }
        self.assertSetEqual(s1, mdp.state)
        
        a1, g1 = planner.suggest_next_action(mdp)
        self.assertEqual(g1, 95)

    def test_sokoban_2(self):
        builder = SokobanBuilder('suitcase-05-01')
        mdp = builder.build_mdp()
        planner = Planner(planning_horizon=6)

        suggested_actions = []
        suggested_returns = []

        for i in range(20): # 20 is intentionally set to be higher than the number of needed moves.

            if len(mdp.available_actions) > 0:

                a, g = planner.suggest_next_action(mdp)

                self.assertTrue(a in mdp.available_actions)

                mdp.transition(a)
                suggested_actions += [a]
                suggested_returns += [g]

        self.assertEqual(suggested_actions, mdp.action_history)
        self.assertEqual(suggested_returns + [0], mdp.return_history)

    def test_sokoban_3(self):

        builder = SokobanBuilder(level_name='suitcase-05-02')
        mdp = builder.build_mdp()
        planner = Planner(planning_horizon=6)

        suggested_actions = []
        suggested_returns = []

        for i in range(20): # 20 is intentionally set to be higher than the number of needed moves.

            if len(mdp.available_actions) > 0:

                a, g = planner.suggest_next_action(mdp)

                self.assertNotEqual(None, a)
                self.assertNotEqual(set(), mdp.available_actions)
                self.assertTrue(a in mdp.available_actions)

                mdp.transition(a)
                suggested_actions += [a]
                suggested_returns += [g]

        self.assertEqual(suggested_actions, mdp.action_history)
        self.assertEqual(suggested_returns + [0], mdp.return_history)
