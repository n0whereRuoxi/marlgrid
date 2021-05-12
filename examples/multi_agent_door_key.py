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
        monitor_get_key = True
        return 'pickup'
    if idx < 42:
        return 'forward'
    if idx < 45:
        return 'left'
    if idx > 45:
        return 'right'

def o_open_door(obs):
    if ('yellow', 'Door') not in obs:
        move_action_list = ['left', 'right', 'forward']
        action = random.choice(move_action_list)
        return action
    idx = obs.where_is(('yellow', 'Door'))
    idx = idx[0] + idx[1] * 7
    if idx == 38:
        monitor_get_key = True
        return 'toggle'
    if idx < 42:
        return 'forward'
    if idx < 45:
        return 'left'
    if idx > 45:
        return 'right'

def o_hold_door(obs):
    return 'hold'

def o_cross_door(env):
    yield env.actions.forward
    yield env.actions.forward

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

env = gym.make('MarlGrid-1AgentDoorKey9x9-v0')

env.max_steps = 200
obs = env.reset()
env.recording = True

count = 0
done = False

while not done:
    env.render()
    obs, _ = env.gen_obs_grid(env.agents[0])
    print(obs)
    env.ground_grid_obs(obs)
    env.state.display()
    time.sleep(1)
    # act = env.action_space.sample()
    if env.state.loc['Key'] != 'Agent':
        action = o_get_key(obs)
    elif env.state.status['Door'] != 'closed' and env.state.status['Door'] != 'held':
        action = o_open_door(obs)
    elif count < 30:
        action = o_hold_door(obs)
    else:
        action = 'wait'
    act = getattr(env.agents[0].actions, action)
    obs, rew, done, _ = env.step([act])
    print(count, [act])
    env.trigger_event()
    count += 1
