import random
from pico2d import *

from player import Player
from slime import Slime
import game_framework
import game_world

spawn_timer = 0.0

player = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

def init():
    global map
    map = load_image('resources/background/farming.png')

    global spawn_timer
    spawn_timer = 0.0

    global player
    player = Player()
    player.xdir = -1
    game_world.add_object(player, 1)

    slimes = [Slime() for _ in range(10)]
    for slime in slimes:
        game_world.add_collision_pair('sword:monster', None, slime)
    game_world.add_objects(slimes, 1)

def update():
    global spawn_timer

    spawn_timer += game_framework.frame_time

    if spawn_timer >= 10.0:
        slime = Slime()
        game_world.add_object(slime, 1)
        game_world.add_collision_pair('sword:monster', None, slime)
        spawn_timer = 0.0

    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    map.draw(640, 360, 1280, 720)
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

