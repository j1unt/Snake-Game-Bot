from SnakeGame import SnakeGame
from SnakeGame import Input
from SnakeNeuralNetwork import SnakeNN
from random import randint
import numpy as np
import math

# CONSTANTS
TRAIN_AMT = 500
MID_LAYER_NEURONS = 20
BATCH_SIZE = 20
OUTPUT_SHAPE = 2
GAMES = 20

# Functions
def gen_data():
    data = []
    dirs = []
    for k in range(TRAIN_AMT):
        game = SnakeGame(200, False, True, 20, 0, False, None)
        s, h, b, td = game.run()
        for move in td:
            x = [move.get_obs_front(), move.get_obs_right(), move.get_obs_left(), move.get_wall()]
            data.append(x)
            dirs.append(move.get_dir())
        print("Game: ", k)
    return data, dirs
    
# Main Code
output = 0
training_data, y = gen_data()

# Train NN
model = SnakeNN(MID_LAYER_NEURONS, OUTPUT_SHAPE, BATCH_SIZE)
model.input(training_data, y)
model.train()

# Play game with trained model
for k in range(GAMES):
    game = SnakeGame(300, True, True, 5, 0.15, True, model)
    game.run()