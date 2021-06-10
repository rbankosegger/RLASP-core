import random
import copy

import gym
import gym_minigrid
from gym_minigrid.wrappers import FullyObsWrapper
from gym_minigrid.minigrid import IDX_TO_COLOR, IDX_TO_OBJECT 

from .state_history import StateHistory

IDX_TO_AGENT_DIRECTION = {
    0: 'right',
    1: 'down',
    2: 'left',
    3: 'up'
}

IDX_TO_DOOR_STATE = {
    0: 'open',
    1: 'closed',
    2: 'locked'
}

def world_object_tuple_to_term(x, y, type_idx, color_idx, state_idx):

    obj_type = IDX_TO_OBJECT[type_idx]
    color = IDX_TO_COLOR[color_idx]

    if obj_type == 'empty' or obj_type == 'unseen':
        return None

    elif obj_type =='agent':
        direction = IDX_TO_AGENT_DIRECTION[state_idx]
        return f'obj(agent({direction}),{x},{y})'

    elif obj_type in { 'wall', 'floor', 'ball', 'key', 'box' }:
        return f'obj({obj_type}({color}),{x},{y})'

    elif obj_type == 'door':
        state = IDX_TO_DOOR_STATE[state_idx]
        return f'obj(door({color},{state}),{x},{y})'

    elif obj_type == 'goal':
        return f'obj(goal,{x},{y})'

    elif obj_type == 'lava':
        return f'obj(lava,{x},{y})'

    else:
        assert False, "unknown object type: '%s'" % obj_type


class GymMinigrid(StateHistory):

    def __init__(self, env):

        self.env = env

        observation = self.env.reset()
        self.state = self._observation_to_state(observation)

        self.done = False

        self.discount_rate = 1
        super().__init__(frozenset(self.state))

    def _observation_to_state(self, obs):

        img = obs['image']
        width, height, channels = img.shape

        state = { world_object_tuple_to_term(x, y, *img[x,y]) 
                    for x in range(width) for y in range(height) } - { None }

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

        self.state = self._observation_to_state(observation)
        self.done = done


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

        self.env = gym.make(self.env_label)
        self.env.seed(random.randint(0, 9999))

        if self.full_observability:
            self.env = FullyObsWrapper(self.env)

        return GymMinigrid(self.env)
