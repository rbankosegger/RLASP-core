from MonteCarlo import *


def test_policy(control, blocks_world, max_episode_length, verbose=False):
    """Test whether the goal state can be reached from each starting state for a given policy.
    For each state, a check will be printed if the goal state was reachable from that state, a cross otherwise.
    Note that this test is tailored for a blocks world of size 4, if other blocks worlds should be tested,
    the final_state and final_action fields have to be updated accordingly.

    :param policy: the policy to be evaluated
    :param blocks_world: a blocks world
    :param max_episode_length: the maximum number of steps before the test for that particular start state gets aborted
    :param verbose: if true, show additional debug information
    """
    expected_final_state = blocks_world.goal_state

    final_action = Action('move(d,c)')
    num_steps = []
    mc = MonteCarlo(blocks_world, max_episode_length, 0, False, 0, False, True, control=control)

    for start_state in blocks_world.generate_all_states():
        steps, final_state = mc.generate_episode(start_state)

        if final_state == expected_final_state:
            print(f'{str(start_state):<80} {"✅":>1}')
        else:
            print(f'{str(start_state):<80} {"❌":>1}')

        num_steps.append(len(steps))

        if verbose:
            print()

            for state, reward, action in steps:
                print('\t', state)
                print('\t', f'-> {action} -> {reward} ->')


            print('\t', final_state)
            print('\t', '?=')
            print('\t', expected_final_state)
            print('+++')
            print()

    print('Average steps: ' + str(sum(num_steps) / len(num_steps)))
