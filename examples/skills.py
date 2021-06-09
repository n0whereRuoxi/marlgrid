import random
 
class Skill:

    def __init__(self, policy, initiation, overall, termination):  # TO-DO: unbounded arguments passed into the skill
        self.policy = policy
        self.conditions = self.Conditions(initiation, overall, termination)

    class Conditions:
        def __init__(self, initiation, overall, termination): 
            self.initiation = initiation # state, args -> boolean
            self.overall = overall
            self.termination = termination

# TO-DO: how to specify the conditions of the skillls
# termination of one skill is the intiation of the next
# pass a general predicate to those two skills

def get_key(obs, args):
    print('get_key')
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
skill_get_key = Skill(get_key, lambda s,a: True, lambda s,a: True, lambda state, args: state.loc[args[1]] == args[0])

def unlock_door(obs, args):
    print('unlock_door')
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
skill_unlock_door = Skill(unlock_door, lambda s,a: True, lambda s,a: True, lambda state,args: state.status[args[1]] != 'locked')

def open_door(obs, args):
    print('open_door')
    if not obs.get(3,5).grasped:
        return 'grasp'
    else:
        return 'slide'
skill_open_door = Skill(open_door, lambda s,a: True, lambda s,a: True, lambda state,args: state.status[args[1]] == 'open')

def approach_door(obs, args):
    print('approach_door')
    if ('yellow', 'Door') not in obs:
        move_action_list = ['left', 'right', 'forward']
        action = random.choice(move_action_list)
        return action
    idx = obs.where_is(('yellow', 'Door'))
    idx = idx[0] + idx[1] * 7
    if idx < 42:
        return 'forward'
    if idx < 45:
        return 'left'
    if idx > 45:
        return 'right'
def approach_door_termination(state, args):
    print('approach_door_termination',state.loc['Door'][0], state.loc['Red'][0] , state.dir['Red'] )
    return state.loc['Door'][0] == state.loc['Red'][0] - 1 and state.dir['Red'] == 2
skill_approach_door = Skill(approach_door, lambda s,a: True, lambda s,a: True, approach_door_termination)

def cross_door(obs, args):
    print('cross_door')
    if obs.get(3,5).__class__.__name__ == 'Door':
        return 'forward'
    elif obs.get(3,6).__class__.__name__ == 'Door':
        print(3,6, obs.get(3,6))
        return 'forward'
skill_cross_door = Skill(cross_door, lambda s,a: True, lambda s,a: True, lambda state,args: state.loc['Door'][0] == state.loc['Red'][0] + 1 )
