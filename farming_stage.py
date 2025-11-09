import random
from pico2d import *

import game_framework
import game_world

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def init():
    global map
    map = load_image('resources/background/farming.png')

def update():
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

