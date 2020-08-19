import os
import sys

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Framework imports
from MonteCarlo import *
from control import SimpleMonteCarloControl, SgdMonteCarloControl
import experiment_utilities

# 3rd-party imports
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('exp2a_data.csv', index_col=0)

df['algorithm'] = df.apply(lambda row: f'{row.algorithm}, $\\alpha={row.step_size_parameter}$' if not pd.isna(row.step_size_parameter) else row.algorithm, axis=1)

window_size = 10
df_smoothed = experiment_utilities.smooth_trial_outcomes(df, window_size)


_, axs = plt.subplots(1, 2, figsize=(10, 6))

sns.lineplot(x='episode', y='observed_returns', hue='algorithm', data=df, palette='colorblind', ci=None, ax=axs[0])
sns.lineplot(x='episode', y='observed_returns', hue='algorithm', data=df_smoothed, palette='colorblind', ci=None, ax=axs[1], legend=False)

number_of_trials = df.groupby(['algorithm', 'trial_number']).count().groupby('algorithm').count().iloc[0,0]


axs[0].set_ylabel(f'Mean return (n={number_of_trials})')
axs[1].set_ylabel(f'Running mean return (n={number_of_trials}, w={window_size})')

for ax in axs:
    ax.set_xlabel('Episode')
    ax.set_ylim(-20, 100)
    ax.set_xlim(0, df['episode'].max())

plt.suptitle('Tabula rasa agent in 5-blocks world')
plt.savefig('exp2a_fig.pdf', format='pdf')
plt.show()
