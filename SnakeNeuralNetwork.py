import numpy as np
import pandas as pd
import torch
import torch.nn as nn

class SnakeNN:
    def __init__(self, hidden_size, out_size, batch_size):
        self.hidden_size = hidden_size
        self.out_size = out_size
        self.batch_size = batch_size
        self.input_size = 0

    def input(self, data, y):
        self.input_size = len(data[0])
        self.input = data
        self.y = y
        self.gen_model()
        
    def gen_model(self):
        self.model = nn.Sequential(nn.Linear(self.input_size, self.hidden_size),
                     nn.ReLU(),
                     nn.Linear(self.hidden_size, self.out_size),
                     nn.Sigmoid())
        self.gen_optim()
        self.gen_loss()

    def gen_optim(self):
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=0.01)

    def gen_loss(self):
        self.criterion = torch.nn.MSELoss()

    def train(self):
        pos = 0
        epochs = 15000
        for k in range(epochs):
            # Generate Dataset
            dataset = []
            parallel_y = []
            for i in range(pos, pos + self.batch_size):
                dataset.append(self.input[i])
                parallel_y.append(self.y[i])
            dataset = torch.tensor(dataset, dtype=torch.float)
            parallel_y = torch.tensor(parallel_y, dtype=torch.float)

            # Forward pass
            forward = self.model(dataset)

            # Calculate loss
            loss = self.criterion(forward, parallel_y)
            print('Iteration: ', k, '  Loss: ', loss.item())

            # Zero the gradient and backpropagate
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
    
    # Return a decision from the trained model
    def decide(self, i):
        i = torch.tensor(i, dtype=torch.float)
        return self.model(i)