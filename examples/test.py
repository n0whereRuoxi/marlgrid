import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from planner.action_instance import ActionInstance
from planner.chronicle import Chronicle
from examples.skills import skill_get_key, skill_unlock_door
from planner.STNU import STNU
import uuid
from marlgrid.utils.video import GridRecorder
import gym_minigrid
import marlgrid.envs
import gym
import random
import time

chronicle = Chronicle()
stnu = STNU()
stnu.add_vertex(chronicle.init_time_id)

action = ActionInstance(uuid.uuid1(), uuid.uuid1(), 'blue', skill_get_key, None)
stnu.add_vertex(action.start)
stnu.add_vertex(action.end)
stnu.add_edge(chronicle.init_time_id, action.start, (0, None)) # the start time of action 1 is greater or equal to the initial time
stnu.add_edge(action.start, action.end, (1, None))

action2 = ActionInstance(uuid.uuid1(), uuid.uuid1(), 'blue', skill_unlock_door, None)
stnu.add_vertex(action2.start)
stnu.add_vertex(action2.end)
stnu.add_edge(action.end, action2.start, (0, None))
stnu.add_edge(action2.start, action2.end, (1, None))

env = gym.make('MarlGrid-2AgentDoorKey9x9-v0')
env.max_steps = 200
obs = env.reset()
count = 0
done = False
now = chronicle.init_time_id

while not done:
    env.render()
    red_obs, _ = env.gen_obs_grid(env.agents[0])
    blue_obs, _ = env.gen_obs_grid(env.agents[1])
    print(obs)
    env.ground_grid_obs(blue_obs)
    env.state.display()
    time.sleep(1)

    enabled = stnu.vert_dict[now].adjacent.keys()[0]
    active_actions = []
    for a in chronicle.temporal_actions:
        if a.start == enabled.id:
            if a.agent == 'blue' and a.skill.init(env.state):
                active_actions.append(a)
    for a in active_actions:
        if a.skill.termination(env.state):
            active_actions.remove(a) # check logic
    blue_action = a.skill.policy(blue_obs)

    act1 = getattr('wait')
    act2 = getattr(env.agents[1].actions, blue_action)
    print(count, [act1, act2])
    obs, rew, done, _ = env.step([act1, act2])
    # print(count, [act1, act2])
    env.trigger_event()
    count += 1
