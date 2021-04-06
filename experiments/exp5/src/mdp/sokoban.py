import os
from typing import Set

from . import MarkovDecisionProcedure

class Sokoban(MarkovDecisionProcedure):

    def __init__(self, state_initial: Set[str], state_static: Set[str]):

        # No discounting for Sokoban
        discount_rate = 1.0 
        file_name = 'sokoban.lp'

        super().__init__(state_initial, state_static, discount_rate, file_name)

class SokobanBuilder:

    def __init__(self, level_name):

        # All levels are stored in ./sokoban_levels/
        path_to_level = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                 'sokoban_levels', 
                                 f'{level_name}.txt')

        self.level_txt = ''
        self.level_asp_initial = set()
        self.level_asp_static = set()
        self._level_from_textfile(path_to_level)


        sample_mdp = self.build_mdp()
        self.mdp_interface_file_path = sample_mdp.interface_file_path
        self.mdp_problem_file_path = sample_mdp.problem_file_path
        self.mdp_state_static = sample_mdp.state_static

    def _level_from_textfile(self, path_to_level):

        legend_dynamic = {
            '$' : {'box({x},{y})'},
            '*' : {'box({x},{y})'},
            '@' : {'sokoban({x},{y})'}
        }

        legend_static = {
            '#' : {'block({x},{y})'},
            '.' : {'dest({x},{y})'},
            '*' : {'dest({x},{y})'},
        }

        with open(path_to_level, 'r') as level_file:
            for y, line in enumerate(level_file, start=1):
                self.level_txt += line
                for x, char in enumerate(line, start=1):
                    self.level_asp_initial |= { s.format(x=x, y=y) for s 
                                                in legend_dynamic.get(char, set()) }
                    self.level_asp_static  |= { s.format(x=x, y=y) for s 
                                                in legend_static.get(char, set()) }

        self.level_asp_static |= { f'col({x1})' for x1 in range(1, x+1) }
        self.level_asp_static |= { f'row({y1})' for y1 in range(1, y+1) }


    def build_mdp(self):
        return Sokoban(state_initial=self.level_asp_initial, state_static=self.level_asp_static)
