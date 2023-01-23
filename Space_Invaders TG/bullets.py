from turtle import Turtle
from random import randint
SHOOTING_GAP = 0.8


class Bullet(Turtle):
    def __init__(self, move_speed):
        super().__init__()
        self.hideturtle()
        self.all_player_bullets = []
        self.all_aliens_bullets = []
        self.player_xcor = 0
        self.player_ycor = -250
        self.shooting_elapsed_time = 0
        self.move_speed = move_speed

    def create_player_bullet(self):
        if self.shooting_elapsed_time > SHOOTING_GAP:
            bullet = Turtle("circle")
            bullet.speed(self.move_speed)
            bullet.penup()
            bullet.shapesize(stretch_len=0.3, stretch_wid=0.3)
            bullet.color("green")
            bullet.goto(self.player_xcor, self.player_ycor)
            self.all_player_bullets.append(bullet)
            self.shooting_elapsed_time = 0

    def create_aliens_bullet(self, xcor, ycor):
        if randint(0, 10) == 5:
            enemy_bullet = Turtle("circle")
            enemy_bullet.speed(self.move_speed)
            enemy_bullet.penup()
            enemy_bullet.shapesize(stretch_len=0.3, stretch_wid=0.3)
            enemy_bullet.color("red")
            enemy_bullet.goto(xcor, ycor)
            self.all_aliens_bullets.append(enemy_bullet)

    def move_all_bullets(self):
        self.shooting_elapsed_time += self.move_speed
        for bullet in self.all_player_bullets:
            new_y = bullet.ycor() + 20
            bullet.goto(bullet.xcor(), new_y)
            if bullet.ycor() > 350:
                bullet.hideturtle()
                self.all_player_bullets.remove(bullet)

        for enemy_bullet in self.all_aliens_bullets:
            new_y = enemy_bullet.ycor() - 20
            enemy_bullet.goto(enemy_bullet.xcor(), new_y)
            if enemy_bullet.ycor() < -350:
                enemy_bullet.hideturtle()
                self.all_aliens_bullets.remove(enemy_bullet)

    def destroy_all_bullets(self):
        for bullet in self.all_aliens_bullets:
            bullet.hideturtle()

        for bullet in self.all_player_bullets:
            bullet.hideturtle()

        self.all_aliens_bullets.clear()
        self.all_player_bullets.clear()

    def destroy_player_bullet(self, player_bullet):
        player_bullet.hideturtle()
        self.all_player_bullets.remove(player_bullet)
