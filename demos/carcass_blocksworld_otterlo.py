import os
import sys

# Make sure the path of the framework is included in the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from mdp import BlocksWorld, BlocksWorldBuilder
from mdp import BlocksWorld, BlocksWorldBuilder
from mdp.abstraction import Carcass

bwb = BlocksWorldBuilder(blocks_world_size=3)

abstract_states_collected = dict()


for state in bwb.all_states:

    mdp = BlocksWorld(state_initial=state, state_static={'subgoal(b1,b2)', 'subgoal(b2,b3)'})
    abstract_mdp = Carcass(mdp, 'blocksworld_otterlo_example.lp')
    abstract_states_collected[abstract_mdp.state] = abstract_states_collected.get(abstract_mdp.state, set()) | {(mdp, abstract_mdp)}



print('+++')
print()
for abstract_state_label, ground_states in sorted(abstract_states_collected.items()):

    print('Abstract state:', abstract_state_label)
    
    for (mdp, abstract_mdp) in ground_states:
        print('\t', sorted(mdp.state))

        for abstract_action in abstract_mdp.available_actions:

            print('\t\t', 'ABSTRACT: ', abstract_action)
            print('\t\t', 'GROUND:   ', abstract_mdp.ground_actions_of(abstract_action))
        print()

    print()

