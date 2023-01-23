from turtle import Turtle


class Barrier():
    def __init__(self):
        self.all_blocks = {}
        self.play_p()
        self.play_l()
        self.play_a()
        self.play_y()

    def play_p(self):
        self.play_v(-355, -150, 10)
        self.play_h(-323, -5.5, 20)
        self.play_h(-323, -70, 20)
        self.play_v(-275.5, -53, 2)

    def play_l(self):
        self.play_v(-185, -150, 10)
        self.play_h(-153, -133.5, 20)

    def play_a(self):
        self.play_v(-15, -150, 10)
        self.play_h(17, -5, 20)
        self.play_h(17, -70, 20)
        self.play_v(97, -150, 10)

    def play_y(self):
        self.play_v(178, -70, 5)
        self.play_h(210, -70, 20)
        self.play_v(289.5, -70, 5)
        self.play_v(234, -150, 4)

    def play_v(self, x, y, j_turns):
        temp = y
        for i in range(8):
            for j in range(j_turns):
                tim = Turtle("square")
                tim.color("#B2B2B2")
                tim.shapesize(stretch_len=0.1, stretch_wid=0.7)
                tim.penup()
                tim.goto(x, y)
                self.all_blocks[tim] = (x, y)
                y += 16
            x += 4
            y = temp

    def play_h(self, x, y, j_turns):
        temp = x
        for i in range(2):
            for j in range(j_turns):
                tim = Turtle("square")
                tim.color("#B2B2B2")
                tim.shapesize(stretch_len=0.1, stretch_wid=0.7)
                tim.penup()
                tim.goto(x, y)
                self.all_blocks[tim] = (x, y)
                x += 4
            y -= 16
            x = temp

    def display_blocks(self):
        for block in self.all_blocks:
            block.goto(self.all_blocks[block])

    def destroy_barrier(self, player_bullets, alien_bullets):
        for block in self.all_blocks:
            for bullet in player_bullets:
                if bullet.distance(block) < 5:
                    self.all_blocks[block] = (1000, 1000)
            for bullet in alien_bullets:
                if bullet.distance(block) < 5:
                    self.all_blocks[block] = (1000, 1000)
        self.display_blocks()


