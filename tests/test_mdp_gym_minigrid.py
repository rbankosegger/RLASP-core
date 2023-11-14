import os
import sys
import unittest
import warnings

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

# Framework imports
from mdp import GymMinigrid, GymMinigridBuilder, GymMinigridCustomLevelBuilder

class TestGymMinigrid(unittest.TestCase):

    def test_available_actions(self):

        # Available actions are the same for any state.

        mdp = GymMinigridBuilder('MiniGrid-Empty-5x5-v0').build_mdp()

        self.assertSetEqual({'left', 'right', 'forward', 'pickup', 'drop', 'toggle', 'done'},
                            mdp.available_actions)


    def test_state(self):
        """

            Simple environment:

                #####
                #A  #
                #   #
                #  G#
                #####
        """

        mdp = GymMinigridBuilder('MiniGrid-Empty-5x5-v0').build_mdp()

        should_be_state = { f'obj(wall(grey),({x},0))' for x in range(0, 5) } \
                        | { f'obj(wall(grey),({x},4))' for x in range(0, 5) } \
                        | { f'obj(wall(grey),(0,{y}))' for y in range(0, 5) } \
                        | { f'obj(wall(grey),(4,{y}))' for y in range(0, 5) } \
                        | { 'obj(agent(east),(1,1))',
                            'obj(goal,(3,3))'
                          }

        self.assertSetEqual(should_be_state, mdp.state)
        self.assertSetEqual(should_be_state, mdp.ground_state)
        # TODO: Test if state also worls for keys, doors, lava, floors, etc...


    def test_state_transition(self):
        """

            Simple environment:

                #####    #####    #####    #####    #####    #####    #####
                #>  #    # > #    #  >#    #  >#    #  v#    #   #    #   #
                #   #    #   #    #   #    #   #    #   #    #  v#    #   #
                #  G#    #  G#    #  G#    #  G#    #  G#    #  G#    #  v#
                #####    #####    #####    #####    #####    #####    #####

                  forward  forward  forward    right  forward  forward
                    
        """

        static_state = { f'obj(wall(grey),({x},0))' for x in range(0, 5) } \
                     | { f'obj(wall(grey),({x},4))' for x in range(0, 5) } \
                     | { f'obj(wall(grey),(0,{y}))' for y in range(0, 5) } \
                     | { f'obj(wall(grey),(4,{y}))' for y in range(0, 5) } \
                     | { 'obj(goal,(3,3))' }

        mdp = GymMinigridBuilder('MiniGrid-Empty-5x5-v0').build_mdp()

        next_state, next_reward = mdp.transition('forward')
        self.assertEqual(static_state | {'obj(agent(east),(2,1))'},
                         next_state)
        self.assertEqual(0, next_reward)
        self.assertEqual(static_state | {'obj(agent(east),(2,1))'},
                         mdp.state)

        next_state, next_reward = mdp.transition('forward')
        self.assertEqual(static_state | {'obj(agent(east),(3,1))'},
                         next_state)
        self.assertEqual(0, next_reward)
        self.assertEqual(static_state | {'obj(agent(east),(3,1))'},
                         mdp.state)

        next_state, next_reward = mdp.transition('forward')
        self.assertEqual(static_state | {'obj(agent(east),(3,1))'},
                         next_state)
        self.assertEqual(0, next_reward)
        self.assertEqual(static_state | {'obj(agent(east),(3,1))'},
                         mdp.state)
        
        next_state, next_reward = mdp.transition('right')
        self.assertEqual(static_state | {'obj(agent(south),(3,1))'},
                         next_state)
        self.assertEqual(0, next_reward)
        self.assertEqual(static_state | {'obj(agent(south),(3,1))'},
                         mdp.state)
        
        next_state, next_reward = mdp.transition('forward')
        self.assertEqual(static_state | {'obj(agent(south),(3,2))'},
                         next_state)
        self.assertEqual(0, next_reward)
        self.assertEqual(static_state | {'obj(agent(south),(3,2))'},
                         mdp.state)
        
        next_state, next_reward = mdp.transition('forward')
        self.assertEqual((static_state | {'obj(agent(south),(3,3))', 'terminal'}) - {'obj(goal,(3,3))'},
                         next_state)

        step_count = 6
        max_steps = 100.0
        self.assertEqual(1 - 0.9 * (step_count / max_steps), next_reward)
        self.assertEqual((static_state | {'obj(agent(south),(3,3))', 'terminal'}) - {'obj(goal,(3,3))'},
                         mdp.state)

        # Check if trajectory is correct: S0, A0, R1, S1, A1, R2, S2 ...
        self.assertEqual(static_state | {'obj(agent(east),(1,1))'}, mdp.state_history[0]) # S0
        self.assertEqual('forward', mdp.action_history[0]) # A0
        self.assertEqual(0, mdp.reward_history[1]) # R1
        self.assertEqual(static_state | {'obj(agent(east),(2,1))'}, mdp.state_history[1]) # S1
        self.assertEqual('forward', mdp.action_history[1]) # A1
        self.assertEqual(0, mdp.reward_history[2]) # R2
        self.assertEqual(static_state | {'obj(agent(east),(3,1))'}, mdp.state_history[2]) # S2
        self.assertEqual('forward', mdp.action_history[2]) # A2
        self.assertEqual(0, mdp.reward_history[3]) # R3
        self.assertEqual(static_state | {'obj(agent(east),(3,1))'}, mdp.state_history[3]) # S3
        self.assertEqual('right', mdp.action_history[3]) # A3
        self.assertEqual(0, mdp.reward_history[4]) # R4
        self.assertEqual(static_state | {'obj(agent(south),(3,1))'}, mdp.state_history[4]) # S4
        self.assertEqual('forward', mdp.action_history[4]) # A4
        self.assertEqual(0, mdp.reward_history[5]) # R5
        self.assertEqual(static_state | {'obj(agent(south),(3,2))'}, mdp.state_history[5]) # S5
        self.assertEqual('forward', mdp.action_history[5]) # A5
        self.assertEqual(1 - 0.9 * (step_count / max_steps), mdp.reward_history[6]) # R6


    def test_returns(self):

        mdp = GymMinigridBuilder('MiniGrid-Empty-5x5-v0').build_mdp()

        mdp.transition('forward')
        mdp.transition('forward')
        mdp.transition('right')
        mdp.transition('forward')
        mdp.transition('forward')

        step_count = 5
        max_steps = 100.0
        final_reward = 1 - 0.9 * (step_count / max_steps)

        # G[t] = R[t+1] + R[t+2] + R[t+3] + ...
        self.assertEqual(mdp.return_history[0], 0 + 0 + 0 + 0 + final_reward)
        self.assertEqual(mdp.return_history[1], 0 + 0 + 0 + final_reward)
        self.assertEqual(mdp.return_history[2], 0 + 0 + final_reward)
        self.assertEqual(mdp.return_history[3], 0 + final_reward)
        self.assertEqual(mdp.return_history[4], final_reward)
        self.assertEqual(mdp.return_history[5], 0) # Return is zero in terminal state


    def test_adjusted_reward_system(self):

        # In the original MDP, there is no discounting (gamma = 1) and the reward in the last episode
        # is proportional to the time it took to get to the goal.
        # i.e. the ground MDP is not markov!
        # To remedy this, we experimented with changing the return.
        # We intruduced a discount factor of 0.9 and set the reward when reaching to goal to be 1.

        # This behavior can be turned on via a parameter in the minigrid builder!
        # By default, the original reward system is used.

        mdp = GymMinigridBuilder('MiniGrid-Empty-5x5-v0', use_alternative_reward_system=True).build_mdp()

        _, next_reward = mdp.transition('forward')
        self.assertEqual(0, next_reward)
        _, next_reward = mdp.transition('forward')
        self.assertEqual(0, next_reward)
        _, next_reward = mdp.transition('right')
        self.assertEqual(0, next_reward)
        _, next_reward = mdp.transition('forward')
        self.assertEqual(0, next_reward)
        _, next_reward = mdp.transition('forward')
        self.assertEqual(1, next_reward)

        # G[t] = R[t+1] + R[t+2] + R[t+3] + ...
        self.assertEqual(mdp.return_history[0], 0 + 0 + 0 + 0 + 1*0.9*0.9*0.9*0.9)
        self.assertEqual(mdp.return_history[1], 0 + 0 + 0 + 1*0.9*0.9*0.9)
        self.assertEqual(mdp.return_history[2], 0 + 0 + 1*0.9*0.9)
        self.assertEqual(mdp.return_history[3], 0 + 1*0.9)
        self.assertEqual(mdp.return_history[4], 1)
        self.assertEqual(mdp.return_history[5], 0) # Return is zero in terminal state

    def test_custom_level_creation(self):

        should_be_state = { f'obj(wall(grey),({x},0))' for x in range(0, 5) } \
                        | { f'obj(wall(grey),({x},4))' for x in range(0, 5) } \
                        | { f'obj(wall(grey),(0,{y}))' for y in range(0, 5) } \
                        | { f'obj(wall(grey),(4,{y}))' for y in range(0, 5) } \
                        | { 'obj(agent(south),(2,2))',
                            'obj(goal,(3,3))'
                          }

        mdp = GymMinigridCustomLevelBuilder('room_5x5').build_mdp()
        self.assertSetEqual(should_be_state, mdp.state)

    def test_all_objects(self):

        world = """
            rW  rF  gK  pA
            yB  <   rDo bDc
            gDl G   ~   _

        """

        should_be_state = {
            'obj(wall(red),(0,0))',
            'obj(floor(red),(1,0))',
            'obj(key(green),(2,0))',
            'obj(ball(purple),(3,0))',
            'obj(box(yellow),(0,1))',
            'obj(agent(west),(1,1))',
            'obj(door(red,open),(2,1))',
            'obj(door(blue,closed),(3,1))',
            'obj(door(green,locked),(0,2))',
            'obj(goal,(1,2))',
            'obj(lava,(2,2))',
        }

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        self.assertSetEqual(should_be_state, mdp.state)

    def test_tiny_custom_world(self):

        # World size nees to be at least 3x3. 
        # If too small, automatically pad the world with empty spaces.

        world = """
            > G

        """
        should_be_state = {
            'obj(agent(east),(0,0))',
            'obj(goal,(1,0))',
        }

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        self.assertSetEqual(should_be_state, mdp.state)


    def test_final_state_after_reaching_goal(self):

        # After reaching the goal, the MDP should be finished (no more actions available)

        world = """
            > G

        """

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        mdp.transition('forward')

        should_be_state = {
            'obj(agent(east),(1,0))',
            'terminal'
        }

        self.assertSetEqual(should_be_state, mdp.state)
        self.assertSetEqual(set(), mdp.available_actions)
        self.assertTrue(mdp.done)


    def test_final_state_after_touching_danger(self):

        # After falling into lava, the MDP should be finished (no more actions available)

        world = """
            > ~
        """

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        mdp.transition('forward')

        should_be_state = {
            'obj(agent(east),(1,0))',
            'terminal'
        }

        self.assertSetEqual(should_be_state, mdp.state)
        self.assertSetEqual(set(), mdp.available_actions)
        self.assertTrue(mdp.done)

    def test_internal_step_limit(self):

        mdp = GymMinigridBuilder('MiniGrid-Empty-5x5-v0').build_mdp()

        # Calculation from minigrid:
        step_limit = 4*5*5

        for s in range(step_limit):
        
            self.assertSetEqual({'left', 'right', 'forward', 'pickup', 'drop', 'toggle', 'done'},
                                mdp.available_actions)

            mdp.transition('right')

        # After this amount of steps, the environment should be done.

        self.assertTrue(mdp.done)
        self.assertSetEqual(set(), mdp.available_actions)


