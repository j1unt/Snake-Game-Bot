# Snake-Game-Bot

This project uses a simple neural network to play a snake game (same rules as https://www.googlesnake.com/). The goal of the project was to get effective results and learn about machine learning and related libraries.

The snake game itself was created using Turtle graphics. The neural network was implemented using PyTorch.

Installation:

With PyTorch installed, clone the repository or download the three .py files and run SnakeBot.py.

Current state of the project:

Snake moves towards the food and generally survives, but does so in a convoluted way.

Training sets from over 10,000 games played usually make the snake run in a circle. Planning to give more valuable input, and tweak the model structure to train more effectively.

Turtle graphics is a major inhibitor for training efficiency since it requires turtle objects to be created for a game to run. I may implement a workaround in the future, or switch to a different graphics library entirely.

Games only last 80 moves in this video.

https://user-images.githubusercontent.com/68975535/157800561-6e162634-fe58-4d82-b53e-2fc18e12a79b.mp4
