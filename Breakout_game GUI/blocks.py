import random
import turtle
from turtle import Turtle
color_list = ['#7DE5ED', '#E14D2A', '#BA94D1', '#001253', '#D6E4E5', '#54B435', '#8B7E74', '#FF6464', '#A9AF7E', '#F49D1A']


class Blocks():
    def __init__(self):
        super().__init__()
        self.all_blocks = {}
        self.x = -230
        self.y = 230
        self.add_blocks = 9

    def blocks_block(self):
        for _ in range(6):
            while self.add_blocks:
                new_block = Turtle("square")
                new_block.color(color_list[self.add_blocks-1])
                new_block.shapesize(stretch_wid=0.5, stretch_len=2.5)
                new_block.penup()
                self.all_blocks[new_block] = (self.x, self.y)
                self.x += 55
                self.add_blocks -= 1
            self.y -= 13
            self.add_blocks = 9
            self.x = -230
        self.display_blocks()

    def display_blocks(self):
        for block in self.all_blocks:
            block.goto(self.all_blocks[block])

    def remove_block(self, ball):
        for block in self.all_blocks:
            if ball.distance(block) < 30:
                ball.bounce_y()
                self.all_blocks[block] = (500, 500)
        self.display_blocks()










