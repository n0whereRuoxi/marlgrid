class Action:
    def __init__(self, head, arg_types, goal, precond):
        self.head = head
        self.arg_types = arg_types
        self.goal = goal
        self.precond = precond