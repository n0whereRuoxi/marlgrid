import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from marlgrid.utils.video import GridRecorder
import gym_minigrid
import marlgrid.envs
import gym
import random
import time

def observe(env):
    grid, _ = env.gen_obs_grid()
    return grid

def o_get_key(obs):
    if ('yellow', 'Key') not in obs:
        move_action_list = ['left', 'right', 'forward']
        action = random.choice(move_action_list)
        return action
    idx = obs.where_is(('yellow', 'Key'))
    idx = idx[0] + idx[1] * 7
    if idx == 38:
        return 'pickup'
    if idx < 42:
        return 'forward'
    if idx < 45:
        return 'left'
    if idx > 45:
        return 'right'

def o_unlock_door(obs):
    if ('yellow', 'Door') not in obs:
        move_action_list = ['left', 'right', 'forward']
        action = random.choice(move_action_list)
        return action
    idx = obs.where_is(('yellow', 'Door'))
    idx = idx[0] + idx[1] * 7
    if idx == 38:
        return 'toggle'
    if idx < 42:
        return 'forward'
    if idx < 45:
        return 'left'
    if idx > 45:
        return 'right'

def o_hold_door(obs):
    return 'hold'

def o_open_door(obs):
    return 'toggle'

def o_approach_door(obs):
    if ('yellow', 'Door') not in obs:
        move_action_list = ['left', 'right', 'forward']
        action = random.choice(move_action_list)
        return action
    idx = obs.where_is(('yellow', 'Door'))
    idx = idx[0] + idx[1] * 7
    if idx == 38:
        return 'pickup'
    if idx < 42:
        return 'forward'
    if idx < 45:
        return 'left'
    if idx > 45:
        return 'right'

def o_cross_door(obs):
    yield 'left'
    yield 'left'
    yield 'forward'
    yield 'forward'
    yield 'forward'

def o_go_to_goal(env):
    grid = observe(env)
    while ('blue', 'goal') not in grid:
        move_action_list = [env.actions.left, env.actions.right, env.actions.forward]
        action = random.choice(move_action_list)
        yield action
        grid = observe(env)
    idx = grid.where_is(('blue', 'goal'))
    while idx < 42 and idx != 38:
        yield env.actions.forward
        grid = observe(env)
        idx = grid.where_is(('blue', 'goal'))
    if idx == 38:
        pass
    elif idx < 45:
        yield env.actions.left
        grid = observe(env)
        idx = grid.where_is(('blue', 'goal'))
        while idx != 38:
            yield env.actions.forward
            grid = observe(env)
            idx = grid.where_is(('blue', 'goal'))
    elif idx > 45:
        yield env.actions.right
        grid = observe(env)
        idx = grid.where_is((None, 'goal'))
        while idx != 38:
            yield env.actions.forward
            grid = observe(env)
            idx = grid.where_is(('blue', 'goal'))
    yield env.actions.forward

def o_go_to_goal_0(env):
    grid = observe(env)
    while ('green', 'goal') not in grid:
        move_action_list = [env.actions.left, env.actions.right, env.actions.forward]
        action = random.choice(move_action_list)
        yield action
        grid = observe(env)
    idx = grid.where_is(('green', 'goal'))
    while idx < 42 and idx != 38:
        yield env.actions.forward
        grid = observe(env)
        idx = grid.where_is(('green', 'goal'))
    if idx == 38:
        pass
    elif idx < 45:
        yield env.actions.left
        grid = observe(env)
        idx = grid.where_is(('green', 'goal'))
        while idx != 38:
            yield env.actions.forward
            grid = observe(env)
            idx = grid.where_is(('green', 'goal'))
    elif idx > 45:
        yield env.actions.right
        grid = observe(env)
        idx = grid.where_is((None, 'goal'))
        while idx != 38:
            yield env.actions.forward
            grid = observe(env)
            idx = grid.where_is(('green', 'goal'))
    yield env.actions.forward

env = gym.make('MarlGrid-2AgentDoorKey9x9-v0')

env.max_steps = 200
obs = env.reset()
env.recording = True

count = 0
done = False

o_c_d = list(o_cross_door(None))
# o_o_d = list(o_open_door(None))
while not done:
    env.render()
    obs_red, _ = env.gen_obs_grid(env.agents[0])
    obs_blue, _ = env.gen_obs_grid(env.agents[1])
    env.ground_grid_obs(obs_red, obs_blue)
    env.state.display()
    time.sleep(1)
    # act = env.action_space.sample()
    if env.state.loc['Key'] != 'Blue':
        action = o_get_key(obs_blue)
    elif env.state.status['Door'] != 'closed' and env.state.status['Door'] != 'open':
        action = o_unlock_door(obs_blue)
    elif env.state.status['Door'] != 'locked' and env.state.status['Door'] != 'open' and count < 13:
        action = o_open_door(obs_blue)
    else:
        action = 'wait'
    print(count, action)
    act1 = getattr(env.agents[0].actions, o_c_d[count - 5] if count >= 5 and count <10 else 'wait')
    act2 = getattr(env.agents[0].actions, action)
    print(count, [act1, act2])
    obs, rew, done, _ = env.step([act1, act2])
    # print(count, [act1, act2])
    env.trigger_event()
    count += 1
