import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

# Framework imports
from mdp import BlocksWorld
from mdp.abstraction import PrologCarcass, PrologCarcassBuilder


class TestCarcassBlocksworldStackOrdered(unittest.TestCase):

    # TODO: It should be okay to stack two goal towers on top of each other as long as the one below is complete.
    # TODO: Test what happens when subgoal(X,table) is true!

    def test_rule_0(self):

        """
            Rule 0: a goal-tower exists and is clear, next goal block is clear

            Example:
                                        ..
                                       [b3] <d3>
            [b2]                       [b2] <d2>
            [b1] [b3] <d2> <d3>        [b1] <d1>
             c1   c2  <d1>  c3    =>    ..   ..
             ------------------         -------

             Initial                    Goal

        """

        mdp = BlocksWorld(state_initial={'on(c1,table)', 'on(b1,c1)', 'on(b2,b1)', 
                                         'on(c2,table)', 'on(b3,c2)', 
                                         'on(d1,table)', 'on(d2,d1)', 
                                         'on(c3,table)', 'on(d3,c3)'},
                          state_static={'subgoal(b3,b2)', 'subgoal(b2,b1)',
                                        'subgoal(d3,d2)', 'subgoal(d2,d1)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')


        self.assertEqual('carcass_r0[gutterAction,move(nextGoalBlock,goodTowerTop)]', abstract_mdp.state)
        self.assertEqual({'gutterAction','move(nextGoalBlock,goodTowerTop)'}, abstract_mdp.available_actions)
        self.assertEqual({'move(b3,b2)', 'move(d3,d2)'}, abstract_mdp.ground_actions_of('move(nextGoalBlock,goodTowerTop)'))


        # Make sure all available ground actions are covered by some abstract action.
        covered = set()
        for abstract_action in abstract_mdp.available_actions:
            covered.update(abstract_mdp.ground_actions_of(abstract_action))
        self.assertEqual(mdp.available_actions, covered)


    def test_rule_1_other_tower_exists(self):

        """
            Rule 1:     a goal-tower exists and has other blocks on top
                        another tower (not just the floor) exists to put blocks on


            Example:
                                      ..
             c2                      [b3]
            [b2]                     [b2]
            [b1]                     [b1]
             c1  [b3]  c3  c4   =>    ..
             ----------------         --

             Initial                 Goal

            

        """

        mdp = BlocksWorld(state_initial={'on(c1,table)', 'on(b1,c1)', 'on(b2,b1)', 'on(c2,b2)', 'on(b3,table)', 'on(c3,table)', 'on(c4,table)'},
                          state_static={'subgoal(b3,b2)', 'subgoal(b2,b1)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

        self.assertEqual('carcass_r1[gutterAction,move(badTopBlock,otherTowerTop),move(badTopBlock,table)]', abstract_mdp.state)
        self.assertEqual({'gutterAction', 'move(badTopBlock,otherTowerTop)', 'move(badTopBlock,table)'}, abstract_mdp.available_actions)
        self.assertEqual({'move(c2,b3)', 'move(c2,c3)', 'move(c2,c4)'}, abstract_mdp.ground_actions_of('move(badTopBlock,otherTowerTop)'))
        self.assertEqual({'move(c2,table)'}, abstract_mdp.ground_actions_of('move(badTopBlock,table)'))

        # Make sure all available ground actions are covered by some abstract action.
        covered = set()
        for abstract_action in abstract_mdp.available_actions:
            covered.update(abstract_mdp.ground_actions_of(abstract_action))
        self.assertEqual(mdp.available_actions, covered)

    def test_rule_1_no_other_tower_exists(self):

        """
            Rule 1:     a goal-tower exists and has other blocks on top
                        no other tower exists -> put on floor


            Example:

            [b3]         ..
            [c2]        [b3]
            [b2]        [b2]
            [b1]        [b1]
             c1     =>   ..
            ----        ----

             Initial    Goal

            

        """

        mdp = BlocksWorld(state_initial={'on(c1,table)', 'on(b1,c1)', 'on(b2,b1)', 'on(c2,b2)', 'on(b3,c2)'},
                          state_static={'subgoal(b3,b2)', 'subgoal(b2,b1)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

        self.assertEqual('carcass_r1[move(badTopBlock,table)]', abstract_mdp.state)
        self.assertEqual({'move(badTopBlock,table)'}, abstract_mdp.available_actions)
        self.assertEqual({'move(b3,table)'}, abstract_mdp.ground_actions_of('move(badTopBlock,table)'))

        # Make sure all available ground actions are covered by some abstract action.
        covered = set()
        for abstract_action in abstract_mdp.available_actions:
            covered.update(abstract_mdp.ground_actions_of(abstract_action))
        self.assertEqual(mdp.available_actions, covered)


    def test_rule_2_other_towers_exist(self):


        """
            Rule 2:     a goal-tower exists and is clear, next goal block is not clear.
                        another tower (not just the floor) exists to put blocks on


            Example:
                                      ..
                                     [b3]
            [b2]                     [b2]
            [b1]  c2                 [b1]
             c1  [b3]  c3  c4   =>    ..
             ---------------          --

             Initial                 Goal

            

        """

        mdp = BlocksWorld(state_initial={'on(c1,table)', 'on(b1,c1)', 'on(b2,b1)', 'on(c2,b3)', 'on(b3,table)', 'on(c3,table)', 'on(c4,table)'},
                          state_static={'subgoal(b3,b2)', 'subgoal(b2,b1)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

        self.assertEqual('carcass_r2[gutterAction,move(badTopBlock,otherTowerTop),move(badTopBlock,table)]', abstract_mdp.state)
        self.assertEqual({'gutterAction', 'move(badTopBlock,otherTowerTop)', 'move(badTopBlock,table)'}, abstract_mdp.available_actions)
        self.assertEqual({'move(c2,c3)', 'move(c2,c4)'}, abstract_mdp.ground_actions_of('move(badTopBlock,otherTowerTop)'))
        self.assertEqual({'move(c2,table)'}, abstract_mdp.ground_actions_of('move(badTopBlock,table)'))

        # Make sure all available ground actions are covered by some abstract action.
        covered = set()
        for abstract_action in abstract_mdp.available_actions:
            covered.update(abstract_mdp.ground_actions_of(abstract_action))
        self.assertEqual(mdp.available_actions, covered)

    def test_rule_2_goal_tower_is_single_block(self):

        """
            If a "good tower base" has only irrelevant blocks underneath, it is indeed a tower base.

            In the following, b1 by itself should count as goal tower.


                                    [b2]
            [b1]  c2                [b1]
             c1  [b2]  c3       =>   ..
            --------------          ----

            Initial                 Goal

        """

        mdp = BlocksWorld(state_initial={'on(c1,table)', 'on(b1,c1)', 
                                         'on(b2,table)', 'on(c2,b2)'},
                          state_static={'subgoal(b2,b1)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

        self.assertEqual('carcass_r2[gutterAction,move(badTopBlock,table)]', abstract_mdp.state)

    def test_rule_3(self):

        """
            Rule 3: no goal tower exists, first goal block is not clear

            Example:

                                
                                     ..
             c1                     [b2]
            [b1]                    [b1]
            [b3] [b2]  c2       =>   ..
            --------------          ----

            Initial                 Goal

        """


        mdp = BlocksWorld(state_initial={'on(b3,table)', 'on(b1,b3)', 'on(c1,b1)', 
                                         'on(b2,table)', 
                                         'on(c2,table)'},
                          state_static={'subgoal(b3,b2)', 'subgoal(b2,b1)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

        self.assertEqual('carcass_r3[gutterAction,move(badTopBlock,otherTowerTop),move(badTopBlock,table)]', abstract_mdp.state)
        self.assertEqual({'gutterAction', 'move(badTopBlock,otherTowerTop)', 'move(badTopBlock,table)'}, abstract_mdp.available_actions)
        self.assertEqual({'move(c1,table)'}, abstract_mdp.ground_actions_of('move(badTopBlock,table)'))
        self.assertEqual({'move(c1,b2)', 'move(c1,c2)'}, abstract_mdp.ground_actions_of('move(badTopBlock,otherTowerTop)'))

        # Make sure all available ground actions are covered by some abstract action.
        covered = set()
        for abstract_action in abstract_mdp.available_actions:
            covered.update(abstract_mdp.ground_actions_of(abstract_action))
        self.assertEqual(mdp.available_actions, covered)

    def test_rule_4(self):

        """
            Rule 4: no goal tower exists, first goal block is clear

            Example:

                                     ..
                                    [b3]
                                    [b2]
            [b1]  c2                [b1]
            [b3] [b2]  c3       =>   ..
            --------------          ----

            Initial                 Goal

        """

        mdp = BlocksWorld(state_initial={'on(b3,table)', 'on(b1,b3)',
                                         'on(b2,table)', 'on(c2,b2)',
                                         'on(c3,table)'},
                          state_static={'subgoal(b3,b2)', 'subgoal(b2,b1)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

        self.assertEqual('carcass_r4[gutterAction,move(towerBase,table)]', abstract_mdp.state)
        self.assertEqual({'gutterAction', 'move(towerBase,table)'}, abstract_mdp.available_actions)
        self.assertEqual({'move(b1,table)'}, abstract_mdp.ground_actions_of('move(towerBase,table)'))

        # Make sure all available ground actions are covered by some abstract action.
        covered = set()
        for abstract_action in abstract_mdp.available_actions:
            covered.update(abstract_mdp.ground_actions_of(abstract_action))
        self.assertEqual(mdp.available_actions, covered)


    def test_3blocks_world_with_table_subgoal_1(self):

       # Things should also work when b0 needs to be on the table as a subgoal.

       mdp = BlocksWorld(state_initial={'on(b0,b1)', 'on(b1,table)', 'on(b2,table)'},
                         state_static={'subgoal(b2,b1)', 'subgoal(b1,b0)', 'subgoal(b0,table)'})
       abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

       self.assertEqual('carcass_r0[gutterAction,move(nextGoalBlock,goodTowerTop)]', abstract_mdp.state)
       self.assertEqual({'move(b0,table)'}, abstract_mdp.ground_actions_of('move(nextGoalBlock,goodTowerTop)'))

    def test_3blocks_world_with_table_subgoal_2(self):
                         
       # Things should also work when b0 needs to be on the table as a subgoal.
       # If b0 is free and only irrelevant blocks are underneath, we still need to move b0 on the table.

       mdp = BlocksWorld(state_initial={'on(b0,c0)', 'on(c0,table)', 'on(b2,table)', 'on(b1,b2)'},
                         state_static={'subgoal(b2,b1)', 'subgoal(b1,b0)', 'subgoal(b0,table)'})
       abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

       self.assertEqual('carcass_r0[gutterAction,move(nextGoalBlock,goodTowerTop)]', abstract_mdp.state)
       self.assertEqual({'move(b0,table)'}, abstract_mdp.ground_actions_of('move(nextGoalBlock,goodTowerTop)'))


    def test_4blocks_world_with_table_subgoal_1(self):

       # Things should also work when b0 needs to be on the table as a subgoal.
       # This special example caused trouble in the past:

       mdp = BlocksWorld(state_initial={'on(b1,b3)', 'on(b3,b2)', 'on(b2,b0)', 'on(b0,table)',
                                        'on(b4,table)'},
                         state_static={'subgoal(b1,b0)', 'subgoal(b2,b1)', 'subgoal(b4,b3)', 'subgoal(b0,table)', 'subgoal(b3,b2)'})


       abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

       self.assertEqual('carcass_r1[gutterAction,move(badTopBlock,otherTowerTop),move(badTopBlock,table)]', abstract_mdp.state)
       self.assertEqual({'move(b1,b4)'}, abstract_mdp.ground_actions_of('move(badTopBlock,otherTowerTop)'))
       self.assertEqual({'move(b1,table)'}, abstract_mdp.ground_actions_of('move(badTopBlock,table)'))
       self.assertEqual({'move(b4,b1)'}, abstract_mdp.ground_actions_of('gutterAction'))

    def test_multipe_table_tower_bases_1(self):

        mdp = BlocksWorld(state_initial={'on(c2,b0)', 'on(b0,table)',
                                         'on(b1,c0)', 'on(c0,table)',
                                         'on(c1,table)'},
                          state_static={'subgoal(b0,table)', 'subgoal(b1,b0)',
                                        'subgoal(c0,table)', 'subgoal(c1,c0)', 'subgoal(c2,c1)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')
        
        self.assertEqual('carcass_r1[gutterAction,move(badTopBlock,otherTowerTop),move(badTopBlock,table)]',abstract_mdp.state)
        self.assertEqual({'move(c2,b1)', 'move(c2,c1)', 'move(b1,c2)', 'move(b1,c1)'}, abstract_mdp.ground_actions_of('move(badTopBlock,otherTowerTop)'))
        self.assertEqual({'move(c2,table)', 'move(b1,table)'}, abstract_mdp.ground_actions_of('move(badTopBlock,table)'))

    def test_multipe_table_tower_bases_2(self):

        mdp = BlocksWorld(state_initial={'on(c2,b0)', 'on(b0,table)',
                                         'on(c0,b1)', 'on(b1,table)',
                                         'on(c1,table)'},
                          state_static={'subgoal(b0,table)', 'subgoal(b1,b0)',
                                        'subgoal(c0,table)', 'subgoal(c1,c0)', 'subgoal(c2,c1)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')
        
        self.assertEqual('carcass_r0[gutterAction,move(nextGoalBlock,goodTowerTop)]',abstract_mdp.state)
        self.assertEqual({'move(c0,table)'}, abstract_mdp.ground_actions_of('move(nextGoalBlock,goodTowerTop)'))


    def test_gutter_state(self):
        mdp = BlocksWorld(state_initial={'on(b0,table)', 'on(b1,b0)', 'on(b2,b1)'},
                          state_static={'subgoal(b0,table)', 'subgoal(b1,b0)', 'subgoal(b2,b1)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

        self.assertEqual('carcass_gutter[]',abstract_mdp.state)
        # reached for goal state

    def test_gutter_state_with_actions(self):
        # There is a complete tower top but the state is not final (b3 is part of a subgoal but b3 does not exist, so final state can never be reached)
        # I expect the abstract state to be the gutter state, with all action grouped into the gutterAction.
        # This should not clash with the `carcass_gutter` hard-coded gutter state in PrologCarcass
        # `gutterAction` (prolog encoding) should be overruled by `random` (python hard coded), which in this case should both group all actions.
        mdp = BlocksWorld(state_initial={'on(b0,table)', 'on(b1,b0)', 'on(b2,b1)'},
                          state_static={'subgoal(b0,table)', 'subgoal(b1,b0)', 'subgoal(b2,b1)', 'subgoal(b3,b2)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

        self.assertEqual('carcass_gutter[random]',abstract_mdp.state)
        self.assertEqual(mdp.available_actions, abstract_mdp.ground_actions_of('random'))

    def test_stacked_good_towers(self):

        # There is one "good" tower b1-b2-b3 which is in its final position
        # There is a second partial "good" tower with d1-d2 in its final position directly on top of the other tower, but b3 missing!
        # Abstract state should by r0, since b3 can be moved on top of b2.
        # The location of b1 does not matter, since the tower below is complete.

        """
            Rule 0: a goal-tower exists and is clear, next goal block is clear

            Example:
 
             d2              ..   ..
             d1             [b3] [d3]
             b3             [b2] [d2]
             b2             [b1] [d1]
             b1  d3   =>     ..   ..
             -------         -------

             Initial         Goal

        """
        mdp = BlocksWorld(state_initial={'on(b1,table)', 'on(b2,b1)', 'on(b3,b2)', 
                                         'on(d1,b3)', 'on(d2,d1)',
                                         'on(d3,table)'},
                          state_static={'subgoal(b2,b1)', 'subgoal(b3,b2)', 
                                        'subgoal(d2,d1)', 'subgoal(d3,d2)'})

        abstract_mdp = PrologCarcass(mdp, rules_filename='prolog_blocksworld_stackordered.pl')

        self.assertEqual('carcass_r0[gutterAction,move(nextGoalBlock,goodTowerTop)]', abstract_mdp.state)
        self.assertEqual({'gutterAction','move(nextGoalBlock,goodTowerTop)'}, abstract_mdp.available_actions)
        self.assertEqual({'move(d3,d2)'}, abstract_mdp.ground_actions_of('move(nextGoalBlock,goodTowerTop)'))
        self.assertEqual({'move(d2,d3)', 'move(d2,table)'}, abstract_mdp.ground_actions_of('gutterAction'))

        # Make sure all available ground actions are covered by some abstract action.
        covered = set()
        for abstract_action in abstract_mdp.available_actions:
            covered.update(abstract_mdp.ground_actions_of(abstract_action))
        self.assertEqual(mdp.available_actions, covered)
