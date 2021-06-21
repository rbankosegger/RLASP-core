import random
import copy
import os

import gym
import gym_minigrid
from gym_minigrid.wrappers import FullyObsWrapper
from gym_minigrid import minigrid

from .state_history import StateHistory

IDX_TO_AGENT_DIRECTION = {
    0: 'east',
    1: 'south',
    2: 'west',
    3: 'north'
}

IDX_TO_DOOR_STATE = {
    0: 'open',
    1: 'closed',
    2: 'locked'
}

def world_object_tuple_to_term(x, y, type_idx, color_idx, state_idx):

    obj_type = minigrid.IDX_TO_OBJECT[type_idx]
    color = minigrid.IDX_TO_COLOR[color_idx]

    if obj_type == 'empty' or obj_type == 'unseen':
        return None

    elif obj_type =='agent':
        direction = IDX_TO_AGENT_DIRECTION[state_idx]
        return f'obj(agent({direction}),({x},{y}))'

    elif obj_type in { 'wall', 'floor', 'ball', 'key', 'box' }:
        return f'obj({obj_type}({color}),({x},{y}))'

    elif obj_type == 'door':
        state = IDX_TO_DOOR_STATE[state_idx]
        return f'obj(door({color},{state}),({x},{y}))'

    elif obj_type == 'goal':
        return f'obj(goal,({x},{y}))'

    elif obj_type == 'lava':
        return f'obj(lava,({x},{y}))'

    else:
        assert False, "unknown object type: '%s'" % obj_type


class GymMinigrid(StateHistory):

    def __init__(self, env):

        self.env = env

        self.done = False

        observation = self.env.reset()
        self.state = self._observation_to_state(observation)
        self.state_static = set()

        self.discount_rate = 1
        super().__init__(frozenset(self.state))

    def _observation_to_state(self, obs):

        img = obs['image']
        width, height, channels = img.shape

        state = { world_object_tuple_to_term(x, y, *img[x,y]) 
                    for x in range(width) for y in range(height) } - { None }

        if self.done:
            state.add('terminal')

        return frozenset(state)


    @property
    def available_actions(self):

        if self.done:
            return set()
        else:
            return { a.name for a in self.env.actions }

    @property
    def ground_state(self):
        return self.state

    def transition(self, action: str):

        action_as_enum = self.env.actions[action]
        observation, next_reward, done, info = self.env.step(action_as_enum)

        self.done = done
        self.state = self._observation_to_state(observation)


        super().transition(action, # A[t]
                           frozenset(self.state), # S[t+1]
                           next_reward # R[t+1]
                          )

        return self.state, next_reward




class GymMinigridBuilder:

    def __init__(self, env_label='MiniGrid-MultiRoom-N6-v0', full_observability=True):

        self.env_label = env_label
        self.full_observability = full_observability

        # So far, no planner is available for this.
        self.mdp_interface_file_path = None
        self.mdp_problem_file_path = None
        self.mdp_state_static = None

    def build_mdp(self):

        env = gym.make(self.env_label)
        env.seed(random.randint(0, 9999))

        if self.full_observability:
            env = FullyObsWrapper(env)

        return GymMinigrid(env)


