import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from planner.action_instance import ActionInstance
from planner.chronicle import Chronicle
from examples.skills import skill_get_key, skill_unlock_door, skill_open_door, skill_approach_door, skill_cross_door, skill_close_door
from planner.STNU import STNU
import uuid
# import gym_minigrid
# register doorkey env
import marlgrid.envs
import gym
import time

chronicle = Chronicle()
stnu = STNU()
stnu.add_vertex(chronicle.init_time_id)

action1 = ActionInstance(uuid.uuid1(), uuid.uuid1(), 'Blue', skill_get_key, ('Blue', 'Key'))
action2 = ActionInstance(uuid.uuid1(), uuid.uuid1(), 'Blue', skill_unlock_door, ('Blue', 'Door'))
action3 = ActionInstance(uuid.uuid1(), uuid.uuid1(), 'Blue', skill_open_door, ('Blue', 'Door'))

env = gym.make('MarlGrid-2AgentDoorKey9x9-v0')
env.max_steps = 200
obs = env.reset()
count = 0
done = False
stnu.vert_dict[chronicle.init_time_id].trigger()
active_actions = []

def is_enabled(time_point, stnu_):
    enabled = True
    for vert in stnu_.vert_dict[time_point].frm:
        if not stnu_.vert_dict[vert].triggered:
            enabled = False
    return enabled

def get_enabled_actions(chronicle_, stnu_):
    enabled_actions = []
    for a in chronicle_.temporal_actions:
        if not stnu_.vert_dict[a.start].triggered and is_enabled(a.start, stnu_):
            # if a.skill.conditions.initiation(env.state, a.args): # a.args says which key which agent
            enabled_actions.append(a)
    return enabled_actions

# simplified dispatch algorithm, no constraint propagation (PC)
active_actions = [action1, action2, action3]
while not done:
    env.render()
    red_obs, _ = env.gen_obs_grid(env.agents[0])
    blue_obs, _ = env.gen_obs_grid(env.agents[1])
    env.ground_grid_obs(red_obs,blue_obs)
    env.state.display()
    # enabled = list(stnu.vert_dict[now].adjacent.keys())
    red_action = 'wait'
    blue_action = 'wait'
    if active_actions:
        a = active_actions[0]
        if a.skill.conditions.termination(env.state, a.args):
            active_actions.remove(a)
        else:
            if a.agent == 'Blue':
                blue_action = a.skill.policy(blue_obs, a.args)
            elif a.agent == 'Red':
                red_action = a.skill.policy(red_obs, a.args)
        time.sleep(1)
    else:
        print('no active actions, continue...')
        time.sleep(1)
    act1 = getattr(env.agents[0].actions, red_action)
    act2 = getattr(env.agents[1].actions, blue_action)
    print(count, [act1, act2])
    obs, rew, done, _ = env.step([act1, act2])
    # env.trigger_event()
    count += 1
