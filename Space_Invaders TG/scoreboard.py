from turtle import Turtle

FONT = ("Arial", 15, "normal")


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.lives = 3
        self.score = 0
        self.pencolor("white")
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-110, 320)
        self.write(f"Lives Remained: {self.lives}", move=False, align="center", font=FONT)
        self.goto(110, 320)
        self.write(f"Score: {self.score}", move=False, align="center", font=FONT)

    def reduce_lives(self):
        self.lives -= 1
        self.update_scoreboard()

    def increase_score(self):
        self.score += 100
        self.update_scoreboard()

    def win(self):
        self.goto(0, 0)
        self.write(f"YOU WON", move=False, align="center", font=("Arial", 20, "bold"))

    def lose(self):
        self.goto(0, 0)
        self.write(f"YOU LOST", move=False, align="center", font=("Arial", 20, "bold"))
