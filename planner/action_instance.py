class ActionInstance:
    def __init__(self, start, end, agent, skill, args):
        self.agent = agent
        self.start = start
        self.end = end
        self.skill = skill
        self.args = args
        self.assertion = [] # is it necessary?

# initial chronicle: goal -> 
# chronicle: actions <-> goal skills

# acting agent: actions <-> goal skills, methods, initial state, goals

# align: assertions <-> conditions
# general translation alg

# methods -> actions -> learn skills according to the action definition
# a simulation of the skill to see if the assersions in the action actually happends