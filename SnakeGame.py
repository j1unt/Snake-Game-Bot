import turtle
import time
from random import randint

# Defines the data to be collected during the game
# Will be used for input into the neural network
class TrainingData:
    # Currently tracking:
    # Obstacles (body parts or edge of the screen) in front, right, or left of head
    # The current direction of the head
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
    def __init__(self, window_size = 400, gui = False, training = False):
        self.score = 0
        self.window_size = window_size
        self.bound = (window_size / 2) - 10
        self.finished = False
        self.gui = False
        # Array of body parts to check their positions
        self.body = []
        # This will be an array of TrainingData structures
        # It records data about the game state at each move
        self.training = training
        self.moves = []
    
    # Initialize the game board
    def display(self):
        # initialize the window
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

        # initialize the food
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        a,b = self.food_spot()
        self.food.goto(a,b)
    
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

        # Sets update delay
        delay = 0.2

        # Adds controls

        self.window.listen()
        self.window.onkeypress(self.up, "w")
        self.window.onkeypress(self.down, "s")
        self.window.onkeypress(self.right, "d")
        self.window.onkeypress(self.left, "a")


        # Structure: Check for loss -> Check if eating food -> Make new move
        while self.finished == False:
            self.window.update()
            # Check for loss
            if self.check_loss() == True:
                print("finished")
                self.finished = True
                body_positions = []
                for k in self.body:
                    body_positions.append(k.pos())
                return (self.score, self.head.pos(), body_positions, self.moves)
            # Check if eating food
            if self.head.distance(self.food) < 20:
                print("eating food")
                # Update score
                self.score += 1
                # Move food
                a,b = self.food_spot()
                self.food.goto(a,b)
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
            # self.make_decision()
            if self.training:
                self.record_data()
            self.move()
            time.sleep(delay)

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
        front = False
        right = False
        left = False
        for seg in self.body:
            if seg.distance(self.head) == 20:
                if self.head.direction == "up":
                    if self.check_up(seg):
                        front = True
                    elif self.check_right(seg):
                        right = True
                    elif self.check_left(seg):
                        left = True
                if self.head.direction == "down":
                    if self.check_down(seg):
                        front = True
                    elif self.check_right(seg):
                        left = True
                    elif self.check_left(seg):
                        right = True
                if self.head.direction == "right":
                    if self.check_up(seg):
                        left = True
                    elif self.check_right(seg):
                        front = True
                    elif self.check_down(seg):
                        right = True
                if self.head.direction == "left":
                    if self.check_up(seg):
                        right = True
                    elif self.check_down(seg):
                        left = True
                    elif self.check_left(seg):
                        front = True
        state = TrainingData(front, right, left, self.head.direction)
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

game = SnakeGame(gui = True, training = True)
game.display()
score, head_pos, body_positions, training_data = game.run()