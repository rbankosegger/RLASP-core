from . import OffPolicyControl

class QLearningControl(OffPolicyControl):

    def __init__(self, target_policy, behavior_policy, alpha):
        super().__init__(target_policy, behavior_policy)
        self.alpha = alpha

    def policy_update_after_step(self, current_state, current_action, next_state, next_reward,
                                 mdp):

            target = next_reward + mdp.discount_rate * (self.target_policy.value_for(next_state, self.target_policy.suggest_action_for_state(next_state)))

            delta = self.alpha * target
            self.update(current_state, current_action, delta)

    def policy_update_after_episode(self, mdp):
        # Learning happens each step. Nothing to do at the end of the episode!
        return 


class QLearningReversedUpdateControl(OffPolicyControl):

    def __init__(self, target_policy, behavior_policy, alpha):
        super().__init__(target_policy, behavior_policy)
        self.alpha = alpha
        self.replay_memory = list()

    def policy_update_after_step(self, current_state, current_action, next_state, next_reward,
                                 mdp):

        self.replay_memory.append((current_state, current_action, next_state, next_reward))

    def policy_update_after_episode(self, mdp):

        for current_state, current_action, next_state, next_reward in reversed(self.replay_memory): 

            target = next_reward + mdp.discount_rate * (self.target_policy.value_for(next_state, self.target_policy.suggest_action_for_state(next_state)))
            delta = self.alpha * target
            self.update(current_state, current_action, delta)
