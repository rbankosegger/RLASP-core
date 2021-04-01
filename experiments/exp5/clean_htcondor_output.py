import glob
import pandas as pd

files = glob.glob('htcondor_workspace/*.csv')
df = pd.concat([pd.read_csv(f) for f in files], ignore_index = True)

# Make episodes start at 1
df.episode_id += 1

# Monte carlo has no learning rate parameter, but a default was chosen nevertheless. Delete that default.
monte_carlo_rows = df['arg_control_algorithm'] == 'monte_carlo'
df.loc[monte_carlo_rows, 'arg_learning_rate'] = None

def mdp_label(row):
    if row.arg_mdp == 'blocksworld':
        return f'{row.arg_blocks_world_size:1.0f}-Blocks World'
    if row.arg_mdp == 'sokoban':
        return f'Sokoban ({row.arg_sokoban_level_name})'

df['mdp_label'] = df.apply(mdp_label, axis=1)

def algorithm_label(row):
    if row.arg_control_algorithm == 'q_learning':
        return 'Standard QL'
    if row.arg_control_algorithm == 'q_learning_reversed_update':
        return 'Reversed-update QL'
    if row.arg_control_algorithm == 'monte_carlo':
        return 'First-visit MC'

df['algorithm_label'] = df.apply(algorithm_label, axis=1)

def planner_label(row):
    if row.arg_plan_for_new_states:
        return f'Plan on first visit (ph={row.arg_planning_horizon})'
    else:
        return 'Tabula rasa'

df['planner_label'] = df.apply(planner_label, axis=1)

def full_algorithm_label(row):

    if row.arg_control_algorithm == 'monte_carlo':
        return row.algorithm_label
    else:
        return f'{row.algorithm_label}, $\\alpha={row.arg_learning_rate}$'

df['full_algorithm_label'] = df.apply(full_algorithm_label, axis=1)

df.to_csv('returns.csv')

