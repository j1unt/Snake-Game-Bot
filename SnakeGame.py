import turtle
import time
from random import randint

class SnakeGame:
    def __init__(self, window_size = 400, gui = False):
        self.score = 0
        self.window_size = window_size
        self.finished = False
        self.gui = False
        # Array of body parts to check their positions
        self.body = []
    
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
        a,b = self.foodspot()
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
        delay = 0.1

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
            self.window.update()
            # Check for loss
            if self.check_loss() == True:
                print("finished")
                self.finished = True
                last_body_pos = []
                for k in self.body:
                    last_body_pos.append(k.pos())
                return (self.score, self.head.pos(), last_body_pos)
            # Check if eating food
            if self.head.distance(self.food) < 20:
                print("eating food")
                # Update score
                self.score += 1
                # Move food
                a,b = self.foodspot()
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
            self.make_decision()
            self.move()
            time.sleep(delay)

    # Checks if the game state results in a loss
    def check_loss(self):
        bound = (self.window_size / 2) - 10
        if self.head.xcor() > bound or self.head.xcor() < (-1 * bound) or self.head.ycor() > bound or self.head.ycor() < (-1 * bound):
            print("out of bounds!")
            return True
        for seg in self.body:
            if seg.distance(self.head) < 20:
                print("hit body!")
                return True
        return False
    
    # Returns a random spot for a new food object to spawn, allowing overlap with the snake
    def foodspot(self):
        b = (self.window_size / 2) - 20
        x = randint(-1 * b, b)
        y = randint(-1 * b, b)
        return (x,y)

    # Will allow for the neural network to make a decision
    def make_decision(self):
        r = randint(1,4)
        if r == 1:
            self.up()
        elif r == 2:
            self.down()
        elif r == 3:
            self.right()
        else:
            self.left()

game = SnakeGame(gui = True)
game.display()
print(game.run())