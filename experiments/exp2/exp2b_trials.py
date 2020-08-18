import os
import sys

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Framework imports
from MonteCarlo import *
from control import SimpleMonteCarloControl, SgdMonteCarloControl

# 3rd-party imports
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt


""" EXPERIMENT PARAMETERS """

number_of_trials = 4
number_of_episodes = 2000
blocks_world_size = 7
planning_horizon = 4

step_size_parameters = [1, 0.8, 0.3, 0.03]


""" SETUP EXPERIMENT """

experiments = []

for _ in range(number_of_trials):

    # Control case: Monte carlo control such as in the bachelor's project, without planning.

    blocks_world = BlocksWorld(blocks_world_size)
    ctrl = SimpleMonteCarloControl(blocks_world)
    mc = MonteCarlo(blocks_world, control=ctrl, max_episode_length=blocks_world_size*2, 
                    planning_factor=0, plan_on_empty_policy=True, planning_horizon=planning_horizon)

    experiments.append(('Mean-based', None, mc))

for step_size_parameter in step_size_parameters * number_of_trials:

    # Other cases: Gradient-based agents with different step size parameter values

    blocks_world = BlocksWorld(blocks_world_size)
    ctrl = SgdMonteCarloControl(blocks_world, step_size_parameter)
    mc = MonteCarlo(blocks_world, control=ctrl, max_episode_length=blocks_world_size*2, 
                    planning_factor=0, plan_on_empty_policy=True, planning_horizon=planning_horizon)

    experiments.append(('Gradient-based', step_size_parameter, mc))


""" RUN EXPERIMENT """

df = pd.DataFrame()
for trial_number, (algorithm_label, step_size_parameter, monte_carlo_algorithm) in enumerate(tqdm(experiments)):

    monte_carlo_algorithm.learn_policy(discount_rate=1, number_episodes=number_of_episodes, show_progress_bar=True)

    data = pd.DataFrame({
        'episode': range(len(monte_carlo_algorithm.return_ratios)),
        'return_ratio': monte_carlo_algorithm.return_ratios,
        'observed_returns' : monte_carlo_algorithm.returns,
        'optimal_returns': monte_carlo_algorithm.optimal_returns
    })

    data['trial_number'] = trial_number

    data['algorithm'] = algorithm_label
    data['step_size_parameter'] = step_size_parameter

    df = df.append(data, ignore_index=True)

df.to_csv('exp2b_data.csv')
