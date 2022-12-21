from turtle import Turtle


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.move_speed = 0.1
        self.x_move = 10
        self.y_move = 10
        self.penup()

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1
        self.move_speed *= 1

    def stop_ball_move(self, ball):
        if ball.ycor() < -160:
            self.goto(0, 0)
            self.pencolor('#fff')
            self.write("GAME OVER", align="center", font=("Arial", 30, "bold"))
            return True