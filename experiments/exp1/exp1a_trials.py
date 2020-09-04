import os
import sys

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Framework imports
from MonteCarlo import MonteCarlo
from mdp import BlocksWorldBuilder
from control import SimpleMonteCarloControl

# 3rd-party imports
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt

number_of_trials = 20
number_of_episodes = 3000
blocks_world_sizes = [4, 5, 6, 7]

def run_trial(blocks_world_size):

    blocks_world_builder = BlocksWorldBuilder(blocks_world_size) 
    ctrl = SimpleMonteCarloControl()
    planner = None # This experiment does not use a planner.
    mc = MonteCarlo(blocks_world_builder, planner, control=ctrl, 
                    max_episode_length=blocks_world_size*2, 
                    planning_factor=0, plan_on_empty_policy=False,
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
for trial_number, blocks_world_size in enumerate(tqdm(blocks_world_sizes * number_of_trials, desc='Running trials')):
    data = run_trial(blocks_world_size)
    data['trial_number'] = trial_number
    data['blocks_world_size'] = blocks_world_size
    df = df.append(data, ignore_index=True)

df.to_csv('exp1a_data.csv')
