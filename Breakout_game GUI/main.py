import turtle
from turtle import Screen
from paddle import Paddle
from blocks import Blocks
from ball import Ball
import time

screen = Screen()
screen.title("Breakout Game")
screen.setup(height=500, width=600)
screen.bgcolor("#404258")
screen.tracer(0)

paddle = Paddle((0, -150))

screen.listen()
screen.onkey(paddle.go_right, "Right")
screen.onkey(paddle.go_left, "Left")


ball = Ball()
game_on = True

blocks = Blocks()
blocks.blocks_block()

while game_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detect collision with up and down
    if paddle.distance(ball) < 30 or ball.ycor() > 230 or ball.ycor() < -230:
        ball.bounce_y()

    # Detect collision with left and right
    if ball.xcor() > 280 or ball.xcor() < -280:
        ball.bounce_x()

    blocks.remove_block(ball)
    if ball.stop_ball_move(ball):
        game_on = False
screen.exitonclick()
