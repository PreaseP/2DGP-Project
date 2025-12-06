from pico2d import *

import cockpit_mode
import game_framework
import game_world
import userdata
from button import Button
from game_framework import change_mode

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_mode(cockpit_mode)

def init():
    global font, popup, small_font, death_timer
    font = load_font('resources/DungGeunMo.TTF', 50)
    popup = load_image('resources/background/ship_popup.png')
    small_font = load_font('resources/DungGeunMo.TTF', 30)

    death_timer = 5.0

def update():
    global death_timer

    death_timer -= game_framework.frame_time
    if death_timer <= 0.0:
        finish()  # 게임 월드 초기화
        game_framework.change_mode(cockpit_mode)
        return

def draw():
    clear_canvas()
    game_world.render()
    popup.draw(640, 360, 1280, 720)

    font.draw(540, 400, 'GAME OVER', (255, 0, 0))
    small_font.draw(450, 300, '5초 후에 조종실로 돌아갑니다.', (255, 255, 255))

    update_canvas()


def finish():
    for layer in game_world.world:
        for o in layer:
            game_world.remove_collision_object(o)
    game_world.clear()

def pause(): pass
def resume(): pass
