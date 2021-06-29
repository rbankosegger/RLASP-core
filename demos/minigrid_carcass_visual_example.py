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
from mdp import GymMinigrid, GymMinigridBuilder, GymMinigridCustomLevelBuilder
from mdp.abstraction import Carcass

# The number of pixels rendered per tile
tile_size=40


world = """
    kW  kW  kW  kW  kW  kW
    kW  >   _   gDl _   kW
    kW  _   _   kW  _   kW
    kW  _   gK  kW  G   kW
    kW  kW  kW  kW  kW  kW

"""


mdp = GymMinigridCustomLevelBuilder(ascii_encoding=world).build_mdp()
abstract_mdp = Carcass(mdp, rules_filename='minigrid.lp', debug=True)

abstract_mdp.transition('forward')
abstract_mdp.transition('right')
abstract_mdp.transition('forward')
abstract_mdp.transition('pickup')
abstract_mdp.transition('left')
abstract_mdp.transition('left')
abstract_mdp.transition('forward')
abstract_mdp.transition('right')
abstract_mdp.transition('toggle')
abstract_mdp.transition('right')
abstract_mdp.transition('drop')
abstract_mdp.transition('pickup')

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

plt.title(abstract_mdp.state)

_ = input('Press any key to close')
