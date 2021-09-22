from examples.skills import skill_get_key, skill_unlock_door, skill_open_door, skill_approach_door

# given a task hierarchy

class HGNNode:

    def __init__(self, label, parameters, goal):
        self.label = label
        self.parameters = parameters
        self.goal = goal
        self.children = []
        self.skill = None

    def add_child(self, HGN_node):
        self.children.append(HGN_node)

    def add_skill(self, skill):
        self.skill = skill

AGENT = ['Blue']
DOOR = ['Yellow Door']
KEY = ['Yellow Key']
LOC = []

class ArgIdx:
    def __init__(self, index):
        self.index = index

skill_open_door = Skill(open_door, lambda state, args: state.status[args[1]] != 'locked', lambda s,a: True, lambda state,args: state.status[args[1]] == 'open')
skill_unlock_door = Skill(unlock_door, 
    lambda state, args: state.loc[args[2]] == args[0], # args[0] -> agent 
    lambda s,a: True, 
    lambda state,args: state.status[args[1]] != 'locked'
)
skill_get_key = Skill(get_key, lambda s,a: True, lambda s,a: True, lambda state, args: state.loc[args[1]] == args[0])

HGN_node_open_door = HGNNode(label = 'open_door', parameters = (AGENT, DOOR), goal = ('status', ArgIdx(1), 'open'))
HGN_node_unlock_door = HGNNode(label = 'unlock_door', parameters = (AGENT, DOOR), goal = ('status', ArgIdx(1), 'closed'))
HGN_node_get_key = HGNNode(label = 'get_key', parameters = (AGENT, DOOR, KEY), goal = ('loc', ArgIdx(2), ArgIdx(0)))