class CustomMinigridEnvironment(minigrid.MiniGridEnv):

    ASCII_TO_COLOR = { 

        'r': 'red',
        'g': 'green',
        'b': 'blue',
        'p': 'purple',
        'y': 'yellow',
        'k': 'grey'
    }

    ASCII_TO_OBJECTS = {

        ** { f'{c}W' : (minigrid.Wall,  dict(color=color)) for c, color in ASCII_TO_COLOR.items() },
        ** { f'{c}F' : (minigrid.Floor, dict(color=color)) for c, color in ASCII_TO_COLOR.items() },
        ** { f'{c}K' : (minigrid.Key,   dict(color=color)) for c, color in ASCII_TO_COLOR.items() },
        ** { f'{c}A' : (minigrid.Ball,  dict(color=color)) for c, color in ASCII_TO_COLOR.items() },
        ** { f'{c}B' : (minigrid.Box,   dict(color=color)) for c, color in ASCII_TO_COLOR.items() },

        ** { f'{c}Do' : (minigrid.Door, dict(color=color, is_open=True, is_locked=False)) for c, color in ASCII_TO_COLOR.items() },
        ** { f'{c}Dc' : (minigrid.Door, dict(color=color, is_open=False, is_locked=False)) for c, color in ASCII_TO_COLOR.items() },
        ** { f'{c}Dl' : (minigrid.Door, dict(color=color, is_open=False, is_locked=True)) for c, color in ASCII_TO_COLOR.items() },

        'G' : (minigrid.Goal, dict()),
        '~' : (minigrid.Lava, dict()),
    }

    ASCII_TO_DIRECTIONS = {

       '>': 0,
       'v': 1,
       '<': 2,
       '^': 3
    }

    def __init__(self, width, height, ascii_symbols):

        self.ascii_symbols = ascii_symbols

        super().__init__(
            width=width,
            height=height,
            see_through_walls=False)

    def _gen_grid(self, width, height):

        self.grid = minigrid.Grid(width, height)

        for x, y, symbol in self.ascii_symbols:
            self._build_from_symbol(x, y, symbol)

        if not self.agent_pos:
            self.place_agent()

        self.mission = ''

    def _build_from_symbol(self, x, y, symbol):

        if symbol in '>v<^':
            self.agent_pos = (x,y)
            self.agent_dir = CustomMinigridEnvironment.ASCII_TO_DIRECTIONS[symbol]

        elif symbol == '_':
            # Empty space, nothing to add
            pass

        else:
            cls,args = CustomMinigridEnvironment.ASCII_TO_OBJECTS[symbol]
            self.put_obj(cls(**args), x, y)


class GymMinigridCustomLevelBuilder:

    def __init__(self, level_name=None, ascii_encoding=None, full_observability=True):

        # Environments can build from level files or directly from strings.
        # But not both!
        assert(not level_name or not ascii_encoding)

        self.full_observability = full_observability

        self.env_ascii_symbols = []
        self.env_width = 3
        self.env_height = 3
        self.level_txt = ''

        if level_name:

            # All levels are stored in ./minigrid_levels/
            path_to_level = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                     'minigrid_levels', 
                                     f'{level_name}.txt')

            self._level_from_textfile(path_to_level)

        if ascii_encoding:

            self._level_from_string(ascii_encoding)



        # So far, no planner is available for this.
        self.mdp_interface_file_path = None
        self.mdp_problem_file_path = None
        self.mdp_state_static = None


    def _level_from_textfile(self, path_to_level):


        with open(path_to_level, 'r') as level_file:
            for y, line in enumerate(level_file, start=0):
                self.level_txt += line

                symbols = [ k for k in line.replace('\n','').split(' ') if k != '' ]

                for x, symbol in enumerate(symbols, start=0):

                    self.env_ascii_symbols.append((x, y, symbol))

                if x + 1 > self.env_width:
                    self.env_width = x + 1

            if y + 1 > self.env_height:
                self.env_height = y + 1

    def _level_from_string(self, level_string):

        lines = [ s for s in level_string.replace('\t', '').split('\n') if s != '' ]

        for y, line in enumerate(lines, start=0):

            self.level_txt += line

            symbols = [ k for k in line.split(' ') if k != '' ]

            for x, symbol in enumerate(symbols, start=0):

                self.env_ascii_symbols.append((x, y, symbol))

            if x + 1 > self.env_width:
                self.env_width = x + 1

        if y + 1 > self.env_height:
            self.env_height = y + 1


    def build_mdp(self):

        env = CustomMinigridEnvironment(self.env_width, self.env_height, self.env_ascii_symbols)

        if self.full_observability:
            env = FullyObsWrapper(env)

        return GymMinigrid(env)
