import os
import sys
import unittest
import warnings

from matplotlib import pyplot as plt

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

# Framework imports
from mdp import GymMinigrid, GymMinigridBuilder, GymMinigridCustomLevelBuilder
from mdp.abstraction import Carcass

class TestGymMinigrid(unittest.TestCase):

    def setUp(self):

        # At time of development, some deprecation warnings occurred in the gym_minigrid package.
        # They are not useful for unittesting, so we suppress them here for all unttests in this class.
        warnings.simplefilter('ignore', category=DeprecationWarning)

    def test_gutter_state(self):

        world = """
            >

        """

        desired_abstract_state = "carcass_gutterState[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_touching_goal_1(self):

        world = """
            kW  kW  kW  kW
            kW  >   G   kW
            kW  kW  kW  kW
        """

        desired_abstract_state = "carcass_(facing(east),objective_x_is(east),objective_y_is(on_axis),touching(goal),in_gap(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_touching_goal_2(self):

        world = """
            kW  kW  kW  kW
            kW  ^   G   kW
            kW  kW  kW  kW
        """

        desired_abstract_state = "carcass_(facing(north),objective_x_is(east),objective_y_is(on_axis),touching(goal),in_gap(none))[left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'left', 'right'},
                            abstract_mdp.available_actions)

    def test_touching_goal_3(self):

        world = """
            kW  kW  kW
            kW  <   kW
            kW  G   kW
            kW  kW  kW
        """

        desired_abstract_state = "carcass_(facing(west),objective_x_is(on_axis),objective_y_is(south),touching(goal),in_gap(none))[left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'left', 'right'},
                            abstract_mdp.available_actions)

    def test_distant_goal_1(self):

        world = """
            kW  kW  kW  kW
            kW  _   G   kW
            kW  v   _   kW
            kW  kW  kW  kW
        """

        desired_abstract_state = "carcass_(facing(south),objective_x_is(east),objective_y_is(north),touching(none),in_gap(none))[left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'left', 'right'},
                            abstract_mdp.available_actions)

    def test_goal_behind_touching_closed_door(self):

        world = """
            kW  kW  kW  kW  kW  kW
            kW  G   kW  _   _   kW
            kW  _   rDc ^   _   kW
            kW  kW  kW  kW  kW  kW

        """

        desired_abstract_state = "carcass_(facing(north),objective_x_is(west),objective_y_is(on_axis),touching(door(closed)),in_gap(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_goal_behind_touching_open_door(self):

        world = """
            kW  kW  kW  kW  kW  kW
            kW  G   kW  _   _   kW
            kW  _   rDo <   _   kW
            kW  kW  kW  kW  kW  kW

        """

        desired_abstract_state = "carcass_(facing(west),objective_x_is(west),objective_y_is(on_axis),touching(door(open)),in_gap(none))[forward,left,right,toggle]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right', 'toggle'},
                            abstract_mdp.available_actions)
        
    def test_goal_behind_distant_door(self):

        world = """
            kW  kW  kW  kW  kW  kW
            kW  G   kW  _   v   kW
            kW  _   gDc _   _   kW
            kW  kW  kW  kW  kW  kW

        """

        desired_abstract_state = "carcass_(facing(south),objective_x_is(west),objective_y_is(south),touching(none),in_gap(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_goal_behind_touching_gap_point(self):

        world = """
            kW  kW  kW  kW  kW
            kW  G   kW  _   kW
            kW  _   _   <   kW
            kW  kW  kW  kW  kW

        """

        desired_abstract_state = "carcass_(facing(west),objective_x_is(west),objective_y_is(on_axis),touching(gap),in_gap(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)


    def test_facing_lava_1(self):

        world = """
            kW  kW  kW  kW
            kW  >   ~   kW
            kW  G   _   kW
            kW  kW  kW  kW
        """
        

        desired_abstract_state = "carcass_facing_danger[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_facing_lava_2(self):
        
        world = """
            kW  kW  kW  kW
            kW  ~   <   kW
            kW  G   _   kW
            kW  kW  kW  kW
        """

        desired_abstract_state = "carcass_facing_danger[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_facing_lava_3(self):
        
        world = """
            kW  kW  kW  kW
            kW  _   ~   kW
            kW  G   ^   kW
            kW  kW  kW  kW
        """

        desired_abstract_state = "carcass_facing_danger[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_facing_lava_4(self):
        
        world = """
            kW  kW  kW  kW
            kW  _   v   kW
            kW  G   ~   kW
            kW  kW  kW  kW
        """

        desired_abstract_state = "carcass_facing_danger[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_touching_but_not_facing_lava(self):

        world = """
            kW  kW  kW  kW
            kW  v   ~   kW
            kW  G   ~   kW
            kW  kW  kW  kW
        """

        desired_abstract_state = "carcass_(facing(south),objective_x_is(on_axis),objective_y_is(south),touching(goal),in_gap(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_facing_dangerous_blue_ball(self):

        world = """
            kW  kW  kW  kW
            kW  >   bA  kW
            kW  G   _   kW
            kW  kW  kW  kW
        """

        desired_abstract_state = "carcass_facing_danger[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')


        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_final_state_after_reaching_goal(self):

        # After reaching the goal, the MDP should be finished (no more actions available)

        world = """
            kW  kW  kW  kW
            kW  >   G   kW
            kW  kW  kW  kW
        """

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')
        abstract_mdp.transition('forward')

        self.assertEqual('carcass_gutterState[]', abstract_mdp.state)
        self.assertSetEqual(set(), abstract_mdp.available_actions)

    def test_final_state_after_touching_danger(self):

        # After falling into lava, the MDP should be finished (no more actions available)

        world = """
            > ~
        """

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        abstract_mdp.transition('forward')

        self.assertEqual('carcass_gutterState[]', abstract_mdp.state)
        self.assertSetEqual(set(), abstract_mdp.available_actions)

    def test_in_vertical_gap(self):

        world = """
            kW  kW  kW  kW  kW
            kW  _   _   _   kW
            kW  kW  ^   kW  kW
            kW  _   G   _   kW
            kW  kW  kW  kW  kW
        """



        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        desired_abstract_state = "carcass_(facing(north),objective_x_is(on_axis),objective_y_is(south),touching(goal),in_gap(vertical))[forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

    def test_in_horizontal_gap(self):

        world = """
            kW  kW  kW  kW  kW
            kW  _   kW  _   kW
            kW  _   ^   G   kW
            kW  _   kW  _   kW
            kW  kW  kW  kW  kW
        """


        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')


        desired_abstract_state = "carcass_(facing(north),objective_x_is(east),objective_y_is(on_axis),touching(goal),in_gap(horizontal))[left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

    def test_what_happens_after_going_through_door(self):


        world = """
            kW  kW  kW  kW  kW  kW
            kW  >   gDc _   _   kW
            kW  _   kW  G   _   kW
            kW  kW  kW  kW  kW  kW

        """


        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        abstract_mdp.transition('toggle')
        abstract_mdp.transition('forward')

        desired_abstract_state = "carcass_(facing(east),objective_x_is(east),objective_y_is(south),touching(none),in_gap(horizontal))[forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

    def test_pickup_key_before_goal(self):

        # If there is a key in the world, but no door, picking it up should not matter!

        world = """
            kW  kW  kW  kW  kW
            kW  v   _   _   kW
            kW  _   _   G   kW
            kW  gK  _   _   kW
            kW  kW  kW  kW  kW
        """

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        desired_abstract_state = "carcass_(facing(south),objective_x_is(east),objective_y_is(south),touching(none),in_gap(none))[forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('forward')

        desired_abstract_state = "carcass_(facing(south),objective_x_is(east),objective_y_is(on_axis),touching(none),in_gap(none))[left,pickup,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('pickup')

        desired_abstract_state = "carcass_(facing(south),objective_x_is(east),objective_y_is(on_axis),touching(none),in_gap(none))[drop,forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

    def test_key_drop_and_pickup_restricted_actions(self):

        world = """
           kW   kW  kW  kW  kW
           kW   _   kW  _   kW
           kW   yK  yDl _   kW
           kW   ^   kW  G   kW
           kW   kW  kW  kW  kW

        """

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        desired_abstract_state = "carcass_(facing(north),objective_x_is(on_axis),objective_y_is(north),touching(key),in_gap(vertical))[left,pickup,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('pickup')
        desired_abstract_state = "carcass_(facing(north),objective_x_is(east),objective_y_is(north),touching(none),in_gap(vertical))[drop,forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('drop')
        desired_abstract_state = "carcass_(facing(north),objective_x_is(on_axis),objective_y_is(north),touching(key),in_gap(vertical))[left,pickup,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('pickup')
        desired_abstract_state = "carcass_(facing(north),objective_x_is(east),objective_y_is(north),touching(none),in_gap(vertical))[drop,forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('left')
        desired_abstract_state = "carcass_(facing(west),objective_x_is(east),objective_y_is(north),touching(none),in_gap(vertical))[left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

    def test_tie_break_preferring_nearer_goals(self):

        # In some cases, multiple paths to a goal are available.
        # For a practical example, consider the FourRooms Environment.
        # In this case, multiple paths to the goal are minimal.
        # We need to break those ties deterministically.
        # -> Add rule to pick a path where the next subgoal has the smallest manhattan distance!

        world = """
           kW   kW  kW  kW  kW
           kW   _   G   _   kW
           kW   _   _   _   kW
           kW   ^   _   G   kW
           kW   kW  kW  kW  kW

        """

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions_v2.lp')

        desired_abstract_state = "carcass_(facing(north),objective_x_is(east),objective_y_is(on_axis),touching(none),in_gap(none))[forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)
