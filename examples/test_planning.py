import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from planner.action_instance import ActionInstance
from planner.chronicle import Chronicle
from examples.skills import skill_get_key, skill_unlock_door, skill_open_door, skill_approach_door, skill_cross_door, skill_close_door
from planner.STNU import STNU
from planner.temporal_assertion import Assertion
import uuid
import gym

env = gym.make('MarlGrid-2AgentDoorKey9x9-v0')
env.max_steps = 200
chronicle = Chronicle()
stnu = STNU()

achive_time_point = uuid.uuid1()
goal = Assertion(achive_time_point, achive_time_point, env.state.loc, 'Red', (4,6))
alternative_goal = Assertion(achive_time_point, achive_time_point, env.state.at, ('Red', 'Door'), 'front')
chronicle.temporal_assertions.append(goal)
