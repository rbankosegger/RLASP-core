from mdp import BlocksWorldBuilder, VacuumCleanerWorldBuilder, SokobanBuilder
from control import *
from policy import *

from matplotlib import pyplot as plt
from tqdm import tqdm

blocks_world_size = 4
max_episode_length = 20
number_episodes = 300
planning_horizon = 3
planning_factor = 0
plan_for_new_states = True 

mdp_builder = BlocksWorldBuilder(blocks_world_size)
#mdp_builder = SokobanBuilder('suitcase-05-01')

sample_mdp = mdp_builder.build_mdp()
planner_policy = PlannerPolicy(planning_horizon, sample_mdp.interface_file_path,
                               sample_mdp.problem_file_path, sample_mdp.state_static)

target_policy= QTablePolicy()
#behavior_policy = PlanningExploringStartsPolicy(planner_policy, RandomPolicy(), QTablePolicy(),
#                                              planning_factor, plan_for_new_states)
behavior_policy = PlanningEpsilonGreedyPolicy(planner_policy, RandomPolicy(), QTablePolicy(),
                                            epsilon=0.2)

#control = FirstVisitMonteCarloControl(behavior_policy)
#control = MonteCarloSGDControl(target_policy, alpha=0.3)
#control = QLearningReversedUpdateControl(target_policy, behavior_policy, alpha=0.3)
control = QLearningControl(target_policy, behavior_policy, alpha=0.3)


returns = []
for _ in tqdm(range(number_episodes), total=number_episodes):
    mdp = mdp_builder.build_mdp()
    control.learn_episode(mdp, step_limit=max_episode_length)
    returns.append(mdp.return_history[0])

plt.plot(returns)
plt.show()
