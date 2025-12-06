from pico2d import *

import boss_stage
import farming_stage
import game_framework
import game_world
import lab_mode
import armory_mode
import stage1
import stage2
import title_mode
import userdata
from button import Button
from game_framework import change_mode
from info_font import InfoFont

ending_set = {1 : 3, 2 : 5, 3 : 5}

def handle_events():
    global idx, max_idx

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if idx == max_idx - 1:
                change_mode(title_mode)
            idx += 1

def init():
    ending_num = userdata.relics['relic1'] + userdata.relics['relic2'] - 1


    global image, idx, max_idx
    idx = 0
    max_idx = ending_set[ending_num]
    image = {}
    for i in range(ending_set[ending_num]):
        image[i] = load_image(f'resources/background/end{ending_num}_{i + 1}.png')


def update():
    game_world.update()

def draw():
    global idx

    clear_canvas()
    image[idx].draw(640, 360, 1280, 720)

    game_world.render()
    update_canvas()

def finish():
    global image
    del image

def pause(): pass
def resume(): pass
