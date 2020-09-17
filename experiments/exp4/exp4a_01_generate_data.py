import os
import sys
import copy
import random
import itertools

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# Framework imports
from control import FirstVisitMonteCarloControl, QLearningControl, QLearningReversedUpdateControl
from policy import *
from mdp import BlocksWorldBuilder

# 3rd-party imports
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt


""" EXPERIMENT PARAMETERS """

number_of_trials = 20

blocks_world_size = 5
mdp_builder = BlocksWorldBuilder(blocks_world_size)
number_of_episodes = 3000
max_episode_length = 20

planning_horizon = 4
planning_factor = 0

alphas = [0.1, 0.2, 0.3, 0.4]
tf = [True, False]

def main():

    setups = list()

    # Simple monte-carlo method as baseline
    setups += [{'cls':FirstVisitMonteCarloControl, 
                'kwargs':{}, 
                'plan_for_new_states': plan_for_new_states,
                'label':'First-visit MC' }
              for plan_for_new_states in tf]

    # Q-Learning with immediate (online) update.
    setups += [{'cls':QLearningControl, 
                'kwargs':{ 'alpha':alpha }, 
                'plan_for_new_states': plan_for_new_states,
                'label':f'QL with online update, $\\alpha={alpha}$'} \
               for alpha, plan_for_new_states in itertools.product(alphas, tf)]

    # Q-Learning with reversed update may be better.
    setups += [{'cls':QLearningReversedUpdateControl, 
                'kwargs':{ 'alpha':alpha }, 
                'plan_for_new_states': plan_for_new_states,
                'label':f'QL with reversed update after episode, $\\alpha={alpha}$' } \
               for alpha, plan_for_new_states in itertools.product(alphas, tf)]

    setups *= number_of_trials

    # Shuffle setups so that the progress bar can give a little more realistic time estimates
    # (not all setups take the same amount of time)
    random.shuffle(setups) 


    df = pd.DataFrame()
    for trial_number, setup in enumerate(tqdm(setups)):
        target_policy = QTablePolicy()
        behavior_policy = PlanningExploringStartsPolicy(PlannerPolicy(planning_horizon,
                                                                      mdp_builder),
                                                        RandomPolicy(),
                                                        QTablePolicy(),
                                                        planning_factor,
                                                        setup['plan_for_new_states'])

        control_class = setup['cls']
        kwargs = {
            **setup['kwargs'],
            'target_policy': target_policy,
            'behavior_policy': behavior_policy
        }

        if control_class == FirstVisitMonteCarloControl:
            # This control algorithm is on-policy -> behavior policy = target policy
            # thus behavior policy does not need to be provided as argument.
            kwargs.pop('behavior_policy')

        control = control_class(**kwargs)

        for episode in range(number_of_episodes):

            mdp = mdp_builder.build_mdp()

            # Make a completely separate copy of the mdp for evaluation
            mdp_test = copy.deepcopy(mdp)
            control.generate_episode_with_target_policy(mdp_test, step_limit=max_episode_length)

            control.learn_episode(mdp, step_limit=max_episode_length)

            row = {
                **setup,
                'trial': trial_number,
                'episode': episode,
                'behavior_policy_return': mdp.return_history[0],
                'target_policy_return': mdp_test.return_history[0]
            }

            df = df.append(pd.Series(row), ignore_index=True)

        df.to_csv('exp4a_02_data.csv')

if __name__ == '__main__':
    main()
