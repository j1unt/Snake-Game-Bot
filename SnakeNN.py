import random
import math
import numpy as np

# Simple implementation of a neural network
# This does not have to scale easily, and is designed with that in mind
class SnakeNN:
    def __init__(self, input, n_per_layer, output):

        # Input is an array of arrays, where input[i] is an array with data mapped to each neuron in the middle layer
        self.input = input

        # Weights from input to middle layer
        self.weights1 = np.random.rand(self.input.shape[1], n_per_layer)
        # Weights from middle layer to output
        self.weights2 = np.random.rand(4,1)
        
        # Biases are arrays where biases[i] corresponds to a set of weights
        self.biases1 = np.zeros(self.input.shape[1, n_per_layer])
        self.biases2 = np.zeros(4,1)

        # This formats the output
        self.output = np.zeros(output.shape)

    def feed_forward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1) + self.biases1)
        self.output = sigmoid(np.dot(self.layer1, self.weights2) + self.biases2)

    def backpropagate(self):
        # Applies the chain rule to minimize the loss function with respect to weights and biases
        w1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1)))
        w2 = np.dot(self.layer1.T, (2*(self.y - self.output) * sigmoid_derivative(self.output)))

        # Update weights to account for loss
        self.weights1 += w1
        self.weights2 += w2

# Activation function
def sigmoid(x):
    sig = 1 / (1 + math.exp(-x))
    return sig

# Sigmoid derivative for loss function
def sigmoid_derivative(x):
    return x * (1.0 - x)