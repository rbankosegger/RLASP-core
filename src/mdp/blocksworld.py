import os
import clingo
import random
from typing import Set, List

from .markov_decision_procedure import MarkovDecisionProcedure

class BlocksWorld(MarkovDecisionProcedure):

    def __init__(self, state_initial: Set[str], state_static: Set[str]):

        # No discounting in any blocks world
        discount_rate = 1.0
        
        super().__init__(state_initial, state_static, discount_rate, 'blocksworld.lp')

class BlocksWorldBuilder():

    def __init__(self, blocks_world_size: int, state_enumeration_limit: int = 9, state_static: Set = None, reverse_stack_order = False):

        self.blocks_world_size: int = blocks_world_size
        self.state_enumeration_limit: int = state_enumeration_limit

        # Used for sampling random states
        self._g_cache = dict()

        self.block_terms: List[str] = [f'b{n}' for n in range(blocks_world_size)]
        if reverse_stack_order:
            self.block_terms = list(reversed(self.block_terms))

        if state_static:
            self.state_static: Set = state_static
        else:
            self.state_static: Set = set(f'subgoal({x},{y})' for (x,y) in zip(self.block_terms, ['table']+self.block_terms))

        self.file_name: str  = 'blocksworld_initial_states.lp'
        self.file_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file_name)

        if blocks_world_size <= state_enumeration_limit:

            self.all_states: List[Set[str]] = self._generate_all_states()


        sample_mdp = self.build_mdp()
        self.mdp_interface_file_path = sample_mdp.interface_file_path
        self.mdp_problem_file_path = sample_mdp.problem_file_path
        self.mdp_state_static = sample_mdp.state_static

    def build_mdp(self):

        while True:

            state_start = self._generate_random_state()
            mdp = BlocksWorld(state_start, self.state_static)

            # Continue generating random start states until we find one that is not equal to 
            # the goal state.
            if len(mdp.available_actions) > 0:
                break

        return mdp

    def _generate_random_state(self):

        if self.blocks_world_size <= self.state_enumeration_limit:
            # print('true random enumerated')
            return random.choice(self.all_states)
        #   else:
        #       print('pseudo random')
        #       return self._generate_pseudo_random_state()
        else:
            # print('true random scalable')
            return self._generate_random_uniform_state()

    def _g(self, n, k):
        # A count of the number of states 
        # that extend a part-state 
        # in which there are k grounded towers and n ungrounded ones.
        # See p.123 of Slaney, Thiebaux. Blocks World revisited. 2021.

        if n == 0:
            return 1

        # Chache the results to reduce redundant computations
        if (n,k) in self._g_cache.keys():
            return self._g_cache[n,k]

        x = self._g(n-1,k+1) + (n-1+k) * self._g(n-1,k)
        self._g_cache[n,k] = x
        return x

    def _generate_random_uniform_state(self):

        # Algorithm from page 126 of:
        # Slaney, Thiebaux. Blocks World revisited. 2021.
        # Samples blocksworld states from a random uniform distribution.
        # Does not scale well but fine for our purposes.
        # Better would be the algorithm on page 127.

        # (1) start with an empty table and n ungrounded towers each consisting of a single block,
        ungrounded_towers = [ [b] for b in self.block_terms ]
        grounded_towers = []

        # (2) repeat until all towers are grounded:
        while(len(ungrounded_towers) > 0):
        
            phi = len(ungrounded_towers)
            tau = len(grounded_towers)
        
            # (2a) arbitrarily select one of the φ yet ungrounded towers,
            t = ungrounded_towers.pop(random.randrange(len(ungrounded_towers)))
        
            if random.uniform(0.0,1.0) <= self._g(phi-1,tau+1)/self._g(phi,tau):
                # (2b) select the table with probability g(φ − 1, τ + 1)/g(φ, τ ) ...
                grounded_towers.append(t)
            else:
                # (2b ct'd.) ... or one of the other towers (grounded or not) 
                # each with probability g(φ − 1, τ )/g(φ, τ ), 
                # and place the selected ungrounded tower onto it.
                i = random.randrange(len(ungrounded_towers) + len(grounded_towers))
                if i < len(ungrounded_towers):
                    ungrounded_towers[i] += t
                else:
                    grounded_towers[i-len(ungrounded_towers)] += t
        
        generated_state = set()
        for t in grounded_towers:
            generated_state |= { f'on({x},{y})' for x,y in zip(t, ['table'] + t) }
        
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
