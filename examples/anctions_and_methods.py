from planner.method import Method
from planner.action import Action
from typing import NewType

AGENT = ['Blue', 'Red']
DOOR = ['Yellow Door', 'Green Door']
KEY = ['Yellow Key', 'Green Key']
LOC = []

class ArgIdx:
    def __init__(self, index):
        self.idx = index

# a goal is specified as conjunction and disjunction of statements
# A statement is state_variable_name(args) = value
# In the python code, a statement is formated as 3-tuple `(state_variable_name, arg, value)`
# GTPyhop only decide relevant methods by its state_variable_name
# Here we match all three arguments
# TO-DO: Disadvantage of statements v.s. predicates: how to represent the negation of the statement? need exhaustion
# TO-DO: Do we need to represent disjunctions?
# TO-DO: How to specify same_color(d,k) = 'true' in precondition
# TO-DO: How to tell the agent to get yellow key using the the same skill that can get any keys? we pass arguments along with the percetion as input into the policy

# action: get_key(a: AGENT,k: KEY)
# goal: loc(k) = a
# precond: None
action1 = Action(head = 'get_key', arg_types = (AGENT, KEY), goal = ['loc', ArgIdx(1), ArgIdx(0)], precond = [])

# action: unlock_door(a: AGENT,d: DOOR,k: KEY)
# goal: status(d) = 'unlocked'
# precond: loc(k) = a (and same_color(d,k) = 'true')
action2 = Action(head = 'unlock_door', arg_types = (AGENT, DOOR, KEY), goal = ['status', ArgIdx(1), 'unlocked'], precond = [['loc', ArgIdx(2), ArgIdx(0)]])

# action: open_door(a: AGENT,d: DOOR)
# goal: status(d) = 'open'
# precond: status(d) = 'unlocked' and at(a,d) = 'front'
action3 = Action(head = 'open_door', arg_types = (AGENT, DOOR), goal = ['status', ArgIdx(1), 'open'], precond = [['status', ArgIdx(1), 'unlocked'],['at', (ArgIdx(0), ArgIdx(1)), 'front']])

# method: open_locked_door(a: AGENT,d: DOOR,k: KEY)
# goal: status(d) = 'open'
# precond: None
# subgoals: loc(k) = a, status(d) = 'unlocked', then status(d) = 'open'
method1 = Method(head = 'open_locked_door', arg_types = (AGENT, DOOR, KEY), goal = ['status', ArgIdx(1), 'open'], precond = [], subgoals = (['loc', ArgIdx(2), ArgIdx(0)], ['status', ArgIdx(1), 'unlocked'], ['status', ArgIdx(1), 'open']))
