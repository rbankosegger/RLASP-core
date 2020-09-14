import copy
from mdp import BlocksWorldBuilder, VacuumCleanerWorldBuilder, SokobanBuilder
from control import *
from policy import *

from matplotlib import pyplot as plt
from tqdm import tqdm

blocks_world_size = 5
max_episode_length = 20
number_episodes = 300
planning_horizon = 4
planning_factor = 0
plan_for_new_states = True 

mdp_builder = BlocksWorldBuilder(blocks_world_size)
#mdp_builder = SokobanBuilder('suitcase-05-01')

sample_mdp = mdp_builder.build_mdp()
planner_policy = PlannerPolicy(planning_horizon, mdp_builder)

target_policy= QTablePolicy()
behavior_policy = PlanningExploringStartsPolicy(planner_policy, RandomPolicy(), QTablePolicy(),
                                              planning_factor, plan_for_new_states)
#behavior_policy = PlanningEpsilonGreedyPolicy(planner_policy, RandomPolicy(), QTablePolicy(),
#                                            epsilon=0.2)

control = FirstVisitMonteCarloControl(behavior_policy)
#control = MonteCarloSGDControl(target_policy, alpha=0.3)
control = QLearningReversedUpdateControl(target_policy, behavior_policy, alpha=0.3)
control = QLearningControl(target_policy, behavior_policy, alpha=0.3)


returns = []
returns_test = []
for _ in tqdm(range(number_episodes), total=number_episodes):

    mdp = mdp_builder.build_mdp()

    mdp_test = copy.deepcopy(mdp)
    control.generate_episode_with_target_policy(mdp_test, step_limit=max_episode_length)
    returns_test.append(mdp_test.return_history[0])

    control.learn_episode(mdp, step_limit=max_episode_length)
    returns.append(mdp.return_history[0])

plt.plot(returns, label='Behavior policy')
plt.plot(returns_test, label='Target policy')
plt.legend()
plt.show()
