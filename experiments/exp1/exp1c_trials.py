import os
import sys

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Framework imports
from MonteCarlo import MonteCarlo
from mdp import BlocksWorldBuilder
from control import SimpleMonteCarloControl
from planner import Planner

# 3rd-party imports
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt

number_of_trials = 20
number_of_episodes = 1000
blocks_world_size = 7
planning_horizon = 12
planning_factors = [0.0, 0.5, 0.7, 1.0]

def run_trial(planning_factor):

    blocks_world_builder = BlocksWorldBuilder(blocks_world_size)
    ctrl = SimpleMonteCarloControl()
    planner = Planner(planning_horizon)

    mc = MonteCarlo(blocks_world_builder, planner, control=ctrl, 
                    max_episode_length=blocks_world_size*2, 
                    planning_factor=planning_factor, plan_on_empty_policy=False, 
                    exploring_starts=True, exploring_factor = 0)

    mc.learn_policy(number_episodes=number_of_episodes, show_progress_bar=True, evaluate_return_ratio=False)

    data = pd.DataFrame({
        'episode': range(len(mc.returns)),
        #'return_ratio': mc.return_ratios,
        'observed_returns' : mc.returns,
        #'optimal_returns': mc.optimal_returns
    })
    
    return data

df = pd.DataFrame()
for trial_number, planning_factor in enumerate(tqdm(planning_factors * number_of_trials, desc='Running trials')):
    data = run_trial(planning_factor)
    data['trial_number'] = trial_number
    data['planning_factor'] = planning_factor
    df = df.append(data, ignore_index=True)

df.to_csv('exp1c_data.csv')
