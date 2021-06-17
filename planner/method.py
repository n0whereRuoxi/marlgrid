class Method:
    def __init__(self, head, goal, precond, subgoals):
        self.head = head
        self.goal = goal
        self.precond = precond
        self.subgoals = subgoals