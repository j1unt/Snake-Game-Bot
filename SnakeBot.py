from SnakeGame import SnakeGame
from SnakeGame import Input
from SnakeNeuralNetwork import SnakeNN
from random import randint
import numpy as np
import math

# CONSTANTS
TRAIN_AMT = 100
MID_LAYER_NEURONS = 4

# Functions
def gen_data():
    data = []
    dirs = []
    for k in range(TRAIN_AMT):
        game = SnakeGame(400, False, True, 20, 0)
        s, h, b, td = game.run()
        for move in td:
            x = [move.get_obs_front(), move.get_obs_right(), move.get_obs_left()]
            data.append(x)
            dirs.append(move.get_dir())
    return data, dirs
    
# Main Code
output = 0
training_data, y = gen_data()

model = SnakeNN(4, 1, 32)
model.input(training_data, y)
model.train()

# Train NN