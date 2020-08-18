from tests import test_policy
from MonteCarlo import MonteCarlo
from BlocksWorld import BlocksWorld
from control import SimpleMonteCarloControl, SgdMonteCarloControl

from matplotlib import pyplot as plt

blocks_world = BlocksWorld(number_of_blocks=7)
ctrl = SgdMonteCarloControl(blocks_world, 0.3)
mc = MonteCarlo(blocks_world, control=ctrl, 
                max_episode_length=14, planning_factor=0, plan_on_empty_policy=True, planning_horizon=6)
learned_policy = mc.learn_policy(discount_rate=1, number_episodes=150, show_progress_bar=True)  # {state : action}

#test_policy(ctrl, blocks_world, max_episode_length=10, verbose=False)

plt.plot(mc.return_ratios)
plt.show()
