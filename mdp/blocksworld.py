import os
import clingo
import random
from typing import Set, List

from .markov_decision_procedure import MarkovDecisionProcedure

class BlocksWorld(MarkovDecisionProcedure):

    def __init__(self, initial_state: Set[str], goal_state: Set[str]):

        # No discounting in any blocks world
        discount_rate = 1.0

        super().__init__(initial_state, goal_state, discount_rate, 'blocksworld.lp')

class BlocksWorldBuilder():

    def __init__(self, blocks_world_size: int, state_enumeration_limit: int = 9):

        self.blocks_world_size: int = blocks_world_size
        self.state_enumeration_limit: int = state_enumeration_limit

        self.block_terms: List[str] = [f'b{n}' for n in range(blocks_world_size)]

        self.file_name: str  = 'blocksworld_initial_states.lp'
        self.file_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file_name)

        if blocks_world_size <= state_enumeration_limit:

            self.all_states: List[Set[str]] = self._generate_all_states()


    def build_mdp(self):

        # Use goal state in which all blocks are stacked in order
        goal_state = set(f'on({x},{y})' for (x,y) in zip(self.block_terms, ['table']+self.block_terms))

        # Continue generating random start states until we find one that is not equal to 
        # the goal state.
        while True:
            start_state = self._generate_random_state()

            if start_state != goal_state:
                break

        return BlocksWorld(start_state, goal_state)

    def _generate_random_state(self):

        if self.blocks_world_size <= self.state_enumeration_limit:
            return random.choice(self.all_states)
        else:
            return self._generate_pseudo_random_state()

    def _generate_pseudo_random_state(self):
        
        generated_state = set()
        placed = []
        shuffled_blocks = random.sample(block_terms, len(self.block_terms))

        for t, block in enumerate(shuffled_blocks):

            if 1.0 / (t+1.0) >= random.random():
                generated_state.add(f'on({block}, table)')
            else:
                generated_state.add(f'on({block},{random.choice(placed)})')

            placed.append(block)

        return generated_state

    def _generate_all_states(self):

        ctl = clingo.Control()

        ctl.load(self.file_path)
        ctl.add('base', [], ' '.join(f'block({t}).' for t in self.block_terms))
        ctl.add('base', [], '#show state/1.')
        ctl.configuration.solve.models = 0


        ctl.ground(parts=[('base', [])])
        models = ctl.solve(yield_=True)

        generated_states = [frozenset(str(symbol.arguments[0]) 
                                        for symbol in model.symbols(shown=True))
                                for model in models]

        return generated_states
