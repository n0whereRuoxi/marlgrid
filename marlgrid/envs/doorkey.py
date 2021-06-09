from ..base import MultiGridEnv, MultiGrid
from ..objects import *

class DoorKeyEnv(MultiGridEnv):
    """
    Environment with a door and key, sparse reward.
    Similar to DoorKeyEnv in 
        https://github.com/maximecb/gym-minigrid/blob/master/gym_minigrid/envs/doorkey.py
    """

    mission = "use the key to open the door and then get to the goal"
    metadata = {}

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = MultiGrid((width, height))
        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)
        # Place a goal in the bottom-right corner
        # self.put_obj(Goal(color="green", reward=1), width - 2, height - 2)
        self.put_obj(Goal(color="green", reward=1), 1, 1)
        # Create a vertical splitting wall
        splitIdx = self._rand_int(2, width - 2)
        self.grid.vert_wall(splitIdx, 0)
        # Place the agent at a random position and orientation
        # on the left side of the splitting wall
        # self.place_agent(size=(splitIdx, height))
        # Place a door in the wall
        doorIdx = self._rand_int(1, width - 2)
        self.put_obj(Door(color="yellow", state=Door.states.locked), splitIdx, doorIdx)
        # Place a yellow key on the left side
        self.place_obj(obj=Key("yellow"), top=(0, 0), size=(splitIdx, height))
        self.agent_spawn_kwargs = {}
        self.place_agents(**self.agent_spawn_kwargs)
        # initialize symbolic state
        self.state.loc = {'Blue': None, 'Red': None, 'Goal': None, 'Key': None, 'Door': None}
        self.state.orientation = {'Blue': None, 'Red': None}
        self.state.status = {'Door': None}
        self.state.dir = {'Blue': None, 'Red': None}
        self.state.room = {'Blue': None}
        # TO-DO: engineering the predicates/ representation learning
        # TO-DO: do we need predicates? at(red, door, back)
    def ground_grid_obs(self, red_obs, blue_obs):
        # if ('yellow', 'Key') in grid: 
        #     coordinate= grid.relative_coordinate_of(('yellow', 'Key'))
        #     if coordinate:
        #         absolute_coordinate = self.get_absolute_coordinate(coordinate, self.agents[0].pos, self.agents[0].dir)
        #         self.state.loc['Key'] = absolute_coordinate\

        # ground obs for red agent
        self.state.loc['Red'] = (self.agents[0].pos[0], self.agents[0].pos[1])
        self.state.dir['Red'] = self.agents[0].dir
        # ground obs for blue agent
        if self.agents[1].carrying and self.agents[1].carrying.type == 'Key':
            self.state.loc['Key'] = 'Blue'
        for i in range(len(blue_obs.grid)):
            for j in range(len(blue_obs.grid[i])):
                e = blue_obs.obj_reg.key_to_obj_map[blue_obs.grid[i, j]]
                if e and e.type == 'Door':
                    self.state.status['Door'] = 'open' if e.state == e.states.open else 'closed' if e.state == e.states.closed else 'locked'
                    absolute_coordinate = self.get_absolute_coordinate((j, i), self.agents[1].pos, self.agents[1].dir)
                    self.state.loc['Door'] = absolute_coordinate
        self.state.loc['Blue'] = (self.agents[1].pos[0], self.agents[1].pos[1])
        self.state.dir['Blue'] = self.agents[1].dir

    def get_absolute_coordinate(self, relative_coordinate, pos, dir):
        (x, y) = relative_coordinate
        (a, b) = pos
        if dir == 0:
            absolute_coordinate = (a+(6-x), b+(y-3))
        elif dir == 1:
            absolute_coordinate = (a+(3-y), b+(6-x))
        elif dir == 2:
            absolute_coordinate = (a-(6-x), b-(y-3))
        elif dir == 3:
            absolute_coordinate = (a+(y-3), b-(6-x))
        print(absolute_coordinate)
        return absolute_coordinate