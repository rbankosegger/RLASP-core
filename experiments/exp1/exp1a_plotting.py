import os
import sys

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Framework imports
from MonteCarlo import *
from control import SimpleMonteCarloControl, SgdMonteCarloControl

# 3rd-party imports
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('exp1a_data.csv', index_col=0)

sns.lineplot(x='episode', y='observed_returns', hue='blocks_world_size', data=df, palette='colorblind', ci=None)
#sns.despine(trim=True)

number_of_trials = df.groupby(['blocks_world_size', 'trial_number']).count().groupby('blocks_world_size').count().iloc[0,0]


plt.title('Tabula rasa agent in different blocks worlds')
plt.xlabel('Episode')
plt.ylabel(f'Mean return (n={number_of_trials})')
plt.ylim(-20, 100)
plt.yticks(range(-20,101,20))
plt.xlim(0, df['episode'].max())
plt.savefig('exp1a_fig.pdf', format='pdf')
#plt.show()
