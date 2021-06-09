import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from planner.action_instance import ActionInstance
from planner.chronicle import Chronicle
from examples.skills import skill_get_key, skill_unlock_door, skill_open_door, skill_approach_door, skill_cross_door
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

action = ActionInstance(uuid.uuid1(), uuid.uuid1(), 'Blue', skill_get_key, ('Blue', 'Key'))
stnu.add_vertex(action.start)
stnu.add_vertex(action.end)
stnu.add_edge(chronicle.init_time_id, action.start, (0, None)) # the start time of action 1 is greater or equal to the initial time
stnu.add_edge(action.start, action.end, (1, None))
chronicle.temporal_actions.append(action)

action2 = ActionInstance(uuid.uuid1(), uuid.uuid1(), 'Blue', skill_unlock_door, ('Blue', 'Door'))
stnu.add_vertex(action2.start)
stnu.add_vertex(action2.end)
stnu.add_edge(action.end, action2.start, (0, None))
stnu.add_edge(action2.start, action2.end, (1, None))
chronicle.temporal_actions.append(action2)

action3 = ActionInstance(uuid.uuid1(), uuid.uuid1(), 'Blue', skill_open_door, ('Blue', 'Door'))
stnu.add_vertex(action3.start)
stnu.add_vertex(action3.end)
stnu.add_edge(action2.end, action3.start, (0, None))
stnu.add_edge(action3.start, action3.end, (1, None))
chronicle.temporal_actions.append(action3)

action4 = ActionInstance(uuid.uuid1(), uuid.uuid1(), 'Red', skill_approach_door, ('Red', 'Door'))
stnu.add_vertex(action4.start)
stnu.add_vertex(action4.end)
stnu.add_edge(action3.end, action4.start, (0, None))
stnu.add_edge(action4.start, action4.end, (1, None))
chronicle.temporal_actions.append(action4)

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
    env.ground_grid_obs(red_obs,blue_obs)


    env.state.display()

    enabled = list(stnu.vert_dict[now].adjacent.keys())[0]
    print(enabled.id)
    active_actions = []
    red_action = 'wait'
    blue_action = 'wait'
    # print('temporal_actions', chronicle.temporal_actions)
    for a in chronicle.temporal_actions:
        # print(a.start)
        if a.start == enabled.id:
            if a.skill.conditions.initiation(env.state, a.args): # a.args says which key which agent
                active_actions.append(a)
    for a in active_actions:
        if a.skill.conditions.termination(env.state, a.args):
            active_actions.remove(a) # check logic
            now = a.end
        else:
            if a.agent == 'Blue':
                blue_action = a.skill.policy(blue_obs, a.args)
            elif a.agent == 'Red':
                red_action = a.skill.policy(red_obs, a.args)
    if not active_actions:
        print('no active actions, continue...')
        time.sleep(0.2)
        continue
    else:
        time.sleep(1)
    act1 = getattr(env.agents[0].actions, red_action)
    act2 = getattr(env.agents[1].actions, blue_action)
    print(count, [act1, act2])
    obs, rew, done, _ = env.step([act1, act2])
    # print(count, [act1, act2])
    env.trigger_event()
    count += 1
