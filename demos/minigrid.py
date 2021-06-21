import sys
import os
import random
import re

import gym
import gym_minigrid

from matplotlib import pyplot as plt
from matplotlib import patches as patches

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

# Framework imports
from mdp import GymMinigrid, GymMinigridBuilder
from mdp.abstraction import Carcass

# The number of pixels rendered per tile
tile_size=40

#builder = GymMinigridBuilder('MiniGrid-FourRooms-v0')
#builder = GymMinigridBuilder('MiniGrid-DoorKey-16x16-v0')
#builder = GymMinigridBuilder('MiniGrid-MultiRoom-N6-v0')
#builder = GymMinigridBuilder('MiniGrid-Dynamic-Obstacles-16x16-v0')
builder = GymMinigridBuilder('MiniGrid-Dynamic-Obstacles-Random-5x5-v0')
#builder = GymMinigridBuilder('MiniGrid-LavaCrossingS9N1-v0')
#builder = GymMinigridBuilder('MiniGrid-LavaCrossingS11N5-v0')
#builder = GymMinigridBuilder('MiniGrid-LavaGapS7-v0')
#builder = GymMinigridBuilder('MiniGrid-LavaGapS6-v0')
#builder = GymMinigridBuilder('MiniGrid-LavaGapS5-v0')
#builder = GymMinigridBuilder('MiniGrid-Empty-Random-5x5-v0')


mdp = builder.build_mdp()
abstract_mdp = Carcass(mdp, 'minigrid.lp', debug=True)
action = random.choice(list(abstract_mdp.available_actions))
next_state, next_reward = abstract_mdp.transition(action)
print(next_state)
print(next_reward)
mdp.env.render(tile_size=tile_size, highlight=False)

def fill(x, y, color, alpha):

    hatch_legend = {
        'magenta' : '..',
        'white' : 'OO',
        'red' : 'xx'
    }
    global tile_size
    hatch = hatch_legend.get(color, '/')
    rect = patches.Rectangle((x*tile_size, y*tile_size), tile_size, tile_size, 
                             linewidth=0, facecolor=color, alpha=alpha, 
                             hatch=hatch, edgecolor=color,
                             fill=False)
    plt.gca().add_patch(rect)


p = re.compile('^highlight\(([0-9]+),([0-9]+),([a-z]+)\)$')
p2 = re.compile('^line\(\(([0-9]+),([0-9]+)\),\(([0-9]+),([0-9]+)\),([a-z]+)\)$')
p3 = re.compile('^arrow\(\(([0-9]+),([0-9]+)\),\(([0-9]+),([0-9]+)\),([a-z]+)\)$')

for s in abstract_mdp._asp_model_symbols:

    print(s)

    m = p.match(str(s))

    if m:
        gs = m.groups()
        x = int(gs[0])
        y = int(gs[1])
        c = gs[2]
        fill(x, y, c, alpha=0.7)

    m2 = p2.match(str(s))

    if m2:
        x1,y1,x2,y2 = [(0.5+int(s)) * tile_size for s in m2.groups()[:4]]
        c = m2.groups()[4]
        plt.plot([x1,x2], [y1,y2], '-', color=c, alpha=1)

    m3 = p3.match(str(s))

    if m3:
        x1,y1,x2,y2 = [(0.5+int(s)) * tile_size for s in m3.groups()[:4]]
        c = m3.groups()[4]
        plt.arrow(x1, y1, x2-x1, y2-y1, 
                  color=c, 
                  width=2,
                  head_width=15,
                  length_includes_head=True)


plt.show()

_ = input('Press any key to close')
