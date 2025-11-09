from pico2d import *

import cockpit_mode
import game_framework

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            game_framework.change_mode(cockpit_mode)

def init():
    global image, font
    image = load_image('resources/background/lab.png')
    font = load_font('resources/DungGeunMo.TTF', 50)

def update():
    pass

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)
    # font.draw(400, 100, 'Press A to farming', (255, 255, 255))
    update_canvas()


def finish():
    global image
    del image

def pause(): pass
def resume(): pass

