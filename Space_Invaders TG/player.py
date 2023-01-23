from turtle import Turtle


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.screen.register_shape("player.gif")
        self.shape("player.gif")
        self.penup()
        self.goto(0, -280)

    def go_right(self):
        if self.xcor() < 350:
            new_x = self.xcor() + 25
            self.goto(new_x, self.ycor())

    def go_left(self):
        if self.xcor() > -350:
            new_x = self.xcor() - 25
            self.goto(new_x, self.ycor())

    def revive(self):
        self.goto(0, -280)


