from SnakeGame import SnakeGame
from SnakeGame import Input
from SnakeNN import SnakeNN
from random import randint
import numpy as np
import math

# CONSTANTS
TRAIN_AMT = 100
MID_LAYER_NEURONS = 25

# Function Definitions
def gen_data():
    data = []
    for k in range(TRAIN_AMT):
        game = SnakeGame(400, False, True, 20, 0)
        s, h, b, td = game.run()
        for move in td:
            x = [move.get_obs_front(), move.get_obs_right(), move.get_obs_left(), move.get_dir()]
            data.append(x)
    return data
    
# Main Code
output = 0
training_data = gen_data()
network = SnakeNN(training_data, 25, output)
network.train()