import os
import sys, getopt
import copy
import random
import itertools

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

# Framework imports
from control import FirstVisitMonteCarloControl, QLearningControl, QLearningReversedUpdateControl
from policy import *
from mdp import BlocksWorldBuilder, SokobanBuilder

# 3rd-party imports
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt


""" EXPERIMENT PARAMETERS """

#number_of_trials = 3

blocks_world_size = 5
mdp_builder = BlocksWorldBuilder(blocks_world_size)
number_of_episodes = 3000
max_episode_length = 15

planning_horizon = 4
planning_factor = 0

alphas = [0.1, 0.2, 0.3, 0.4]
tf = [True, False]


def handle_args(argv):
    usage = 'Required: `-d db_file.csv -j job_id -s setup`'
    db_file = None
    job_id = None
    setup = None

    try:
        opts, args = getopt.getopt(argv, 'hd:j:s:')
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt == '-d':
            db_file = arg
        elif opt == '-j':
            job_id = int(arg)
        elif opt == '-s':
            setup = int(arg)


    if db_file is None or job_id is None or setup is None:
        print(usage)
        sys.exit(2)

    return db_file, job_id, setup

def main(argv):

    setups = list()

    mdp_label = f'{blocks_world_size}-Blocks World'
    mdp_builder = BlocksWorldBuilder(blocks_world_size)


    # Simple monte-carlo method as baseline
    setups += [{'mdp_label': mdp_label,
                'mdp_builder':mdp_builder,
                'cls':FirstVisitMonteCarloControl, 
                'kwargs':{}, 
                'plan_for_new_states': plan_for_new_states,
                'label':'First-visit MC' }
              for plan_for_new_states in tf]

    # Q-Learning with immediate (online) update.
    setups += [{'mdp_label': mdp_label,
                'mdp_builder':mdp_builder,
                'cls':QLearningControl, 
                'kwargs':{ 'alpha':alpha }, 
                'plan_for_new_states': plan_for_new_states,
                'label':f'QL with online update, $\\alpha={alpha}$'} \
               for alpha, plan_for_new_states in itertools.product(alphas, tf)]

    # Q-Learning with reversed update may be better.
    setups += [{'mdp_label': mdp_label,
                'mdp_builder':mdp_builder,
                'cls':QLearningReversedUpdateControl, 
                'kwargs':{ 'alpha':alpha }, 
                'plan_for_new_states': plan_for_new_states,
                'label':f'QL with reversed update after episode, $\\alpha={alpha}$' } \
               for alpha, plan_for_new_states in itertools.product(alphas, tf)]



    db_file, job_id, setup_id = handle_args(argv)

    try:
        setup = setups[setup_id]
    except IndexError:
        print(f'Setup id ({setup_id}) out of range. Must be smaller than {len(setups)}.')
        sys.exit(2)


    df = pd.DataFrame()

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

    for episode in tqdm(list(range(number_of_episodes))):

        mdp = mdp_builder.build_mdp()

        # Make a completely separate copy of the mdp for evaluation
        mdp_test = copy.deepcopy(mdp)
        control.generate_episode_with_target_policy(mdp_test, step_limit=max_episode_length)

        control.learn_episode(mdp, step_limit=max_episode_length)

        row = {
            **setup,
            'episode': episode,
            'behavior_policy_return': mdp.return_history[0],
            'target_policy_return': mdp_test.return_history[0],

            'job_id': job_id,
            'setup_id': setup_id
        }

        df = df.append(pd.Series(row), ignore_index=True)

    df.to_csv(db_file)

if __name__ == '__main__':
    main(sys.argv[1:])
