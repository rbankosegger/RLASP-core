from tests import test_policy
from MonteCarlo import MonteCarlo
from mdp import BlocksWorldBuilder, VacuumCleanerWorldBuilder
from control import SimpleMonteCarloControl, SgdMonteCarloControl
from planner import Planner

from matplotlib import pyplot as plt


mdp_builder = BlocksWorldBuilder(blocks_world_size=7)
#mdp_builder = VacuumCleanerWorldBuilder()
planner = Planner(planning_horizon=12)
ctrl = SimpleMonteCarloControl()
mc = MonteCarlo(mdp_builder, planner, control=ctrl, 
                max_episode_length=14, planning_factor=0.7, plan_on_empty_policy=False,
                exploring_starts=True, exploring_factor = 0.0)

learned_policy = mc.learn_policy(number_episodes=300, show_progress_bar=True, evaluate_return_ratio=True)

# Get sub-policy statistics to make sure they work correctly
n = float(sum(cnt for cnt in mc.count_sub_policies.values()))
print([(pol, cnt / n) for pol, cnt in mc.count_sub_policies.items()])

#test_policy(ctrl, blocks_world, mgenerate_random_state verbose=False)

plt.plot(mc.returns)
plt.show()
