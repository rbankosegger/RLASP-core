import os
import sys
import unittest

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

# Framework imports
from mdp import SlidingPuzzle

class TestSlidingPuzzle(unittest.TestCase):


    def test_available_actions_1(self):

        mdp = SlidingPuzzle(state_initial={'on(p0,1,0)'},
                          state_static={'size(2)', 'subgoal(p0,0,0)'})
        self.assertSetEqual({'move(p0,0,0)','move(p0,1,1)'},
                         mdp.available_actions)

    def test_available_actions_2(self):

        mdp = SlidingPuzzle(state_initial={'on(p0,1,0)', 'on(p1,1,1)'},
                          state_static={'size(2)', 'subgoal(p0,0,0)', 'subgoal(p1,0,1)'})
        self.assertSetEqual({'move(p0,0,0)', 'move(p1,0,1)'},
                         mdp.available_actions)

    def test_available_actions_3(self):

        mdp = SlidingPuzzle(state_initial={'on(p0,1,0)', 'on(p1,0,1)'},
                          state_static={'size(2)', 'subgoal(p0,0,0)', 'subgoal(p1,0,1)'})
        self.assertEqual({'move(p0,0,0)', 'move(p0,1,1)', 'move(p1,0,0)', 'move(p1,1,1)'},
                         mdp.available_actions)

    def test_available_actions_4(self):

        mdp = SlidingPuzzle(state_initial={'on(p0,0,0)', 'on(p1,1,1)'},
                          state_static={'size(2)', 'subgoal(p0,0,0)', 'subgoal(p1,0,1)'})

        # Available actions should be updated after state transitions.
        mdp.transition('move(p1,1,0)')
        self.assertEqual({'move(p0,0,1)', 'move(p1,1,1)'},
                         mdp.available_actions)

    def test_available_actions_5(self):

        mdp = SlidingPuzzle(state_initial={'on(p0,0,0)', 'on(p1,0,1)'},
                          state_static={'size(2)', 'subgoal(p0,0,0)', 'subgoal(p1,0,1)'})

        # No actions available in the goal state
        self.assertEqual(set(),
                         mdp.available_actions)

    def test_state_transition(self):

        # Transition to arbitrary state
        mdp = SlidingPuzzle(state_initial={'on(p0,0,0)', 'on(p1,1,0)'},
                          state_static={'size(2)', 'subgoal(p0,0,0)', 'subgoal(p1,0,1)'})

        next_state, next_reward = mdp.transition('move(p1,1,1)')
        self.assertEqual({'on(p0,0,0)', 'on(p1,1,1)'}, next_state)
        self.assertEqual(-1, next_reward)
        self.assertEqual({'on(p0,0,0)', 'on(p1,1,1)'}, mdp.state)

        next_state, next_reward = mdp.transition('move(p1,0,1)')
        self.assertEqual({'on(p0,0,0)', 'on(p1,0,1)'}, next_state)
        self.assertEqual(99, next_reward)
        self.assertEqual({'on(p0,0,0)', 'on(p1,0,1)'}, mdp.state)

        # Check if trajectory is correct: S0, A0, R1, S1, A1, R2, S2
        self.assertEqual({'on(p0,0,0)', 'on(p1,1,0)'}, mdp.state_history[0]) # S0
        self.assertEqual('move(p1,1,1)', mdp.action_history[0]) # A0
        self.assertEqual(-1, mdp.reward_history[1]) # R1
        self.assertEqual({'on(p0,0,0)', 'on(p1,1,1)'}, mdp.state_history[1]) #S1
        self.assertEqual('move(p1,0,1)', mdp.action_history[1]) # A1
        self.assertEqual(100-1, mdp.reward_history[2]) # R2
        self.assertEqual({'on(p0,0,0)', 'on(p1,0,1)'}, mdp.state_history[2]) #S2

    def test_returns_1(self):

        # Optimal way to goal
        mdp = SlidingPuzzle(state_initial={'on(p0,1,0)', 'on(p1,0,1)'},
                          state_static = {'size(2)', 'subgoal(p0,0,0)', 'subgoal(p1,0,1)'})
        mdp.transition('move(p0,0,0)')

        # G[t] = R[t+1] + ...
        self.assertEqual(mdp.return_history[0], 99)


    def test_returns_2(self):

        # Undiscounted return

        mdp = SlidingPuzzle(state_initial={'on(p0,1,1)', 'on(p1,1,0)'},
                          state_static = {'size(2)', 'subgoal(p0,0,0)', 'subgoal(p1,0,1)'})
        mdp.transition('move(p0,0,1)')
        mdp.transition('move(p0,0,0)')
        mdp.transition('move(p1,1,1)')
        mdp.transition('move(p1,0,1)')

        # G[t] = R[t+1] + R[t+2] + R[t+3] + R[t+4]
        self.assertEqual(mdp.return_history[0], -1 + -1 + -1 + 99)
        self.assertEqual(mdp.return_history[1], -1 + -1 + 99)
        self.assertEqual(mdp.return_history[2], -1 + 99)
        self.assertEqual(mdp.return_history[3], 99)
        self.assertEqual(mdp.return_history[4], 0) # Return is zero in terminal state
