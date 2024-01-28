import turtle
import random

class Game:
    # Setting up the game and its screen
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Egg Catcher by Lagayada & Emano")
        self.screen.bgcolor("deep sky blue")
        self.screen.setup(width=900, height=600)
        self.basket = None
        self.eggs = []
        self.clouds = []
        self.egg_speed = 0
        self.egg_interval = 0
        self.score = 0
        self.lives = 0

    # Calling the following methods
    def setup(self):
        self.create_rectangle()
        self.create_sun()
        self.create_basket()
        self.set_difficulty()
        self.create_initial_clouds()
        self.setup_keyboard_bindings()

    # Setting up background using rectangle
    def create_rectangle(self):
        rectangle = turtle.Turtle()
        rectangle.speed(0)
        rectangle.penup()
        rectangle.goto(100, -250)
        rectangle.shape("square")
        rectangle.shapesize(stretch_wid=10, stretch_len=130)
        rectangle.color("forest green")

    #Creating sun
    def create_sun(self):
        oval = turtle.Turtle()
        oval.speed(0)
        oval.penup()
        oval.goto(-400, 260)
        oval.shape("circle")
        oval.shapesize(stretch_wid=10, stretch_len=10)
        oval.color("orange")

    # Creating Basket
    def create_basket(self):
        self.basket = turtle.Turtle()
        self.basket.shape("circle")
        self.basket.color("sienna")
        self.basket.shapesize(stretch_wid=1, stretch_len=5)
        self.basket.penup()
        self.basket.speed(0)
        self.basket.goto(0, -250)

    # Setting up Difficulty Levels
    def set_difficulty(self):
        # On screen User Input 
        difficulty = self.screen.textinput("Difficulty", "Choose difficulty (easy/hard): ")

        if difficulty == "easy":
            self.egg_speed, self.egg_interval = 7, 10000  # Egg speed, Egg interval
        elif difficulty == "hard":
            self.egg_speed, self.egg_interval = 12, 10000  # Egg speed, Egg interval
        else:
            print("Invalid difficulty level. Defaulting to easy.")
            self.egg_speed, self.egg_interval = 7, 5000  # Default to easy

    # Initializing the clouds
    def create_initial_clouds(self):
        self.clouds = [self.create_cloud(random.randint(-400, 400), random.randint(100, 200)) for _ in range(3)]

    # Creating clouds
    def create_cloud(self, x, y):
        cloud = turtle.Turtle()
        cloud.speed(0)
        cloud.penup()
        cloud.goto(x, y)
        cloud.shape("circle")
        cloud.color("white")
        cloud.shapesize(stretch_wid=2, stretch_len=6)
        return cloud

    # Keyboard Controls
    def setup_keyboard_bindings(self):
        self.screen.listen()
        self.screen.onkeypress(lambda: self.basket.setx(self.basket.xcor() - 30), "Left")
        self.screen.onkeypress(lambda: self.basket.setx(self.basket.xcor() + 30), "Right")
        self.screen.ontimer(self.create_egg, 15000) # 15 seconds

    # Creating Eggs
    def create_egg(self):
        # Generate a random number between 0 and 1
        random_number = random.random()

        # Adjust this threshold to control the quantity of eggs (e.g., 0.5 for fewer eggs)
        if random_number < 0.5:
            x = random.randint(-290, 290)
            y = 250
            new_egg = turtle.Turtle()
            new_egg.shape("circle")
            new_egg.color("light pink")
            new_egg.shapesize(stretch_wid=3, stretch_len=2)
            new_egg.penup()
            new_egg.speed(0)
            new_egg.goto(x, y)
            self.eggs.append(new_egg)

        # Schedule the creation of a new egg again after the interval
        self.screen.ontimer(self.create_egg, self.egg_interval)

    # Clouds Movement
    def move_cloud(self, cloud, speed):
        x = cloud.xcor()
        x -= speed
        cloud.setx(x)

    # checking the clouds coordinate
    def is_cloud_out_of_screen(self, cloud):
        return cloud.xcor() < -450

    # Looping the game
    def game_loop(self):
        self.lives = 3
        self.score = 0
        while self.lives > 0:
            # Check if there are no eggs on the screen
            if not self.eggs:
                x = random.randint(-290, 290)
                y = 250
                new_egg = turtle.Turtle()
                new_egg.shape("circle")
                new_egg.color("light pink")
                new_egg.shapesize(stretch_wid=3, stretch_len=2)
                new_egg.penup()
                new_egg.speed(0)
                new_egg.goto(x, y)
                self.eggs.append(new_egg)

            # Move and check clouds
            for cloud in self.clouds:
                self.move_cloud(cloud, 2)
                if self.is_cloud_out_of_screen(cloud):
                    new_x = random.randint(400, 600)
                    new_y = random.randint(100, 200)
                    cloud.goto(new_x, new_y)

            for egg in self.eggs:
                egg.sety(egg.ycor() - self.egg_speed) # Adjust the speed of the eggs

                # Check if the basket caught the egg
                if self.basket.distance(egg) < 30:
                    egg.goto(random.randint(-290, 290), 250)
                    self.score += 10
                    self.screen.title("Egg Catcher - Score: {} Lives: {}".format(self.score, self.lives))

                # Check if the egg reached the bottom
                if egg.ycor() < -290:
                    egg.goto(random.randint(-290, 290), 250)
                    self.lives -= 1
                    self.screen.title("Egg Catcher - Score: {} Lives: {}".format(self.score, self.lives))
                    if self.lives == 0:
                        turtle.penup()
                        turtle.goto(0, 0)
                        turtle.color("maroon")
                        turtle.write("Game Over! Final Score: {}".format(self.score), align="center",
                                     font=("Times", 45, "bold"))
                        turtle.hideturtle()
                        turtle.done()

            # Screen update
            self.screen.update()

# Initial game set up
if __name__ == "__main__":
    game_instance = Game()
    game_instance.setup()
    game_instance.game_loop()
    turtle.mainloop()           # Start the turtle main loop
