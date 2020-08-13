from ClingoBridge import *
import random
from entities import *
import numpy as np
import pickle

class BlocksWorld:
    def __init__(self, number_of_blocks:int = 4, state_enumeration_limit:int = 9):
        """Initialize a blocks world, load pickle with blocks world states from path optionally.

        :param number_of_blocks: The blocks world size
        :param state_enumeration_limit: Blocks worlds bigger than this don't try to enumerate all possible states

        """

        self.number_of_blocks = number_of_blocks
        self.state_enumeration_limit = state_enumeration_limit

        self.block_terms: list = [f'b{i}' for i in range(number_of_blocks)]
        self.blocks_dl: str = ''.join(f'block({t}).' for t in self.block_terms)
        self.subgoals_dl: str = ''.join(f'subgoal({x}, {y}).' for (x, y) in zip(self.block_terms, 
                                                                                 ['table'] + self.block_terms))

        goal_part_states = set(PartState(f'on({x},{y})') for (x, y) in zip(self.block_terms, 
                                                                           ['table'] + self.block_terms))
        self.goal_state = State(goal_part_states)

    def get_random_start_state(self) -> State:
        """Returns a random start state given all possible states.

        :return: a random state
        """
        if self.number_of_blocks <= self.state_enumeration_limit:
            return random.choice(self.generate_all_states())
        else:
            return self.generate_random_start_state()

    def generate_all_states(self):
        """Enumerate all states of the blocks world.

        :return: an ndarray of all states of the environment
        """
        self.clingo = ClingoBridge()  # reset clingo
        self.clingo.add_file('initial-states.lp')
        self.clingo.run([('base', self.blocks_dl)])
        output = self.clingo.output

        num_states = int(len(output) / 2)

        states = np.full(num_states, object)
        for i in range(0, num_states):
            state_atoms = []
            for atom in output[i]:
                if atom.name == 'state':
                    state_atoms.append(atom)
            states[i] = self.parse_state(state_atoms)
        return states

    def generate_random_start_state(self) -> State:
        """Generate a random start state without relying on the enumeration of all states, useful for large blocks worlds.
        Note that those random states are not as representative as the ones generated using enumeration.

        :return: a random state
        """
        part_states = []
        blocks = self.get_blocks()
        random.shuffle(blocks)
        placed = []
        t = 0

        for block in blocks:
            if 1 / (t + 1) >= random.random():
                part_states.append(PartState(f'on({block.arguments[0]},table)'))
            else:
                rand = random.randint(0, len(placed) - 1)
                part_states.append(PartState(f'on({block.arguments[0]},{placed[rand]})'))

            placed.append(block.arguments[0])
            t += 1

        return State(set(part_states))

    def get_blocks(self) -> list:
        """Returns a list of blocks in the blocks world.

        :return: a list of blocks
        """
        self.clingo = ClingoBridge()  # reset clingo

        base = ('base', '')
        self.clingo.ctl.add('base', [], self.blocks_dl)
        self.clingo.add_file('initial-states.lp')
        self.clingo.run([base], n=1)
        output = self.clingo.output[0]

        blocks = []
        for atom in output:
            if atom.name == 'block':
                blocks.append(atom)

        return blocks

    def next_step(self, state: State, action: Action, t: int):
        """Perform one step using the ASP, return new state, new available actions, best possible action,
        reward and maximum reward (for calculating the return ratio).

        :param state: the current state
        :param action: the action to be performed
        :param t: operation mode/planning horizon (see thesis)
        :return: new state, new available actions, best possible action, reward and maximum reward
        """
        self.clingo = ClingoBridge()  # reset clingo
        facts = []

        # add dynmaic rules
        facts.append(('base', ''.join([part_state.clingo_string() for part_state in state.locations])))
        facts.append(('base', f'#const t = {t}.'))
        if action:
            facts.append(('base', action.clingo_string()))
        facts.append(('base', self.subgoals_dl))


        # add static main program file
        #self.clingo.ctl.add('base', [], self.subgoals_dl)
        self.clingo.add_file('blocksworld-mdp.lp')
        self.clingo.run(facts)
        output = self.clingo.output

        available_actions = []
        part_states = []
        max_reward = None
        next_reward = None
        best_action = None

        answer_set = output[-1]  # take last, most optimal output
        for atom in answer_set:
            if atom.name == 'executable':
                available_actions.append(self.parse_action(atom))
            elif atom.name == 'state':
                part_states.append(self.parse_part_state(atom))
            elif atom.name == 'bestAction':
                best_action = self.parse_action(atom)
            elif atom.name == 'nextReward':
                next_reward = atom.arguments[0].number
            elif atom.name == 'maxReward':
                max_reward = atom.arguments[0].number
            else:
                print(f'ERROR: unexpected atom "{atom.name}"')

        return State(set(part_states)), available_actions, best_action, next_reward, max_reward

    def parse_part_state(self, atom: clingo.Symbol) -> PartState:

        """Parse a part-state.

        :param atom: a clingo atom
        :return: a part-state object representing one on/2 atom
        """

        on_predicate = atom.arguments[0]
        top_block = on_predicate.arguments[0]
        bottom_block = on_predicate.arguments[1]
        return PartState(f'on({top_block},{bottom_block})')

    def parse_action(self, atom: clingo.Symbol) -> Action:
        """Parse an action.

        :param atom: a clingo atom
        :return: an action object representing one move/2 atom
        """

        move_predicate = atom.arguments[0]
        top_block = move_predicate.arguments[0]
        bottom_block = move_predicate.arguments[1]
        return Action(f'move({top_block},{bottom_block})')

    def parse_state(self, atoms: list) -> State:
        """Parse a full state.

        :param atoms: a list of clingo atoms
        :return: a state object consisting of many part-state objects
        """
        part_states = []
        for partState in atoms:
            part_states.append(self.parse_part_state(partState))
        return State(set(part_states))

    def optimal_return_for_state(self, state):

        max_planning_horizon = 2*(len(state.locations)-1)
        (_, _, _, _, max_reward) = self.next_step(state, action=None, t = max_planning_horizon) # clingo IO

        return max_reward
