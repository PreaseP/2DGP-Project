from pico2d import *

import cockpit_mode
import game_framework
import game_world
import userdata
from button import Button
import common

return_type = None

def handle_events():
    global return_type

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return_type = 0
            game_framework.change_mode(cockpit_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            return_type = 1
            game_framework.pop_mode()
        else:
            common.player.handle_event(event)

def init():
    global font, popup
    font = load_font('resources/DungGeunMo.TTF', 50)
    popup = load_image('resources/background/ship_popup.png')

def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    popup.draw(640, 360, 1280, 720)

    font.draw(390, 400, 'ESC를 눌러 조종실로 귀환', (255, 255, 255))
    font.draw(450, 300, 'SPACE를 눌러 재개', (255, 255, 255))

    update_canvas()


def finish():
    global return_type
    if return_type == 0:
        for layer in game_world.world:
            for o in layer:
                game_world.remove_collision_object(o)
        game_world.clear()
    else:
        pass

def pause(): pass
def resume(): pass
