import random
 
class Skill:
    def __init__(self, policy, initiation, overall, termination):
        self.policy = policy
        self.initiation = initiation
        self.overall = overall
        self.termination = termination

def get_key(obs):
    if ('yellow', 'Key') not in obs:
        move_action_list = ['left', 'right', 'forward']
        action = random.choice(move_action_list)
        return action
    idx = obs.where_is(('yellow', 'Key'))
    idx = idx[0] + idx[1] * 7
    if idx == 38:
        return 'pickup'
    if idx < 42:
        return 'forward'
    if idx < 45:
        return 'left'
    if idx > 45:
        return 'right'
skill_get_key = Skill(get_key, lambda s: True, lambda s: True, lambda state: state.loc['Key'] == 'Agent')

def unlock_door(obs):
    if ('yellow', 'Door') not in obs:
        move_action_list = ['left', 'right', 'forward']
        action = random.choice(move_action_list)
        return action
    idx = obs.where_is(('yellow', 'Door'))
    idx = idx[0] + idx[1] * 7
    if idx == 38:
        return 'toggle'
    if idx < 42:
        return 'forward'
    if idx < 45:
        return 'left'
    if idx > 45:
        return 'right'
skill_unlock_door = Skill(unlock_door, lambda s: True, lambda s: True, lambda state: state.status['Door'] != 'locked')