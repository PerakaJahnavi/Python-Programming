from turtle import Screen
from barrier import Barrier
from invaders import Invaders
from scoreboard import ScoreBoard
from player import Player
from bullets import Bullet
from anime import Animate
import time
import random

screen = Screen()
screen.title("Space Invaders Game")
screen.setup(height=700, width=800)
screen.bgcolor("#000000")
screen.tracer(0)
game_speed = 0.1

barrier = Barrier()
player = Player()
bullet = Bullet(game_speed)
invaders = Invaders()
scoreboard = ScoreBoard()
anime_player = Animate(game_speed, [player])
anime_aliens = Animate(game_speed, invaders.all_invaders)

screen.listen()
screen.onkey(player.go_right, "Right")
screen.onkey(player.go_left, "Left")
screen.onkey(bullet.create_player_bullet, key="Up")

game_is_on = True
while game_is_on:
    time.sleep(game_speed)
    bullet.player_xcor = player.xcor()
    attacker = random.choice(invaders.all_invaders)
    bullet.create_aliens_bullet(attacker.xcor(), attacker.ycor())
    bullet.move_all_bullets()
    anime_aliens.move_inplace()
    anime_player.move_inplace()
    anime_aliens.move_sides()
    # DETECT collisions
    for enemy in invaders.all_invaders:
        for player_bullet in bullet.all_player_bullets:
            # collision with player bullets
            if player_bullet.distance(enemy) < 30:
                invaders.destroy(enemy)
                bullet.destroy_player_bullet(player_bullet)
                scoreboard.increase_score()

        for enemy_bullet in bullet.all_aliens_bullets:
            # collision with enemy bullets
            if enemy_bullet.distance(player) < 40:
                scoreboard.reduce_lives()
                bullet.destroy_all_bullets()
                player.revive()

    barrier.destroy_barrier(bullet.all_player_bullets, bullet.all_aliens_bullets)
    # if players lives all lost
    if scoreboard.lives == 0:
        game_is_on = False
        scoreboard.lose()

    # if players hit all the aliens
    if scoreboard.score >= 3600:
        game_is_on = False
        scoreboard.win()
    screen.update()

screen.exitonclick()
