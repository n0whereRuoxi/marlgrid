class ActionInstance:
    def __init__(self, start, end, agent, skill, args):
        self.agent = agent
        self.start = start
        self.end = end
        self.skill = skill
        self.args = args