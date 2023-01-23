MOVEMENT_TIME = 0.5
MOVEMENT_TIME_SIDES = 5
MOVEMENT_DISTANCE = 3


class Animate():
    def __init__(self, move_speed, objects):
        self.all_objects = objects
        self.elapsed_time = 0
        self.elapsed_time_sides = 0
        self.move_speed = move_speed

    def move_inplace(self):
        self.elapsed_time += self.move_speed
        if self.elapsed_time <= MOVEMENT_TIME:
            self.move_up()
        elif self.elapsed_time <= MOVEMENT_TIME * 2:
            self.move_down()
        else:
            self.elapsed_time = 0

    def move_up(self):
        for item in self.all_objects:
            up_y = item.ycor() + MOVEMENT_DISTANCE
            item.goto(item.xcor(), up_y)

    def move_down(self):
        for item in self.all_objects:
            down_y = item.ycor() - MOVEMENT_DISTANCE
            item.goto(item.xcor(), down_y)

    def move_sides(self):
        self.elapsed_time_sides += self.move_speed
        if self.elapsed_time_sides <= MOVEMENT_TIME_SIDES:
            self.move_right()
        elif self.elapsed_time_sides <= MOVEMENT_TIME_SIDES * 3:
            self.move_left()
        elif self.elapsed_time_sides <= MOVEMENT_TIME_SIDES * 4:
            self.move_right()
        else:
            print("reset")
            self.elapsed_time_sides = 0

    def move_right(self):
        for item in self.all_objects:
            right_x = item.xcor() + MOVEMENT_DISTANCE
            item.goto(right_x, item.ycor())

    def move_left(self):
        for item in self.all_objects:
            left_x = item.xcor() - MOVEMENT_DISTANCE
            item.goto(left_x, item.ycor())
