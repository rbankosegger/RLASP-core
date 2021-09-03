from .mdp import *
from .mdp.abstraction import Carcass, CarcassBuilder
from .control import *
from .policy import *

import argparse
import copy
import csv
import sys
import os
import pickle
from datetime import datetime

from tqdm import tqdm

def main():

    parser = argparse.ArgumentParser(description='Train a RLASP agent in a given MDP.')

    parser.add_argument('--no_progress_bar', help='Don\'t show progress in stdout',
                        dest='show_progress_bar', action='store_false')
    parser.set_defaults(show_progress_bar=True)

    parser.add_argument('--qtable_input', help='Provides a file location to read a qtable description from. This will be used to initialize the qtables in both behavior and target policy before training.', metavar='qtable.pickle', default=None)
    parser.add_argument('--qtable_output', help='Provides a file location to write a qtable description of the target policy after training.', metavar='qtable.pickle', default=None)

    parser.add_argument('--db_file', help='Location to store the generated data. If `None`, no file will be generated.', metavar='db_file.csv', default='out.csv')

    parser.add_argument('--episodes', help='The number of episodes to train for.', type=int, default=100)
    parser.add_argument('--max_episode_length', help='The maximum number of steps within an episode.', type=int, default=10)

    # Behavior policies
    parser.add_argument('--epsilon', help='The "epsilon" parameter for the epsilon-greedy behavior policy. Does nothing for other behavior policies.', type=float, default=0.3)
    parser.add_argument('--planning_horizon', help='The number of steps into the future considered by the planner', type=int, default=4)

    parser.add_argument('--no_planning', help='Don\'t show progress in stdout',
                        dest='plan_for_new_states', action='store_false')
    parser.set_defaults(plan_for_new_states=False)

    # Control algorithms
    parser.add_argument('--control_algorithm', help='The control algorithm to be used for training', default='q_learning',
                              choices={'monte_carlo', 'q_learning', 'q_learning_reversed_update'})

    parser.add_argument('--learning_rate', help='The learning rate (also step-size parameter or alpha) considered by some control algorithms.', type=float, default=0.3)

    # Abstraction / Carcass
    parser.add_argument('--carcass', help='The filename of the logic programm describing a carcass for the given MDP. The file must be located in `src/mdp/abstraction/carcass_rules`.', 
                        default=None)

    # MDP's
    subparsers = parser.add_subparsers(help='The markov decision procedure which should be learned.', title='Markov decision procedure')

    parser_blocksworld = subparsers.add_parser('blocksworld', help='The classic blocksworld.')
    parser_blocksworld.add_argument('--blocks_world_size', help='The number of blocks in the blocks world.', type=int, default=5)
    parser_blocksworld.add_argument('--blocks_world_reversed_stack_order', help='If true, block need to be stacked in reverse order.', 
                                    default=False, action='store_true')
    parser_blocksworld.set_defaults(mdp='blocksworld', behavior_policy='planning_epsilon_greedy')

    parser_sokoban = subparsers.add_parser('sokoban', help='The sokoban game.')
    parser_sokoban.add_argument('--sokoban_level_name', help='The sokoban level name.', default='suitcase-05-01')
    parser_sokoban.set_defaults(mdp='sokoban', behavior_policy='planning_epsilon_greedy')

    parser_slidingpuzzle = subparsers.add_parser('slidingpuzzle', help='The sliding puzzle.')
    parser_slidingpuzzle.add_argument('--sliding_puzzle_size', help='The sliding puzzle size.', type=int, default=2)
    parser_slidingpuzzle.add_argument('--sliding_puzzle_missing_pieces', help='Missing pieces in the sliding puzzle.', type=int, default=2)
    parser_slidingpuzzle.set_defaults(mdp='slidingpuzzle', behavior_policy='planning_epsilon_greedy')

    parser_minigrid = subparsers.add_parser('minigrid', help='The minigrid environment from openAI gym')
    parser_minigrid.add_argument('--minigrid_level', help='The minigrid level id', default='MiniGrid-MultiRoom-N6-v0')
    parser_minigrid.add_argument('--minigrid_fully_observable', help='If true, the entire environment will be part of the agents observatons. If false, the agent sees only its immediate environment',
                                 default=True)
    # Note: max_episode_length is handled internally by minigrid environments -> set it to `None`.
    parser_minigrid.set_defaults(mdp='minigrid', behavior_policy='planning_epsilon_greedy', max_episode_length=None)

    parser_vacuum = subparsers.add_parser('vacuumworld', help='The sliding puzzle.')
    parser_vacuum.set_defaults(mdp='vacuumworld', behavior_policy='planning_exploring_starts')

    args = parser.parse_args()

    initial_value_estimate = 0.3


    if args.mdp == 'blocksworld':
        mdp_builder = BlocksWorldBuilder(args.blocks_world_size, reverse_stack_order = args.blocks_world_reversed_stack_order)
    elif args.mdp == 'sokoban':
        mdp_builder = SokobanBuilder(args.sokoban_level_name)
    elif args.mdp == 'slidingpuzzle':
        mdp_builder = SlidingPuzzleBuilder(args.sliding_puzzle_size, args.sliding_puzzle_missing_pieces)
    elif args.mdp == 'minigrid':
        mdp_builder = GymMinigridBuilder(args.minigrid_level, args.minigrid_fully_observable)

    elif args.mdp == 'vacuumworld':
        mdp_builder = VacuumCleanerWorldBuilder()

    if args.carcass:
        mdp_builder = CarcassBuilder(mdp_builder, args.carcass)


    behavior_policy_qtable = QTablePolicy(initial_value_estimate)
    if args.qtable_input:
        with open(args.qtable_input, 'rb') as f:
            behavior_policy_qtable.q_table = pickle.load(f)


    if args.behavior_policy == 'planning_exploring_starts':

        behavior_policy = PlanningExploringStartsPolicy(PlannerPolicy(args.planning_horizon, mdp_builder),
                                                        RandomPolicy(),
                                                        behavior_policy_qtable,
                                                        planning_factor=0,
                                                        plan_for_new_states=args.plan_for_new_states)

    elif args.behavior_policy == 'planning_epsilon_greedy':

        behavior_policy = PlanningEpsilonGreedyPolicy(PlannerPolicy(args.planning_horizon, mdp_builder),
                                                      RandomPolicy(),
                                                      behavior_policy_qtable,
                                                      args.epsilon,
                                                      args.plan_for_new_states)

    if args.control_algorithm == 'monte_carlo':

        control = FirstVisitMonteCarloControl(behavior_policy)
        
        qtable_policy_for_export = behavior_policy.qtable_policy

    elif args.control_algorithm == 'q_learning':

        target_policy = QTablePolicy(initial_value_estimate)
        if args.qtable_input:
            with open(args.qtable_input, 'rb') as f:
                target_policy.q_table = pickle.load(f)

        control = QLearningControl(target_policy, behavior_policy, args.learning_rate)

        qtable_policy_for_export = target_policy

    elif args.control_algorithm == 'q_learning_reversed_update':

        target_policy = QTablePolicy(initial_value_estimate)
        if args.qtable_input:
            with open(args.qtable_input, 'rb') as f:
                target_policy.q_table = pickle.load(f)

        control = QLearningReversedUpdateControl(target_policy, behavior_policy, args.learning_rate)

        qtable_policy_for_export = target_policy

    df = list()

    episode_ids = range(args.episodes)
    if args.show_progress_bar:
        episode_ids = tqdm(episode_ids, total=args.episodes)
    
    behavior_policy_return_cumulative = 0.0
    target_policy_return_cumulative = 0.0


    for episode_id in episode_ids:

        mdp = mdp_builder.build_mdp()
        control.try_initialize_state(mdp.state, mdp.available_actions)

        # First, test the target policy and see how it would perform
        mdp_target = copy.deepcopy(mdp)
        t0 = datetime.now()
        control.generate_episode_with_target_policy(mdp_target, step_limit=args.max_episode_length)
        t1 = datetime.now()
        time_spent_in_target_episode = (t1 - t0).total_seconds()

        # Second, train the target policy and the behavior policy on the mdp
        t0 = datetime.now()
        control.learn_episode(mdp, step_limit=args.max_episode_length)
        t1 = datetime.now()
        time_spent_in_behavior_episode = (t1 - t0).total_seconds()

        # Compute cumulative returns
        behavior_policy_return_cumulative += mdp.return_history[0]
        target_policy_return_cumulative += mdp_target.return_history[0]

        # Finally, store all results in the dataframe
        row = {

            ** { f'arg_{k}':v for k, v in vars(args).items() },

            'episode_id': episode_id,
            'behavior_policy_return': mdp.return_history[0],
            'target_policy_return': mdp_target.return_history[0],
            'behavior_policy_return_cumulative': behavior_policy_return_cumulative,
            'target_policy_return_cumulative': target_policy_return_cumulative,
            'time_spent_in_behavior_episode': time_spent_in_behavior_episode,
            'time_spent_in_target_episode': time_spent_in_target_episode,
        }

        df.append(row)

    if args.db_file:

        csv_headers = set()
        for row in df:
            csv_headers |= row.keys()

        with open(args.db_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(csv_headers))
            writer.writeheader()
            writer.writerows(df)


    if args.qtable_output:
        with open(args.qtable_output, 'wb') as f:
            pickle.dump(qtable_policy_for_export.q_table, f)

if __name__ == '__main__':
    main()
