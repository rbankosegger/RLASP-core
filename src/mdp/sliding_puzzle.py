import os
import clingo
import random
from typing import Set, List

from .markov_decision_procedure import MarkovDecisionProcedure

class SlidingPuzzle(MarkovDecisionProcedure):

    def __init__(self, state_initial: Set[str], state_static: Set[str]):

        # TODO: check
        # No discounting for Sliding
        discount_rate = 1.0
        file_name = 'sliding_puzzle.lp'

        super().__init__(state_initial, state_static, discount_rate, file_name)

class SlidingPuzzleBuilder:

    def __init__(self, puzzle_size: int, missing_pieces: int, state_enumeration_limit: int = 9):

        self.puzzle_size: int = puzzle_size
        self.missing_pieces: int = missing_pieces
        self.state_enumeration_limit: int = state_enumeration_limit

        self.piece_terms: List[str] = [f'p{n}' for n in range(self.puzzle_size**2-self.missing_pieces)]

        self.file_name: str  = 'sliding_puzzle_initial_states.lp'
        self.file_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file_name)

        if puzzle_size <= state_enumeration_limit:
            self.all_states: List[Set[str]] = self._generate_all_states()

        sample_mdp = self.build_mdp()
        self.mdp_interface_file_path = sample_mdp.interface_file_path
        self.mdp_problem_file_path = sample_mdp.problem_file_path
        self.mdp_state_static = sample_mdp.state_static

    def build_mdp(self):

        # Use goal state in which all pieces are in numerical order
        state_static = set()
        positions = iter((i,j) for i in range(self.puzzle_size) for j in range(self.puzzle_size))
        for piece in self.piece_terms:
            position = next(positions)
            state_static.add('subgoal({},{},{})'.format(piece, position[0], position[1]))

        while True:

            state_start = self._generate_random_state()
            mdp = SlidingPuzzle(state_start, state_static)

            # Continue generating random start states until we find one that is not equal to
            # the goal state.
            # For the sliding puzzle this condition is not good enough as there are plenty
            # problems with no solution.
            if len(mdp.available_actions) > 0:
                break

        return mdp

    def _generate_random_state(self):

        if self.puzzle_size <= self.state_enumeration_limit:
            return random.choice(self.all_states)
        else:
            return self._generate_pseudo_random_state()

    def _generate_pseudo_random_state(self):

        generated_state = set()
        shuffled_pieces = random.sample(self.piece_terms, len(self.piece_terms))
        positions = list((i,j) for i in range(self.puzzle_size) for j in range(self.puzzle_size))
        shuffled_positions = iter(random.sample(positions, self.puzzle_size**2))

        for piece in shuffled_pieces:
            position = next(shuffled_positions)
            generated_state.add('on({},{},{})'.format(piece, position[0], position[1]))

        return generated_state

    def _generate_all_states(self):

        ctl = clingo.Control()

        ctl.load(self.file_path)
        ctl.add('base', [], 'size({}).'.format(self.puzzle_size))
        ctl.add('base', [], ' '.join(f'piece({p}).' for p in self.piece_terms))
        ctl.add('base', [], '#show state/1.')
        ctl.configuration.solve.models = 0

        ctl.ground(parts=[('base', [])])
        models = ctl.solve(yield_=True)

        generated_states = [frozenset(str(symbol.arguments[0])
                                        for symbol in model.symbols(shown=True))
                                for model in models]

        return generated_states
