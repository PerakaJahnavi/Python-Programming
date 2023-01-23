from turtle import Turtle

INVADER_PIC = "Alien.gif"
MOVEMENT_TIME = 0.5
MOVEMENT_DISTANCE = 1


class Invaders(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.all_invaders = []
        self.screen.register_shape(INVADER_PIC)
        self.create_invaders()

    def create_invaders(self):
        for row in range(4):
            for column in range(9):
                invader = Turtle(INVADER_PIC)
                invader.penup()
                invader.goto(column * 50 - 200, row * 50 + 100)
                self.all_invaders.append(invader)

    def destroy(self, invader):
        invader.hideturtle()
        self.all_invaders.remove(invader)