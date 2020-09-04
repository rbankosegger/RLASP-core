import os
import sys

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Framework imports
from MonteCarlo import MonteCarlo
from mdp import BlocksWorldBuilder
from control import SimpleMonteCarloControl, SgdMonteCarloControl
from planner import Planner

# 3rd-party imports
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt


""" EXPERIMENT PARAMETERS """

number_of_trials = 20
number_of_episodes = 2000
blocks_world_size = 7
planning_horizon = 5

step_size_parameters = [1, 0.8, 0.3, 0.03]


""" SETUP EXPERIMENT """

experiments = []

for _ in range(number_of_trials):

    # Control case: Monte carlo control such as in the bachelor's project, without planning.

    blocks_world_builder = BlocksWorldBuilder(blocks_world_size)
    planner = Planner(planning_horizon)
    ctrl = SimpleMonteCarloControl()
    mc = MonteCarlo(blocks_world_builder, planner, control=ctrl, 
                    max_episode_length=blocks_world_size*2, 
                    planning_factor=0, plan_on_empty_policy=True,
                    exploring_starts=True, exploring_factor = 0)

    experiments.append(('Mean-based', None, mc))

for step_size_parameter in step_size_parameters * number_of_trials:

    # Other cases: Gradient-based agents with different step size parameter values

    blocks_world_builder = BlocksWorldBuilder(blocks_world_size)
    planner = Planner(planning_horizon)
    ctrl = SgdMonteCarloControl(step_size_parameter)
    mc = MonteCarlo(blocks_world_builder, planner, control=ctrl, 
                    max_episode_length=blocks_world_size*2, 
                    planning_factor=0, plan_on_empty_policy=True,
                    exploring_starts=True, exploring_factor = 0)

    experiments.append(('Gradient-based', step_size_parameter, mc))


""" RUN EXPERIMENT """

df = pd.DataFrame()
for trial_number, (algorithm_label, step_size_parameter, monte_carlo_algorithm) in enumerate(tqdm(experiments)):

    monte_carlo_algorithm.learn_policy(number_episodes=number_of_episodes, show_progress_bar=True, 
                                       evaluate_return_ratio=False)

    data = pd.DataFrame({
        'episode': range(len(monte_carlo_algorithm.returns)),
        'observed_returns' : monte_carlo_algorithm.returns,
    })

    data['trial_number'] = trial_number

    data['algorithm'] = algorithm_label
    data['step_size_parameter'] = step_size_parameter

    df = df.append(data, ignore_index=True)

df.to_csv('exp2b_data.csv')
