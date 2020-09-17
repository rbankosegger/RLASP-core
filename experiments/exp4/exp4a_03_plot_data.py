import os
import sys

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

import experiment_utilities
from exp4a_01_generate_data import number_of_trials, number_of_episodes, blocks_world_size, planning_horizon, max_episode_length
import control

# 3rd-party imports
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('exp4a_02_data.csv', index_col=0)

def map_algorithm_label(s):
    if 'QLearningControl' in s:
        return 'Standard QL'
    elif 'QLearningReversedUpdateControl' in s:
        return 'Reversed-update QL'
    elif 'FirstVisitMonteCarloControl' in s:
        return 'First-visit MC'

# Make episodes start at 1
df['episode'] += 1

df['algorithm_label'] = df['cls'].map(map_algorithm_label)
df['alpha_label'] = df['kwargs'].map(lambda kwargs: eval(kwargs).get('alpha', 'n/a')) 
df['planner_label'] = df['plan_for_new_states'].map(lambda plan: f'Plan on first visit (ph={planning_horizon})' if plan else 'Tabula rasa')

def map_shorter_label(s):
    return s.replace('QL with online update', 'Standard QL', 1) \
            .replace('QL with reversed update after episode', 'Reversed-update QL', 1)

df['label'] = df['label'].map(map_shorter_label)

df_molten = df.melt(id_vars=['algorithm_label', 'alpha_label', 'episode', 'label', 'planner_label', 'plan_for_new_states'],
                    value_vars=['behavior_policy_return', 'target_policy_return'])


# Set style
#sns.set_theme(style="ticks")
sns.set_style('whitegrid')


# Plot boxplot
selector = df['episode'].isin([150, 3000])
g = sns.catplot(x='algorithm_label', y='behavior_policy_return', 
            kind='swarm',
            order=['First-visit MC', 'Standard QL', 'Reversed-update QL'],
            hue='alpha_label', hue_order=['n/a', 0.1, 0.2, 0.3, 0.4],
            col='planner_label',
            row='episode',
            data=df[selector],
            palette='colorblind',
            dodge=True,
            aspect=4/3.0, height=3.4,
            facet_kws={'subplot_kws':{'yticks':range(-25, 101, 25), 'ylim':(-25, 105)}})
    
plt.suptitle(f'Comparison of all agents in a {blocks_world_size}-blocks world (episode length limit of {max_episode_length})')
g.set_titles('Results at {row_name} episodes \n{col_name}')
g.set_ylabels(f'Return for behavior policy')
g.set_xlabels('')
plt.tight_layout(h_pad=3.5, rect=[0,0,0.9,0.95])
plt.savefig('exp4a_04_plot_1.pdf', format='pdf')
plt.clf()





selector = (df_molten['label'].isin(['First-visit MC',
                                     'Standard QL, $\\alpha=0.1$',
                                     'Reversed-update QL, $\\alpha=0.4$']))

g = sns.FacetGrid(df_molten[selector], col='label', row='planner_label', hue='variable',
                  col_order=['First-visit MC', 'Standard QL, $\\alpha=0.1$', 'Reversed-update QL, $\\alpha=0.4$'],
                  aspect=0.9, height=3.4,
                  subplot_kws={'xticks':range(0, 3001, 1000), 'yticks':range(-25, 101, 25), 
                               'xlim': (0, 3030), 'ylim':(-25, 105)})
g.map(sns.lineplot, 'episode', 'value', ci=None, alpha=0.8, palette='colorblind')
g.add_legend()
g.set_ylabels(f'Mean return ($n={number_of_trials}$)')
g.set_xlabels(f'Episode')
plt.tight_layout(h_pad=3.5, rect=[0,0,0.8,0.9])
g.set_titles('{col_name}\n{row_name}')
plt.suptitle(f'Comparison of selected agents in a {blocks_world_size}-blocks world (episode length limit of {max_episode_length})')
plt.savefig('exp4a_04_plot_2.pdf', format='pdf')
plt.clf()





selector = (df_molten['algorithm_label'] == 'Standard QL') \
            & (df_molten['episode'] <= 1000)
g = sns.FacetGrid(df_molten[selector], row='planner_label', col='alpha_label', hue='variable', 
                  aspect=0.7, height=3.4,
                  subplot_kws={'xticks':range(0, 1001, 250), 'yticks':range(-25, 101, 25), 
                               'xlim': (0, 1010), 'ylim':(-25, 105)})
g.map(sns.lineplot, 'episode', 'value', ci=None, alpha=0.8, palette='colorblind')
g.add_legend()
g.set_ylabels(f'Mean return ($n={number_of_trials}$)')
g.set_titles('{row_name}, $\\alpha={col_name}$')
plt.tight_layout(h_pad=3.5, rect=[0,0,0.85,0.9])
plt.suptitle(f'Standard Q-learning agents in a {blocks_world_size}-blocks world (episode length limit of {max_episode_length})')
plt.savefig('exp4a_04_plot_3.pdf', format='pdf')
plt.clf()





selector = (df_molten['algorithm_label'] == 'Reversed-update QL') \
            & (df_molten['episode'] <= 1000)
g = sns.FacetGrid(df_molten[selector], row='planner_label', col='alpha_label', hue='variable', 
                  aspect=0.7, height=3.4,
                  subplot_kws={'xticks':range(0, 1001, 250), 'yticks':range(-25, 101, 25), 
                               'xlim': (0, 1010), 'ylim':(-25, 105)})
g.map(sns.lineplot, 'episode', 'value', ci=None, alpha=0.8, palette='colorblind')
g.add_legend()
g.set_ylabels(f'Mean return ($n={number_of_trials}$)')
g.set_titles('{row_name}, $\\alpha={col_name}$')
plt.tight_layout(h_pad=3.5, rect=[0,0,0.85,0.9])
plt.suptitle(f'Reversed-update Q-learning agents in a {blocks_world_size}-blocks world (episode length limit of {max_episode_length})')
plt.savefig('exp4a_04_plot_4.pdf', format='pdf')
plt.clf()
