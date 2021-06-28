import itertools
import os

# The maximum number of jobs to be submitted simulatneously to htcondor
max_batch_size = 1000

number_of_repititions = 20

learning_rates = [0.001, 0.003, 0.005, 0.01, 0.03, 0.05, 0.1, 0.3, 0.5]
epsilons = [0.05, 0.1, 0.2, 0.3]
minigrid_levels = [

    'MiniGrid-Empty-8x8-v0',
    'MiniGrid-FourRooms-v0',
    'MiniGrid-Dynamic-Obstacles-8x8-v0'
]

def setup(i, learning_rate, epsilon, minigrid_level, use_carcass):


    args = [
        f'--db_file=returns.{i:04d}.csv',
        f'--episodes=3000',
        f'--control_algorithm=q_learning',
        f'--learning_rate={learning_rate}',
        f'--epsilon={epsilon}',
        f'--no_planning'
    ]

    if use_carcass:
        args += [f'--carcass=minigrid.lp']

    args += [
        f'minigrid --minigrid_level={minigrid_level}'
    ]


    return ' '.join(args)

with open('1a_template.sh', 'r') as templatefile:
    template = templatefile.read()

parameters_list = list(itertools.product(learning_rates, epsilons, minigrid_levels, [True,False]))

batch = 0

for i, parameters in enumerate(parameters_list * number_of_repititions):

    if i % max_batch_size == 0:
        batch += 1

    path = f'htcondor_workspace/batch_{batch}'

    os.makedirs(path, exist_ok=True)


    with open(f'{path}/run.{i:04d}.sh', 'w') as runfile:

        runfile.write(template.format(args_imported_by_python=setup(i, *parameters)))
