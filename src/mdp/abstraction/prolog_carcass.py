import os
import random
import clingo

from .. import StateHistory
from collections import namedtuple
from . import PrologInterface

class PrologCarcass(StateHistory):

    @staticmethod
    def file_path(file_name):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prolog_carcass_rules', file_name)

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


        prolog = PrologInterface()
        facts = [f'{s}' for s in self.mdp.state] + [f'{s}' for s in self.mdp.state_static]
        query_results = prolog.run_query(consult_file=self.file_path(self.rules_filename), 
                                            knowledge_base=facts,
                                            queries=['choose(S)', 'choose(S), abstractAction(AAbs,ACon)'])

        state_name=f'carcass_{query_results[0][0]['S']}'

        self.available_actions = set()
        self._ground_actions=dict()
        for computed_answer in query_results[1]:
                
            abstract_action = computed_answer['AAbs'].replace(' ','')
            ground_action = computed_answer['ACon'].replace(' ','')
        
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
