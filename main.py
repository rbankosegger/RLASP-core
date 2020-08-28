from tests import test_policy
from MonteCarlo import MonteCarlo
from mdp import BlocksWorld, BlocksWorldBuilder
from control import SimpleMonteCarloControl, SgdMonteCarloControl
from planner import Planner

from matplotlib import pyplot as plt


mdp_builder = BlocksWorldBuilder(blocks_world_size=7)
planner = Planner(planning_horizon=5)
ctrl = SgdMonteCarloControl(0.3)
mc = MonteCarlo(mdp_builder, planner, control=ctrl, 
                max_episode_length=14, planning_factor=0, plan_on_empty_policy=True)
learned_policy = mc.learn_policy(discount_rate=1, number_episodes=150, show_progress_bar=True)

#test_policy(ctrl, blocks_world, mgenerate_random_state verbose=False)

plt.plot(mc.returns)
plt.show()
