import itertools


number_of_repititions = 1

learning_rates = [0.1, 0.3, 0.6]
tf = [True, False]


mdps = ['blocksworld --blocks_world_size=5', 
        '--epsilon=0.2 sokoban --sokoban_level_name=suitcase-05-01']


def setup(i, mdp, la, no_planning):

    (control_algorithm, learning_rate) = la

    args = [
        f'--db_file=returns.{i:04d}.csv',
        f'--episodes=3000',
        f'--max_episode_length=15', 
        f'--planning_horizon=4',
        f'--control_algorithm={control_algorithm}',
    ]

    if learning_rate:
        args.append(f'--learning_rate={learning_rate}')

    if no_planning:
        args.append('--no_planning')

    args.append(mdp)

    return ' '.join(args)

control_algorithms = [('monte_carlo', None)] \
        + [('q_learning', lr) for lr in learning_rates] \
        + [('q_learning_reversed_update', lr) for lr in learning_rates]

with open('template.sh', 'r') as templatefile:
    template = templatefile.read()

parameters_list = list(itertools.product(mdps, control_algorithms, [True, False]))
for i, parameters in enumerate(parameters_list * number_of_repititions):
    with open(f'htcondor_workspace/run.{i:04d}.sh', 'w') as runfile:
        runfile.write(template.format(args_imported_by_python=setup(i, *parameters)))
