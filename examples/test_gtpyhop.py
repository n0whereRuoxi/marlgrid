import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import planner.gtpyhop as gtpyhop
import random
from examples.skills import skill_approach_door, skill_get_key, skill_unlock_door, skill_open_door, skill_approach_door, skill_cross_door, skill_close_door

# This avoids hard-coding the domain name, making the code more portable
domain_name = __name__
the_domain = gtpyhop.Domain(domain_name)

################################################################################
# rigid relations, states, goals

rigid = gtpyhop.State('rigid relations')
rigid.types = {
    'agent': ['blue', 'red'],
    'door': ['yellow_door', 'blue_door'],
    'key': ['yellow_key', 'green_key'],
    'loc': []
}

# prototypical initial state
state0 = gtpyhop.State('state0')
state0.loc = {'blue': (2, 6), 'red': (6, 6), 'goal': None, 'key': None, 'door': (5, 6)}
state0.orientation = {'blue': None, 'red': None}
state0.status = {'door': 'locked'}
state0.dir = {'blue': 0, 'red': 0}
state0.room = {'blue': None}

# helper functions
def has_right_key(state, a, d): # TO-DO
    return True
def at_door(agent_loc, agent_dir,door_loc): # TO-DO
    return True
def reachable(state,a,k): # TO-DO
    return True
def same_color(d,k): # TO-DO
    return True

# action1 = Action(head = 'get_key', arg_types = (AGENT, KEY), goal = ['loc', ArgIdx(1), ArgIdx(0)], precond = [])
def get_key(state,a,k):
    # no preconditoin
    if a in rigid.types['agent']: # checks argument type
        return skill_get_key
gtpyhop.declare_methods('loc',get_key)

#action2 = Action(head = 'unlock_door', arg_types = (AGENT, DOOR, KEY), goal = ['status', ArgIdx(1), 'unlocked'], precond = [['loc', ArgIdx(2), ArgIdx(0)]])
def unlock_door(state,a,d):
    if has_right_key(state,a,d):
        return skill_unlock_door
gtpyhop.declare_methods('status',unlock_door)

# action: open_door(a: AGENT,d: DOOR)
# goal: status(d) = 'open'
# precond: status(d) = 'unlocked' and at(a,d) = 'front'
# action3 = Action(head = 'open_door', arg_types = (AGENT, DOOR), goal = ['status', ArgIdx(1), 'open'], precond = [['status', ArgIdx(1), 'unlocked'],['at', (ArgIdx(0), ArgIdx(1)), 'front']])
def open_door(state,a,d):
    if at_door(state.loc[a], state.dir[a], state.loc[d]) and state.status[d] == 'unlocked':
        return skill_open_door
gtpyhop.declare_methods('status',open_door)

# method1 = Method(head = 'open_locked_door', arg_types = (AGENT, DOOR, KEY), goal = ['status', ArgIdx(1), 'open'], precond = [], subgoals = (['loc', ArgIdx(2), ArgIdx(0)], ['status', ArgIdx(1), 'unlocked'], ['status', ArgIdx(1), 'locked']))
def open_locked_door(state, a,d,k):
    if state.status[d] == 'locked': # checks precondition
        return [('loc', a, k), ('status', a, d), ('status', a, d)]
        # return [('loc', k, a), ('status', d, 'unlocked'), ('status', d, 'open')]
gtpyhop.declare_methods('status',open_locked_door)

def cross_locked_door(state, a1, a2, d, k):
    if reachable(a2,k) and same_color(d,k) and state.status[d] == 'locked':
        return [('status', a2, d, k), ('loc', a1, d), ('loc', a1, d)]
        # return [('status', d, 'open'), ('loc', a1, back(d)), ('loc', a1, front(d))]
gtpyhop.declare_methods('loc',cross_locked_door)

def move_to(state, a, l):
    return (skill_move_to, a, l)
gtpyhop.declare_methods('loc',cross_locked_door)

print("- If verbose=0, GTPyhop returns the solution but prints nothing.\n")
gtpyhop.verbose = 0
gtpyhop.pyhop(state0,[('loc','red','blue','yellow_door', 'yellow_key')])
