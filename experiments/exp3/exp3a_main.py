import os
import sys

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests import test_policy
from MonteCarlo import MonteCarlo
from mdp import BlocksWorldBuilder
from control import SimpleMonteCarloControl, SgdMonteCarloControl

from matplotlib import pyplot as plt

mdp_builder = BlocksWorldBuilder(blocks_world_size=7)
planner = None
ctrl = SimpleMonteCarloControl()
mc = MonteCarlo(mdp_builder, planner, control=ctrl, 
                max_episode_length=14, planning_factor=0, plan_on_empty_policy=False,
                exploring_starts=True, exploring_factor = 0.0)
learned_policy = mc.learn_policy(number_episodes=150, show_progress_bar=True)
