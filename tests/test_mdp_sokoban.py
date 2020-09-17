import os
import sys
import unittest

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

# Framework imports
from mdp import Sokoban, SokobanBuilder

class TestSokoban(unittest.TestCase):
    
    def test_builder(self):

        builder = SokobanBuilder(level_name='suitcase-05-01')

        true_string_representation = '########\n' \
                                   + '#  ..$ #\n' \
                                   + '# $@ $ #\n' \
                                   + '# $..  #\n' \
                                   + '########'

        # This is the dynamic state, which can change over time.
        true_initial_state = {  'box(6,2)', 'box(3,3)', 'box(6,3)', 'box(3,4)',
                                'sokoban(4,3)'
                             }

        # This is the static state, which won't change.
        true_static_state = {   'block(1,1)', 'block(2,1)', 'block(3,1)', 'block(4,1)',
                                'block(5,1)', 'block(6,1)', 'block(7,1)', 'block(8,1)',
                                'block(1,2)', 'block(8,2)',
                                'block(1,3)', 'block(8,3)',
                                'block(1,4)', 'block(8,4)',
                                'block(1,5)', 'block(2,5)', 'block(3,5)', 'block(4,5)',
                                'block(5,5)', 'block(6,5)', 'block(7,5)', 'block(8,5)',

                                'dest(4,2)', 'dest(5,2)', 'dest(4,4)', 'dest(5,4)',

                                'row(1)', 'row(2)', 'row(3)', 'row(4)', 'row(5)',
                                'col(1)', 'col(2)', 'col(3)', 'col(4)', 
                                'col(5)', 'col(6)', 'col(7)', 'col(8)', 
                            } 
        
        self.assertEqual(true_string_representation, builder.level_txt)
        self.assertSetEqual(true_initial_state, builder.level_asp_initial)
        self.assertSetEqual(true_static_state, builder.level_asp_static)

        mdp = builder.build_mdp()

        self.assertEqual(true_initial_state, mdp.state)

    def test_available_actions_1(self):

        builder = SokobanBuilder(level_name='suitcase-05-01')
        mdp = builder.build_mdp()

        true_available_actions = {  'push(6,2,left)', 'push(6,2,right)',
                                    'push(3,3,left)', 'push(3,3,right)',
                                    'push(6,3,left)', 'push(6,3,right)',
                                    'push(3,4,left)', 'push(3,4,right)' 
                                 }

        self.assertSetEqual(true_available_actions, mdp.available_actions)

    def test_available_actions_2(self):

        builder = SokobanBuilder(level_name='suitcase-05-02')
        mdp = builder.build_mdp()

        true_available_actions = {  'push(5,3,left)', 'push(5,3,right)', 'push(5,3,down)',
                                    'push(4,4,right)', 'push(4,4,up)', 'push(4,4,down)',
                                    'push(6,4,left)', 'push(6,4,up)', 'push(6,4,down)',
                                    'push(5,5,left)', 'push(5,5,right)', 'push(5,5,up)'
                                 }

        self.assertSetEqual(true_available_actions, mdp.available_actions)

    def test_available_actions_3(self):

        builder = SokobanBuilder(level_name='suitcase-05-01a')
        mdp = builder.build_mdp()

        true_available_actions = {  'push(5,2,right)',
                                    'push(4,3,right)',
                                    'push(4,4,right)'
                                 }

        self.assertSetEqual(true_available_actions, mdp.available_actions)

    def test_no_actions_available(self):

        builder = SokobanBuilder(level_name='suitcase-05-01b')
        mdp = builder.build_mdp()

        self.assertEqual(set(), mdp.available_actions)
        self.assertEqual(0, len(mdp.available_actions))

    def test_no_actions_available_after_action(self):

        builder = SokobanBuilder(level_name='suitcase-05-01c')
        mdp = builder.build_mdp()
        mdp.transition('push(3,2,right)')

        self.assertEqual(set(), mdp.available_actions)
        self.assertEqual(0, len(mdp.available_actions))


    def test_executing_wrong_actions(self):

        builder = SokobanBuilder(level_name='suitcase-05-01')
        mdp = builder.build_mdp()
        with self.assertRaises(Exception):
            mdp.transition('push(3,3,up)')

    def test_transition_1(self):

        """
        Just messing around with arbitrary moves:

        State 0:        State 1:        State 2:
             #######         #######         #######
             #     #         #     #         #     #
            ## .$. #        ## .@. #        ## * . #
            #@ $ $ #        #  $$$ #        #  @$$ #
            #  .$. #        #  .$. #        #  .$. #
            ##     #        ##     #        ##     #
             #######         #######         #######

        """

        builder = SokobanBuilder(level_name='suitcase-05-02')
        mdp = builder.build_mdp()
        state_0 = mdp.state

        next_state, next_reward = mdp.transition('push(5,3,down)')
        state_1 = state_0 - {'box(5,3)', 'sokoban(2,4)'} | {'box(5,4)', 'sokoban(5,3)'}
        self.assertSetEqual(state_1, mdp.state)
        self.assertSetEqual(state_1, next_state)
        self.assertEqual(-1, next_reward)

        true_available_actions_1 = { 'push(4,4,up)', 'push(4,4,down)',
                                     'push(6,4,up)', 'push(6,4,down)',
                                     'push(5,5,left)', 'push(5,5,right)'
                                   }
        self.assertEqual(true_available_actions_1, mdp.available_actions)

        next_state, next_reward = mdp.transition('push(4,4,up)')
        state_2 = state_1 - {'box(4,4)', 'sokoban(5,3)'} | {'box(4,3)', 'sokoban(4,4)'}
        self.assertSetEqual(state_2, mdp.state)
        self.assertSetEqual(state_2, next_state)
        self.assertEqual(-1, next_reward)

        true_available_actions_2 = { 'push(4,3,up)', 'push(4,3,down)', 'push(4,3,left)', 'push(4,3,right)',
                                     'push(6,4,up)', 'push(6,4,down)',
                                     'push(5,5,left)', 'push(5,5,right)'
                                   }
        self.assertEqual(true_available_actions_2, mdp.available_actions)

        self.assertEqual([None, -1, -1], mdp.reward_history)
        self.assertEqual([-2, -1, 0], mdp.return_history) 

    def test_transition_2(self):

        """
        Moving a block into a corner should end the MDP. 

        State 0         State 4
            ########        ########
            #  ..$ #        #  ..$ #
            # $@ $ #        # $  $ #
            # $..  #        #$@..  #
            ########        ########
        """

        builder = SokobanBuilder(level_name='suitcase-05-01')
        mdp = builder.build_mdp()
        state_0 = mdp.state
        state_1 = state_0 - { 'box(3,4)', 'sokoban(4,3)' } \
                          | { 'box(2,4)', 'sokoban(3,4)' }

        next_state, next_reward = mdp.transition('push(3,4,left)')

        self.assertSetEqual(state_1, mdp.state)
        self.assertSetEqual(state_1, next_state)
        self.assertEqual(-101, next_reward)
        self.assertSetEqual(set(), mdp.available_actions)

        self.assertEqual([None, -101], mdp.reward_history)
        self.assertEqual([-101, 0], mdp.return_history)

    def test_transition_3(self):

        """
        Get a reward when moving to the goal state.

        State 0         State 1         State 2         State 3         
            ########        ########        ########        ########    
            #  ..$ #        #  ..$ #        # $..$ #        # @*.$ #    
            # $@ $ #        # $  $ #        # @  $ #        #    $ #    
            # $..  #        # @*.  #        #  *.  #        #  *.  #    
            ########        ########        ########        ########    

        State 4         State 5         State 6     
            ########        ########        ########
            #  **@ #        #  **  #        #  **  #
            #    $ #        #    @ #        #      #
            #  *.  #        #  *.$ #        #  **@ #
            ########        ########        ########

        """

        builder = SokobanBuilder(level_name='suitcase-05-01')
        mdp = builder.build_mdp()
        state_0 = mdp.state

        mdp.transition('push(3,4,right)')
        mdp.transition('push(3,3,up)')
        mdp.transition('push(3,2,right)')
        mdp.transition('push(6,2,left)')
        mdp.transition('push(6,3,down)')
        next_state, next_reward = mdp.transition('push(6,4,left)')


        true_state_8 = { 'box(4,2)', 'box(5,2)', 'box(4,4)', 'box(5,4)',
                         'sokoban(6,4)' }

        self.assertSetEqual(true_state_8, mdp.state)
        self.assertSetEqual(true_state_8, next_state)
        self.assertEqual(99, next_reward)
        
        self.assertEqual([None, -1, -1, -1, -1, -1, 99], mdp.reward_history)
        self.assertEqual([94, 95, 96, 97, 98, 99, 0], mdp.return_history)
