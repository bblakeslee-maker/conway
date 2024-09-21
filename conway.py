import pathlib
import time
import typing

import numpy as np
import scipy.ndimage as sni
import yaml


class Conway:
    def __init__(self, config_path: pathlib.Path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.__threshold = float(config['threshold'])
        self.__interval = float(config['interval'])
        self.__max_iterations = int(config['iterations'])
        self.__iteration_counter = 1
        self.__neighbor_filter = np.array([[1, 1, 1],
                                           [1, 0, 1],
                                           [1, 1, 1]])
        self.__world = self.__init_world(config)

    def __init_world(self, config: typing.Dict):
        if config['world'] is None:
            if 0.0 <= self.__threshold <= 1:
                print('Initializing random world!')
                self.__height = int(config['height'])
                self.__width = int(config['width'])
                return np.random.choice(
                    (0, 1),
                    size=(self.__height, self.__width),
                    p=(1 - self.__threshold, self.__threshold))
            else:
                raise ValueError('ERROR: Invalid threshold value!')
        else:
            print('Initializing fixed world!')
            fixed_world = np.array(config['world'])
            self.__height, self.__width = fixed_world.shape
            return fixed_world

    def update_grid(self):
        new_world = np.zeros(self.__world.shape, dtype=int)
        # This wrap parameter assumes that the world is round
        neighbor_counts = sni.convolve(self.__world, self.__neighbor_filter, mode='wrap')

        # A cell that is alive retains its alive state if exactly 2 or 3 neighbors are alive
        survivor = (self.__world == 1) & ((neighbor_counts == 2) | (neighbor_counts == 3))
        # A cell that is dead becomes alive if exactly 3 of its neighbors are alive
        new_cell = (self.__world == 0) & (neighbor_counts == 3)
        new_world[survivor | new_cell] = 1

        # Technically, since the new world is already zeroed, these conditions aren't necessary.
        # However, they are included for completeness.
        # A cell that is alive changes state to dead if its neighbors include 0 or 1 alive cells
        dead_cell_1 = (self.__world == 1) & ((neighbor_counts == 0) | (neighbor_counts == 1))
        # A cell that is alive changes state to dead if more than 3 neighbors are alive
        dead_cell_2 = (self.__world == 1) & (neighbor_counts > 3)
        new_world[dead_cell_1 | dead_cell_2] = 0

        self.__world = new_world
        time.sleep(self.__interval)
        self.__iteration_counter += 1
        if self.dead_world():
            raise ValueError('World is dead, aborting...')
        if (self.__max_iterations > 0) and (self.__iteration_counter > self.__max_iterations):
            raise ValueError('Reached maximum iterations, aborting...')

    def dead_world(self):
        return np.sum(self.__world) == 0

    def __str__(self):
        return (f'Iteration {self.__iteration_counter:,} / {self.__max_iterations:,}\n' +
                str(self.__world))
