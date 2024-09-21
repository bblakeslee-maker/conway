import pathlib
import time

import numpy as np
import scipy.ndimage as sni
import yaml


class Conway:
    def __init__(self, config_path: pathlib.Path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.__threshold = float(config['threshold'])
        self.__interval = float(config['interval'])
        self.__iterations = int(config['iterations'])
        self.__height = int(config['height'])
        self.__width = int(config['width'])
        self.__world = self.__init_world()
        self.__neighbor_filter = np.array([[1, 1, 1],
                                           [1, 0, 1],
                                           [1, 1, 1]])

    def __init_world(self):
        return np.random.choice(
            (0, 1),
            size=(self.__height, self.__width),
            p=(1 - self.__threshold, self.__threshold))

    def update_grid(self):
        new_board = np.zeros(self.__world.shape)
        neighbor_counts = sni.convolve(self.__world, self.__neighbor_filter, mode='wrap')
        survivor = (self.__world == 1) & ((neighbor_counts == 2) | (neighbor_counts == 3))
        new_cell = (self.__world == 0) & (neighbor_counts == 3)
        new_board[survivor | new_cell] = 1
        self.__world = new_board
        time.sleep(self.__interval)

    def __str__(self):
        return str(self.__world)
