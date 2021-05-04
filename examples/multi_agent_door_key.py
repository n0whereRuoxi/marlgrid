from marlgrid.utils.video import GridRecorder
import gym_minigrid
import marlgrid.envs
import gym

# env = gym_minigrid.envs.empty.EmptyEnv(size=10)
env = gym.make('MarlGrid-2AgentDoorKey9x9-v0')
# env = gym.make('MarlGrid-3AgentCluttered11x11-v0')

env.max_steps = 200
obs = env.reset()
env.recording = True

count = 0
done = False

while not done:
    env.render()
    act = env.action_space.sample()
    obs, rew, done, _ = env.step(act)
    count += 1
