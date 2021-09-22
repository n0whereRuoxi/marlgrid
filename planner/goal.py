class Multigoal():
    """
    g = Multigoal(goal_name,**kwargs) creates a Multigoal object that is a 
    container for state-variable bindings. It represents a conjunctive goal, 
    i.e., the goal of achieving every state-variable binding in g.
      - The optional argument 'goal_name' is the name to use for the goal.
        If you omit it, a name of the form _goal# will be assigned, where #
        is an integer.
      - The keyword args are name and initial values of state variables.
        A state variable's initial value is usually {}, but it can also
        be a dictionary of arguments and their initial values.
    Example: here are three equivalent ways to specify a goal named 'goal1'
    in which boxes b and c are located in room2 and room3:
        First:
           g = Multigoal('goal1')
           g.loc = {}   # create a dictionary for things like loc['b']
           g.loc['b'] = 'room2'
           g.loc['c'] = 'room3'
        Second:
           g = Multigoal('goal1', loc={})
           g.loc['b'] = 'room2'
           g.loc['c'] = 'room3'
        Third:
           g = Multigoal('goal1',loc={'b':'room2', 'c':'room3'})
    """
    def __init__(self,name=None):
        """
        If 'name' is given, then use it as the goal's name. Otherwise,
        give it a name of the form '_multigoal#' where # is an integer.
        """
        global _next_multigoal_number
        if name:
            self.__name__ = name
        else:
            self.__name__ = f'_multigoal{_next_multigoal_number}'
            _next_multigoal_number += 1
            
    def __str__(self):
        return f"<Multigoal {self.__name__}>"
        
    def __repr__(self):
        """Return a string that can be used to reconstruct the state"""
        x = f"Multigoal('{self.__name__}', "
        x += ', '.join([f'{v}={vars(self)[v]}' for v in vars(self) if v != '__name__'])
        x += ')'
        return x

    def copy(self,name=None):
        """
        Make a copy of the goal. If name is given, then give the copy that name.
        Otherwise give it a name of the form '_multigoal#' where # is an integer.
        """
        global _next_multigoal_number
        multigoal = copy.deepcopy(self)
        if name:
            multigoal.__name__ = name
        else:
            multigoal.__name__ = f'_multigoal{_next_multigoal_number}'
            _next_multigoal_number += 1
        return multigoal

    def display(self,heading=None):
        """
        Print the multigoal's state-variables and their values. The arguments are:
         - heading (optional) is a heading to print beforehand.
        """
        _print_state(self,heading=heading)


def _print_state(state,heading=None):
    """
    Print the state-variables and values in 'state', which may be
    either a state object or a goal object. The optional arguments are:
    - heading, a heading to print beforehand.
    """
    if heading == None: heading = get_type(state)
    if state != False:
        title = f"{heading} {state.__name__}:"
        dashes = '-'*len(title)
        print(title)
        print(dashes)
        for (varname,val) in vars(state).items():
            if varname != '__name__':
                print(f"  - {varname} = {val}")
        print('')
    else: 
        if heading == None: heading = 'state'
        print('{heading} = False','\n')