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
import signal
from datetime import datetime

from tqdm import tqdm

keyboard_interrupt_occurred = False
def handle_keyboard_interrupt(sig, frame):
    global keyboard_interrupt_occurred
    keyboard_interrupt_occurred = True
    print('\nKeyboard interrupt detected! Quitting after saving this episode...')
signal.signal(signal.SIGINT, handle_keyboard_interrupt)

def write_experiment_data(data, filename):
    if filename:
        csv_headers = set()
        for row in data:
            csv_headers |= row.keys()

        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(csv_headers))
            writer.writeheader()
            writer.writerows(data)

def build_episode_generator(episode_limit):
    i = 0
    while True:
        yield i
        i += 1
        if episode_limit and i == episode_limit:
            return

def main():

    global keyboard_interrupt_occurred

    parser = argparse.ArgumentParser(description='Train a RLASP agent in a given MDP.')

    parser.add_argument('--no_progress_bar', help='Don\'t show progress in stdout',
                        dest='show_progress_bar', action='store_false')
    parser.set_defaults(show_progress_bar=True)

    parser.add_argument('--test_target_policy', help='Generate every episode, twice (with same starting state). Once with the behavior policy and learning as usual. Once with the target policy and no learning.',
                        dest='test_target_policy', action='store_true')
    parser.set_defaults(test_target_policy=False)

    parser.add_argument('--qtable_input', help='Provides a file location to read a qtable description from. This will be used to initialize the qtables in both behavior and target policy before training.', metavar='qtable.pickle', default=None)
    parser.add_argument('--qtable_output', help='Provides a file location to write a qtable description of the target policy after training.', metavar='qtable.pickle', default=None)

    parser.add_argument('--db_file', help='Location to store the generated data. If `None`, no file will be generated.', metavar='db_file.csv', default='out.csv')

    parser.add_argument('--episodes', help='The number of episodes to train for.', type=int, default=None)
    parser.add_argument('--max_episode_length', help='The maximum number of steps within an episode.', type=int, default=10)

    # Behavior policies
    parser.add_argument('--epsilon', help='The "epsilon" parameter for the epsilon-greedy behavior policy. Does nothing for other behavior policies.', type=float, default=0.3)
    parser.add_argument('--planning_horizon', help='The number of steps into the future considered by the planner', type=int, default=4)

    parser.add_argument('--no_planning', dest='plan_for_new_states', action='store_false')
    parser.add_argument('--yes_planning', dest='plan_for_new_states', action='store_true')
    parser.set_defaults(plan_for_new_states=False)

    # Control algorithms
    parser.add_argument('--control_algorithm', help='The control algorithm to be used for training', default='q_learning',
                              choices={'monte_carlo', 'q_learning', 'q_learning_reversed_update'})

    parser.add_argument('--learning_rate', help='The learning rate (also step-size parameter or alpha) considered by some control algorithms.', type=float, default=0.3)
    parser.add_argument('--initial_q_estimate', help='The starting q-value estimate for a new state-action pair.', type=float, default=0)

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
    parser_minigrid.add_argument('--minigrid_use_alternative_reward_system', 
                                 help='If `false`, use the original rewards with no discounting. If `true`, a discount factor is introduced and the reward for reaching the goal state will always be 1.',
                                 action='store_true', default=False)
    # Note: max_episode_length is handled internally by minigrid environments -> set it to `None`.
    parser_minigrid.set_defaults(mdp='minigrid', behavior_policy='planning_epsilon_greedy', max_episode_length=None)

    parser_vacuum = subparsers.add_parser('vacuumworld', help='The sliding puzzle.')
    parser_vacuum.set_defaults(mdp='vacuumworld', behavior_policy='planning_exploring_starts')

    args = parser.parse_args()


    if args.mdp == 'blocksworld':
        mdp_builder = BlocksWorldBuilder(args.blocks_world_size, reverse_stack_order = args.blocks_world_reversed_stack_order)
    elif args.mdp == 'sokoban':
        mdp_builder = SokobanBuilder(args.sokoban_level_name)
    elif args.mdp == 'slidingpuzzle':
        mdp_builder = SlidingPuzzleBuilder(args.sliding_puzzle_size, args.sliding_puzzle_missing_pieces)
    elif args.mdp == 'minigrid':
        mdp_builder = GymMinigridBuilder(args.minigrid_level, args.minigrid_fully_observable, args.minigrid_use_alternative_reward_system)

    elif args.mdp == 'vacuumworld':
        mdp_builder = VacuumCleanerWorldBuilder()

    if args.carcass:
        mdp_builder = CarcassBuilder(mdp_builder, args.carcass)


    behavior_policy_qtable = QTablePolicy(args.initial_q_estimate)
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

        target_policy = QTablePolicy(args.initial_q_estimate)
        if args.qtable_input:
            with open(args.qtable_input, 'rb') as f:
                target_policy.q_table = pickle.load(f)

        control = QLearningControl(target_policy, behavior_policy, args.learning_rate)

        qtable_policy_for_export = target_policy

    elif args.control_algorithm == 'q_learning_reversed_update':

        target_policy = QTablePolicy(args.initial_q_estimate)
        if args.qtable_input:
            with open(args.qtable_input, 'rb') as f:
                target_policy.q_table = pickle.load(f)

        control = QLearningReversedUpdateControl(target_policy, behavior_policy, args.learning_rate)

        qtable_policy_for_export = target_policy

    df = list()


    episode_ids = build_episode_generator(args.episodes)
    if args.show_progress_bar:
        if args.episodes:
            episode_ids = tqdm(episode_ids, total=args.episodes, bar_format='{l_bar}{bar:20}{r_bar}')
        else:
            episode_ids = tqdm(episode_ids)
    
    behavior_policy_return_cumulative = 0.0
    target_policy_return_cumulative = 0.0

    for episode_id in episode_ids:

        mdp = mdp_builder.build_mdp()
        control.try_initialize_state(mdp.state, mdp.available_actions)

        if args.test_target_policy:
            # Test the target policy and see how it would perform.
            mdp_target = copy.deepcopy(mdp)
            t0 = datetime.now()
            control.generate_episode_with_target_policy(mdp_target, step_limit=args.max_episode_length)
            t1 = datetime.now()
            time_spent_in_target_episode = (t1 - t0).total_seconds()

        # Train the target policy and the behavior policy on the mdp
        t0 = datetime.now()
        control.learn_episode(mdp, step_limit=args.max_episode_length)
        t1 = datetime.now()
        time_spent_in_behavior_episode = (t1 - t0).total_seconds()

        # Store results in the dataframe
        behavior_policy_return_cumulative += mdp.return_history[0]
        row = {
            ** { f'arg_{k}':v for k, v in vars(args).items() },

            'episode_id': episode_id,
            'behavior_policy_return': mdp.return_history[0],
            'behavior_policy_return_cumulative': behavior_policy_return_cumulative,
            'time_spent_in_behavior_episode': time_spent_in_behavior_episode,
        }

        if args.test_target_policy: 
            target_policy_return_cumulative += mdp_target.return_history[0]
            row |= {
                'target_policy_return': mdp_target.return_history[0],
                'time_spent_in_target_episode': time_spent_in_target_episode,
                'target_policy_return_cumulative': target_policy_return_cumulative,
            }

        df.append(row)

        write_experiment_data(df, args.db_file)

        if keyboard_interrupt_occurred:
            sys.exit('\nProgram exit due to keyboard interrupt.')


    if args.qtable_output:
        with open(args.qtable_output, 'wb') as f:
            pickle.dump(qtable_policy_for_export.q_table, f)

if __name__ == '__main__':
    main()
