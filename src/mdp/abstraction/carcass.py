import os
import random
import clingo

from .. import StateHistory

class Carcass(StateHistory):

    @staticmethod
    def file_path(file_name):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'carcass_rules', file_name)

    def __init__(self, mdp, rules_filename, debug=False):

        self.mdp = mdp
        self.rules_filename = rules_filename 
        self.debug = debug

        self.available_actions=set()
        self._ground_actions=dict()
        self.state=None

        # Set the first abstract state
        self._update_abstract_state()

        super().__init__(self.state)

    @property
    def ground_state(self):
        return self.mdp.ground_state

    def _update_abstract_state(self):

        ctl = clingo.Control()
        ctl.load(self.file_path(self.rules_filename))
        ctl.add('base', [], ' '.join(f'{s}.' for s in self.mdp.state))
        ctl.add('base', [], ' '.join(f'{s}.' for s in self.mdp.state_static))

        if self.debug:
           ctl.add('base', [], '#show highlight/3. #show line/3. #show arrow/3.')

        ctl.configuration.solve.models = 0  # create all stable models and find the optimal one
        ctl.ground(parts=[('base', [])])

        solvehandle = ctl.solve(yield_=True)

        model = list(solvehandle)[0]

    
        #self.state=f'abstract{rule_id}'
        self.available_actions = set()
        self._ground_actions=dict()

        self._asp_model_symbols = list(model.symbols(shown=True))

        state_name = ''
        
        for symbol in self._asp_model_symbols:


            if symbol.name == 'choose':

                state_name=f'carcass_{symbol.arguments[0]}'
            
        
            if symbol.name == 'abstractAction':
                
                abstract_action =  str(symbol.arguments[0])
                ground_action = str(symbol.arguments[1])
        
                self.available_actions.add(abstract_action)
        
                self._ground_actions[abstract_action] = self._ground_actions.get(abstract_action, set()) | {ground_action}


        if state_name == 'carcass_gutter':
            
            # No rules are applicable. Group all available ground actions into one single "gutter" action.

            if len(self.mdp.available_actions) > 0:
                self.available_actions = {'random'}
                self._ground_actions = { 'random' : self.mdp.available_actions }

            else:
                self.available_actions = set()
                self._ground_actions = dict()

        if len(self.mdp.available_actions) == 0:
            self.available_actions = set()
            self._ground_actions = dict()


        self.state = f'{state_name}[{",".join(a for a in sorted(self.available_actions))}]'


    def ground_actions_of(self, abstract_action):

        return self._ground_actions.get(abstract_action, dict())

    def find_abstract_actions_for_ground_action(self, ground_action):

        abstract_actions = { aa for aa, gas in self._ground_actions.items() if ground_action in gas }

        return abstract_actions

    def transition(self, action):

        # Incoming action is considered abstract if there is an abstract action matching its name
        # If not, the incoming action is treated as ground

        action_is_abstract = len(self.ground_actions_of(action)) > 0

        if action_is_abstract:

            abstract_action = action
            ground_action = random.choice(list(self.ground_actions_of(abstract_action)))

        else:

            ground_action = action
            abstract_action_candidates = self.find_abstract_actions_for_ground_action(action)
            abstract_action = random.choice(list(abstract_action_candidates))

        next_ground_state, next_reward = self.mdp.transition(ground_action)

        self._update_abstract_state()

        super().transition(abstract_action, #A[t]
                           self.state, # S[t+1]
                           next_reward # R[t+1]
                          )

        return self.state, next_reward

    @property 
    def discount_rate(self):
        return self.mdp.discount_rate
