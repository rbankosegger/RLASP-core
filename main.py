from tests import test_policy
from MonteCarlo import MonteCarlo
from BlocksWorld import BlocksWorld

from matplotlib import pyplot as plt

blocks_world = BlocksWorld(number_of_blocks=4)
mc = MonteCarlo(blocks_world, max_episode_length=10, planning_factor=0, plan_on_empty_policy=False, planning_horizon=0)
learned_policy = mc.learn_policy(discount_rate=1, number_episodes=150, show_progress_bar=True)  # {state : action}

test_policy(learned_policy, blocks_world, max_episode_length=10, verbose=False)

plt.plot(mc.return_ratios)
plt.show()
