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
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_touching_goal_1(self):

        world = """
            > G

        """

        desired_abstract_state = "carcass_(facing(east),objective_x_is(east),objective_y_is(on_axis),touching(goal),in_choke(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_touching_goal_2(self):

        world = """
            ^ G

        """

        desired_abstract_state = "carcass_(facing(north),objective_x_is(east),objective_y_is(on_axis),touching(goal),in_choke(none))[left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'left', 'right'},
                            abstract_mdp.available_actions)

    def test_touching_goal_3(self):

        world = """
            <
            G

        """

        desired_abstract_state = "carcass_(facing(west),objective_x_is(on_axis),objective_y_is(south),touching(goal),in_choke(none))[left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'left', 'right'},
                            abstract_mdp.available_actions)

    def test_distant_goal_1(self):

        world = """
            _ G
            v

        """

        desired_abstract_state = "carcass_(facing(south),objective_x_is(east),objective_y_is(north),touching(none),in_choke(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_goal_behind_touching_closed_door(self):

        world = """
            kW  kW  kW  kW  kW  kW
            kW  G   kW  _   _   kW
            kW  _   rDc ^   _   kW
            kW  kW  kW  kW  kW  kW

        """

        desired_abstract_state = "carcass_(facing(north),objective_x_is(west),objective_y_is(on_axis),touching(door(closed)),in_choke(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

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

        desired_abstract_state = "carcass_(facing(west),objective_x_is(west),objective_y_is(on_axis),touching(door(open)),in_choke(none))[forward,left,right,toggle]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

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

        desired_abstract_state = "carcass_(facing(south),objective_x_is(west),objective_y_is(south),touching(none),in_choke(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_goal_behind_touching_choke_point(self):

        world = """
            kW  kW  kW  kW  kW
            kW  G   kW  _   kW
            kW  _   _   <   kW
            kW  kW  kW  kW  kW

        """

        desired_abstract_state = "carcass_(facing(west),objective_x_is(west),objective_y_is(on_axis),touching(choke),in_choke(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)


    def test_facing_lava_1(self):
        
        world = """
            >  ~
            G  _

        """

        desired_abstract_state = "carcass_facing_danger[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_facing_lava_2(self):
        
        world = """
            ~  <
            G  _

        """

        desired_abstract_state = "carcass_facing_danger[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_facing_lava_3(self):
        
        world = """
            _  ~
            G  ^

        """

        desired_abstract_state = "carcass_facing_danger[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_facing_lava_4(self):
        
        world = """
            _  v
            G  ~

        """

        desired_abstract_state = "carcass_facing_danger[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_touching_but_not_facing_lava(self):

        world = """
            v  ~
            G  ~

        """

        desired_abstract_state = "carcass_(facing(south),objective_x_is(on_axis),objective_y_is(south),touching(goal),in_choke(none))[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_facing_dangerous_blue_ball(self):

        world = """
            >  bA
            G  _

        """

        desired_abstract_state = "carcass_facing_danger[forward,left,right]"

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')


        self.assertEqual(desired_abstract_state, abstract_mdp.state)
        self.assertSetEqual({'forward', 'left', 'right'},
                            abstract_mdp.available_actions)

    def test_final_state_after_reaching_goal(self):

        # After reaching the goal, the MDP should be finished (no more actions available)

        world = """
            > G

        """

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')
        abstract_mdp.transition('forward')

        self.assertEqual('carcass_gutterState[]', abstract_mdp.state)
        self.assertSetEqual(set(), abstract_mdp.available_actions)

    def test_final_state_after_touching_danger(self):

        # After falling into lava, the MDP should be finished (no more actions available)

        world = """
            > ~
        """

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        abstract_mdp.transition('forward')

        self.assertEqual('carcass_gutterState[]', abstract_mdp.state)
        self.assertSetEqual(set(), abstract_mdp.available_actions)

    def test_in_vertical_choke(self):

        world = """
            kW  kW  kW
            kW  ^   kW
            kW  G   kW
            kW  kW  kW

        """


        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        desired_abstract_state = "carcass_(facing(north),objective_x_is(on_axis),objective_y_is(south),touching(goal),in_choke(vertical))[left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

    def test_in_horizontal_choke(self):

        world = """
            kW  kW  kW  kW
            kW  ^   G   kW
            kW  kW  kW  kW

        """


        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')



        desired_abstract_state = "carcass_(facing(north),objective_x_is(east),objective_y_is(on_axis),touching(goal),in_choke(horizontal))[left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

    def test_what_happens_after_going_through_door(self):


        world = """
            kW  kW  kW  kW  kW  kW
            kW  >   gDc _   _   kW
            kW  _   kW  G   _   kW
            kW  kW  kW  kW  kW  kW

        """


        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        abstract_mdp.transition('toggle')
        abstract_mdp.transition('forward')

        desired_abstract_state = "carcass_(facing(east),objective_x_is(east),objective_y_is(south),touching(none),in_choke(horizontal))[forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

    def test_pickup_key_before_door(self):

        # If there is a key in the world, pick it up before moving to the goal!
        # Note: This only works with the MiniGrid-DoorKey environment, not more complex environments with multiple locked / open doors and keys!


        world = """
            v   _   G
            _   _   _
            gK  _   _

        """

        mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        # Before picking up the key, treat the key as the goal!
        desired_abstract_state = "carcass_(facing(south),objective_x_is(on_axis),objective_y_is(south),touching(none),in_choke(none))[forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('forward')

        desired_abstract_state = "carcass_(facing(south),objective_x_is(on_axis),objective_y_is(south),touching(key),in_choke(none))[left,pickup,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('pickup')

        # After picking up the key, the `goal` object should be the goal!
        desired_abstract_state = "carcass_(facing(south),objective_x_is(east),objective_y_is(north),touching(none),in_choke(none))[drop,forward,left,right]"
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
        abstract_mdp = Carcass(mdp, rules_filename='minigrid_restricted_actions.lp')

        desired_abstract_state = "carcass_(facing(north),objective_x_is(on_axis),objective_y_is(north),touching(key),in_choke(vertical))[left,pickup,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('pickup')
        desired_abstract_state = "carcass_(facing(north),objective_x_is(on_axis),objective_y_is(north),touching(choke),in_choke(vertical))[drop,forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('drop')
        desired_abstract_state = "carcass_(facing(north),objective_x_is(on_axis),objective_y_is(north),touching(key),in_choke(vertical))[left,pickup,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('pickup')
        desired_abstract_state = "carcass_(facing(north),objective_x_is(on_axis),objective_y_is(north),touching(choke),in_choke(vertical))[drop,forward,left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)

        abstract_mdp.transition('left')
        desired_abstract_state = "carcass_(facing(west),objective_x_is(on_axis),objective_y_is(north),touching(choke),in_choke(vertical))[left,right]"
        self.assertEqual(desired_abstract_state, abstract_mdp.state)
