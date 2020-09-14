from collections import defaultdict

from . import OffPolicyControl

class FirstVisitMonteCarloControl(OffPolicyControl):

    def __init__(self, target_policy):

        # This method is on-policy -> Target policy = Behavior policy
        super().__init__(target_policy=target_policy,
                         behavior_policy=target_policy)

        self.visits = defaultdict(int)

    def update(self, state, action, delta):
        # Make sure behavior policy is NOT updated here!
        # The update would be doubled since behavior_policy = target_policy.
        self.target_policy.update(state, action, delta)

    def policy_update_after_episode(self, mdp):

        visits_this_episode = set()

        for state, action, return_ in zip(mdp.state_history,
                                          mdp.action_history,
                                          mdp.return_history):

            is_first_visit = (state, action) not in visits_this_episode
            if is_first_visit:

                self.visits[state, action] += 1
                q = self.target_policy.value_for(state, action)
                v = float(self.visits[state, action])

                delta = (return_ - q) / v 

                self.update(state, action, delta)

                visits_this_episode.add((state, action))


class MonteCarloSGDControl(OffPolicyControl):

    def __init__(self, target_policy, alpha):

        # This method is on-policy -> Target policy = Behavior policy
        super().__init__(target_policy=target_policy, 
                         behavior_policy=target_policy)

        self.alpha = alpha

    def update(self, state, action, delta):
        # Make sure behavior policy is NOT updated here!
        # The update would be doubled since behavior_policy = target_policy.
        self.target_policy.update(state, action, delta)

    def policy_update_after_episode(self, mdp):

        for state, action, return_ in zip(mdp.state_history,
                                          mdp.action_history,
                                          mdp.return_history):

            q = self.target_policy.value_for(state, action)
            delta = self.alpha * (return_ - q)
            self.update(state, action, delta)

