from pico2d import *

import boss_stage
import farming_stage
import game_framework
import game_world
import lab_mode
import armory_mode
import stage1
import stage2
import userdata
from button import Button
from game_framework import change_mode
from info_font import InfoFont

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.pop_mode()

def init():
    global image
    image = load_image('resources/background/guide_cockpit.png')


def update():
    game_world.update()

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)

    game_world.render()
    update_canvas()

def finish():
    global image
    del image

def pause(): pass
def resume(): pass
