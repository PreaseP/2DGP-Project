from pico2d import *

import farming_stage
import game_framework
import lab_mode
import armory_mode

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            game_framework.change_mode(farming_stage)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            game_framework.change_mode(lab_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            game_framework.change_mode(armory_mode)

def init():
    global image, font
    image = load_image('resources/background/cockpit.png')
    font = load_font('resources/DungGeunMo.TTF', 50)

def update():
    pass

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)
    font.draw(350, 100, 'Press A to go farming', (255, 255, 255))
    update_canvas()


def finish():
    global image
    del image

def pause(): pass
def resume(): pass

