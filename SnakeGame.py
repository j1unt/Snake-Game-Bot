import turtle
import time
import torch
import math
from random import randint

# Defines the data to be collected during the game
# Will be used for input into the neural network
class Input:
    # Currently tracking:
    # Obstacles (body parts or edge of the screen) in front, right, or left of head
    # whether or not the head is in the right direction to reach the food (1 yes, -1 no)
    # The correct choice of direction for the head
    def __init__(self, f, r, l, i, dir):
        self.obs_front = f
        self.obs_right = r
        self.obs_left = l
        self.in_dir = i
        self.dir = dir
    
    def get_obs_front(self):
        return self.obs_front
    
    def get_obs_right(self):
        return self.obs_right

    def get_obs_left(self):
        return self.obs_left

    def get_in_dir(self):
        return self.in_dir

    def get_dir(self):
        return self.dir

class SnakeGame:
    def __init__(self, window_size = 400, gui = False, training = False, food_amt = 1, delay = 0, playing = False, model = None):
        self.score = 0
        self.window_size = window_size
        self.bound = (window_size / 2) - 10
        self.gui = gui
        self.food_amt = food_amt
        self.finished = False
        # Array of body parts to check their positions
        self.body = []
        # This will be an array of TrainingData structures
        # It records data about the game state at each move
        self.training = training
        self.moves = []
        # Tracks the last position of the head
        self.old_head_x = 0
        self.old_head_y = 0
        # Delay for game update
        self.delay = delay
        # Set up board and gui
        self.display()
        # True if the model will be making decisions
        self.playing = playing
        # Takes a trained model to make decisions
        self.model = model
        self.current_state = Input(0,0,0,0,0)

        # Tracking variables to stop cancel runs if the snake is circling
        self.max_moves = 40
        self.test_moves = 0
        self.circling = False
    
    # Initialize the game board
    def display(self):
        # initialize the window
        #print("Starting GUI")
        self.window = turtle.Screen()
        self.window.title("Snake Game")
        self.window.bgcolor("blue")
        self.window.setup(self.window_size, self.window_size)
        self.window.tracer(0)

        # initialize the snake
        self.head = turtle.Turtle()
        self.head.shape("square")
        self.head.color("yellow")
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "up"

        self.food = []
        # initialize the food
        for k in range(self.food_amt):
            f = turtle.Turtle()
            f.speed(0)
            f.shape("circle")
            f.color("red")
            f.penup()
            a,b = self.food_spot()
            f.goto(a,b)
            self.food.append(f)

    # Moves the head in the current direction
    def move(self):
        if self.head.direction == "up":
            y = self.head.ycor()
            self.head.sety(y + 20)
        if self.head.direction == "down":
            y = self.head.ycor()
            self.head.sety(y - 20)
        if self.head.direction == "left":
            x = self.head.xcor()
            self.head.setx(x - 20)
        if self.head.direction == "right":
            x = self.head.xcor()
            self.head.setx(x + 20)

    # Run main game loop
    def run(self):

        # Adds controls
        """
        self.window.listen()
        self.window.onkeypress(self.up, "w")
        self.window.onkeypress(self.down, "s")
        self.window.onkeypress(self.right, "d")
        self.window.onkeypress(self.left, "a")
        """

        # Structure: Check for loss -> Check if eating food -> Make new move
        while self.finished == False:

            if self.gui == True:
                self.window.update()
            # Check for loss
            if self.check_loss() == True or self.circling == True:
                # Record final data
                self.record_data(True)
                # Record final body positions
                body_positions = []
                # Clear board
                for k in self.body:
                    body_positions.append(k.pos())
                    k.goto(self.bound + 100, self.bound + 100)
                self.window.clear()
                return (self.score, self.head.pos(), body_positions, self.moves)
            
            # Check if eating food
            for k in range(self.food_amt):
                if self.head.distance(self.food[k]) < 20:
                    #print("eating food")
                    # Update score
                    self.score += 1
                    # Move food
                    a,b = self.food_spot()
                    self.food[k].goto(a,b)
                    # Add new body part
                    bp = turtle.Turtle()
                    bp.speed(0)
                    bp.shape("square")
                    bp.color("green")
                    bp.penup()
                    self.body.append(bp)

            # Update body part positions
            for i  in range(len(self.body)- 1, 0, -1):
                x = self.body[i - 1].xcor()
                y = self.body[i - 1].ycor()
                self.body[i].goto(x, y)
            if len(self.body) > 0:
                x = self.head.xcor()
                y = self.head.ycor()
                self.body[0].goto(x, y)

            # Make new move
            self.make_decision(self.playing)
            self.current_state = self.record_data()
            self.old_head_x = self.head.xcor()
            self.old_head_y = self.head.ycor()
            self.move()
            time.sleep(self.delay)
    # End main game loop

    # Checks if the game state results in a loss
    def check_loss(self):
        if self.head.xcor() > self.bound or self.head.xcor() < (-self.bound) or self.head.ycor() > self.bound or self.head.ycor() < (-self.bound):
            return True
        for seg in self.body:
            if seg.distance(self.head) < 20:
                return True
        return False
    
    # Returns a random spot for a new food object to spawn, allowing overlap with the snake
    def food_spot(self):
        b = (self.window_size / 2) - 20
        x = randint(-b, b)
        y = randint(-b, b)
        return (x,y)

    # Will allow for the neural network to make a decision
    def make_decision(self, dec = False):
        if not dec:
            self.rand_dir()
        else: # Otherwise, ask the bot for a decision
            self.test_moves += 1
            print("Move:", self.test_moves)
            if self.test_moves == self.max_moves:
                print("Circling")
                self.circling = True
                self.test_moves = 0
            i1 = [self.current_state.get_obs_left(), 
                self.current_state.get_obs_front(), 
                self.current_state.get_obs_right(),
                self.current_state.get_in_dir(), -1]
            i2 = [self.current_state.get_obs_left(), 
                self.current_state.get_obs_front(), 
                self.current_state.get_obs_right(),
                self.current_state.get_in_dir(), 0]
            i3 = [self.current_state.get_obs_left(), 
                self.current_state.get_obs_front(), 
                self.current_state.get_obs_right(),
                self.current_state.get_in_dir(), 1]
            d1 = self.model.decide(i1)
            d2 = self.model.decide(i2)
            d3 = self.model.decide(i3)
            d1 = d1.detach().numpy()
            d2 = d2.detach().numpy()
            d3 = d3.detach().numpy()
            d = max(d1, d2, d3)
            print("D1, Left:", d1)
            print("D2, Straight:", d2)
            print("D3, Right:", d3)
            if d == d1:
                print("Turned left")
                self.turn_left()
            elif d == d2:
                print("Turned straight")
                self.keep_dir()
            else:
                print("Turned right")
                self.turn_right()

    # Records the game state in the moves array
    def record_data(self, dead = False):
        # Information to aqcuire
        correct_output = 0
        front = 0
        right = 0
        left = 0
        angle = 0
        
        # Checks for objects to the front, left, and right of the head
        for seg in self.body:
            if seg.distance(self.head) == 20:
                if self.head.direction == "up":
                    if self.check_up(seg) or self.check_wall_up():
                        front = 1
                    elif self.check_right(seg) or self.check_wall_right():
                        right = 1
                    elif self.check_left(seg) or self.check_wall_left():
                        left = 1
                elif self.head.direction == "down":
                    if self.check_down(seg) or self.check_wall_down():
                        front = 1
                    elif self.check_right(seg) or self.check_wall_right():
                        left = 1
                    elif self.check_left(seg) or self.check_wall_left():
                        right = 1
                elif self.head.direction == "right":
                    if self.check_up(seg) or self.check_wall_up():
                        left = 1
                    elif self.check_right(seg) or self.check_wall_right():
                        front = 1
                    elif self.check_down(seg) or self.check_wall_down():
                        right = 1
                elif self.head.direction == "left":
                    if self.check_up(seg) or self.check_wall_up():
                        right = 1
                    elif self.check_down(seg) or self.check_wall_down():
                        left = 1
                    elif self.check_left(seg) or self.check_wall_left():
                        front = 1
        if self.head.direction == "up":
            if self.check_wall_up():
                front = 1
            elif self.check_wall_right():
                right = 1
            elif self.check_wall_left():
                left = 1
        elif self.head.direction == "down":
            if self.check_wall_down():
                front = 1
            elif self.check_wall_right():
                left = 1
            elif self.check_wall_left():
                right = 1
        elif self.head.direction == "right":
            if self.check_wall_up():
                left = 1
            elif self.check_wall_right():
                front = 1
            elif self.check_wall_down():
                right = 1
        elif self.head.direction == "left":
            if self.check_wall_up():
                right = 1
            elif self.check_wall_down():
                left = 1
            elif self.check_wall_left():
                front = 1
        # Check if head direction is the most efficient to find food
        # If head is going towards the most desirable direction, return 1, else return -1
        in_right_dir = 0
        food_pos_x, food_pos_y = self.food[0].xcor(), self.food[0].ycor()
        head_pos_x, head_pos_y = self.head.xcor(), self.head.ycor()
        if abs(head_pos_x - food_pos_x) > abs(head_pos_y - food_pos_y):
            # Food is further from head x coord
            if head_pos_x < food_pos_x:
                if self.head.direction == "right":
                    in_right_dir = 1
                else:
                    in_right_dir = -1
            else:
                if self.head.direction == "left":
                    in_right_dir = 1
                else:
                    in_right_dir = -1
        else:
            # Food is further from head y coord
            if head_pos_y < food_pos_y:
                if self.head.direction == "up":
                    in_right_dir = 1
                else:
                    in_right_dir = -1
            else:
                if self.head.direction == "down":
                    in_right_dir = 1
                else:
                    in_right_dir = -1

        # Logs nearby object states for test games
        if self.playing == True:
            print("Left:", left)
            print("Front:", front)
            print("Right:", right)
        
        # First, find the change in distance between the head and the food 
        # Then, record the correct decision
        # distance_delta is positive if the head got closer to the food
        distance_delta = (math.sqrt(pow(self.old_head_x - self.food[self.food_amt - 1].xcor(), 2) +
                                   pow(self.old_head_y - self.food[self.food_amt - 1].ycor(), 2)) -
                          math.sqrt(pow(self.head.xcor() - self.food[self.food_amt - 1].xcor(), 2) + 
                                   pow(self.head.ycor() - self.food[self.food_amt - 1].ycor(), 2)))
        if dead:
            correct_output = -1
        elif distance_delta > 0:
            correct_output = 1

        # Adds the state to the log and returns to update the current state
        state = Input(front, right, left, in_right_dir, correct_output)
        self.moves.append(state)
        return state

    # DIRECTION CHANGING FUNCTIONS
    # Lower Level:
    def up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def left(self):
        if self.head.direction != "right":
            self.head.direction = "left"
    
    # Higher Level:
    def keep_dir(self):
        dir = self.head.direction
        if dir == "up":
            self.up()
        elif dir == "down":
            self.down()
        elif dir == "right":
            self.right()
        elif dir == "left":
            self.left()

    def turn_right(self):
        dir = self.head.direction
        if dir == "up":
            self.right()
        elif dir == "down":
            self.left()
        elif dir == "right":
            self.down()
        elif dir == "left":
            self.up()
        
    def turn_left(self):
        dir = self.head.direction
        if dir == "up":
            self.left()
        elif dir == "down":
            self.right()
        elif dir == "right":
            self.up()
        elif dir == "left":
            self.down()
    
    def rand_dir(self):
        r = randint(1,4)
        if r == 1:
            self.up()
        elif r == 2:
            self.down()
        elif r == 3:
            self.right()
        else:
            self.left()
    
    # OBSTACLE CHECKING FUNCTIONS
    def check_up(self, seg):
        if self.head.ycor() + 20 == seg.ycor():
            return True
        return False

    def check_down(self, seg):
        if self.head.ycor() - 20 == seg.ycor():
            return True
        return False
    
    def check_right(self, seg):
        if self.head.xcor() + 20 == seg.xcor():
            return True
        return False
    
    def check_left(self, seg):
        if self.head.xcor() - 20 == seg.xcor():
            return True
        return False

    def check_wall_up(self):
        if self.head.ycor() + 40 >= self.bound:
            return True
        return False

    def check_wall_down(self):
        if self.head.ycor() - 40 <= -self.bound:
            return True
        return False
    
    def check_wall_right(self):
        if self.head.xcor() + 40 >= self.bound:
            return True
        return False
    
    def check_wall_left(self):
        if self.head.xcor() - 40 <= -self.bound:
            return True
        return False

# This runs a game with random moves! (Or commands if you enable them!)
# game = SnakeGame(800, gui = True, training = True, food_amt = 1, delay = 0.1)
# score, head_pos, body_positions, training_data = game.run()