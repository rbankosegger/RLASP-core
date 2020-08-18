import os
import sys

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests import test_policy
from MonteCarlo import MonteCarlo
from BlocksWorld import BlocksWorld
from control import SimpleMonteCarloControl, SgdMonteCarloControl

from matplotlib import pyplot as plt

blocks_world = BlocksWorld(number_of_blocks=7)
ctrl = SimpleMonteCarloControl(blocks_world)
mc = MonteCarlo(blocks_world, control=ctrl, 
                max_episode_length=14, planning_factor=0, plan_on_empty_policy=False, planning_horizon=0)
learned_policy = mc.learn_policy(discount_rate=1, number_episodes=150, show_progress_bar=True)  # {state : action}
