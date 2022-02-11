import random
import math
import numpy as np

# Simple implementation of a neural network
# This does not have to scale easily, and is designed with that in mind
class SnakeNN:
    def __init__(self, input, n_per_layer, output):
        # Input is an array of arrays, where input[i] is an array with data from a move state
        # The data is formatted in the same order as Input objects
        # obs_front, obs_right, obs_left, head_dir
        self.input = input
        # This formats the output layer (not really needed)
        self.output = output
        # Weights from input layer to middle layer
        self.weights1 = np.random.rand(np.array(self.input).shape[0], n_per_layer)
        # Weights from middle layer to output layer
        self.weights2 = np.random.rand(n_per_layer,1)
        # Biases from input layer to middle layer
        self.biases1 = np.zeros((np.array(self.input).shape[0], n_per_layer))
        # Biases from middle layer to output layer
        self.biases2 = np.zeros((n_per_layer,1))

    def feed_forward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1) + self.biases1)
        self.output = sigmoid(np.dot(self.layer1, self.weights2) + self.biases2)

    # This function is currently a placeholder to test the network and will be refactored later
    def backpropagate(self):
        # Applies the chain rule to minimize the loss function with respect to weights and biases
        w1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1)))
        w2 = np.dot(self.layer1.T, (2*(self.y - self.output) * sigmoid_derivative(self.output)))

        # Update weights to account for loss
        self.weights1 += w1
        self.weights2 += w2
    
    def train(self):
        self.feed_forward()
        self.backpropagate()

# Activation function
def sigmoid(x):
    sig = 1 / (1 + math.exp(-x))
    return sig

# Sigmoid derivative for loss function
def sigmoid_derivative(x):
    return x * (1.0 - x)