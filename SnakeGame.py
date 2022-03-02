import turtle
import time
from random import randint

# Defines the data to be collected during the game
# Will be used for input into the neural network
class Input:
    # Currently tracking:
    # Obstacles (body parts or edge of the screen) in front, right, or left of head
    # The predicted direction of the head
    def __init__(self, f, r, l, dir):
        self.obs_front = f
        self.obs_right = r
        self.obs_left = l
        self.dir = dir
    
    def get_obs_front(self):
        return self.obs_front
    
    def get_obs_right(self):
        return self.obs_right

    def get_obs_left(self):
        return self.obs_left

    def get_dir(self):
        return self.dir

class SnakeGame:
    def __init__(self, window_size = 400, gui = False, training = False, food_amt = 1, delay = 0):
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
        # Delay for game update
        self.delay = delay
        # Set up board and gui
        self.display()
    
    # Initialize the game board
    def display(self):
        # initialize the window
        if self.gui:
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
        self.head.direction = "stop"

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
    
    # Direction changing functions
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
            if self.gui:
                self.window.update()
            # Check for loss
            if self.check_loss() == True:
                print("finished")
                self.finished = True # Useless failsafe
                # Record final body positions and hide them
                body_positions = []
                for k in self.body:
                    body_positions.append(k.pos())
                    k.goto(self.bound + 100, self.bound + 100)
                # Clear board
                for k in range(self.food_amt):
                    self.food[k].goto(self.bound + 100, self.bound + 100)
                self.head.goto(self.bound + 100, self.bound + 100)
                return (self.score, self.head.pos(), body_positions, self.moves)
            # Check if eating food
            for k in range(self.food_amt):
                if self.head.distance(self.food[k]) < 20:
                    print("eating food")
                    # Update score
                    self.score += 1
                    # Move food
                    a,b = self.food_spot()
                    self.food[k].goto(a,b)
                    # Add new body part
                    print("adding body part")
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
            self.make_decision()
            if self.training:
                self.record_data()
            self.move()
            time.sleep(self.delay)

    # Checks if the game state results in a loss
    def check_loss(self):
        if self.head.xcor() > self.bound or self.head.xcor() < (-self.bound) or self.head.ycor() > self.bound or self.head.ycor() < (-self.bound):
            print("out of bounds!")
            return True
        for seg in self.body:
            if seg.distance(self.head) < 20:
                print("hit body!")
                return True
        return False
    
    # Returns a random spot for a new food object to spawn, allowing overlap with the snake
    def food_spot(self):
        b = (self.window_size / 2) - 20
        x = randint(-b, b)
        y = randint(-b, b)
        return (x,y)

    # Will allow for the neural network to make a decision
    def make_decision(self, is_random = True):
        if is_random:
            r = randint(1,4)
            if r == 1:
                self.up()
            elif r == 2:
                self.down()
            elif r == 3:
                self.right()
            else:
                self.left()
        else: # Otherwise, ask the bot for a decision
            pass

    # Records the game state in the moves array
    def record_data(self):
        # First, find the information
        front = 0
        right = 0
        left = 0
        for seg in self.body:
            if seg.distance(self.head) == 20:
                if self.head.direction == "up":
                    if self.check_up(seg):
                        front = 1
                    elif self.check_right(seg):
                        right = 1
                    elif self.check_left(seg):
                        left = 1
                if self.head.direction == "down":
                    if self.check_down(seg):
                        front = 1
                    elif self.check_right(seg):
                        left = 1
                    elif self.check_left(seg):
                        right = 1
                if self.head.direction == "right":
                    if self.check_up(seg):
                        left = 1
                    elif self.check_right(seg):
                        front = 1
                    elif self.check_down(seg):
                        right = 1
                if self.head.direction == "left":
                    if self.check_up(seg):
                        right = 1
                    elif self.check_down(seg):
                        left = 1
                    elif self.check_left(seg):
                        front = 1
        state = Input(front, right, left, 1)
        self.moves.append(state)
    
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

game = SnakeGame(gui = True, training = True, food_amt = 1, delay = 0.1)
#score, head_pos, body_positions, training_data = game.run()