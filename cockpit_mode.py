from pico2d import *

import farming_stage
import game_framework
import lab_mode
import armory_mode
import userdata
from button import Button

buttonList = []

# 버튼 위치/크기 (화면 중앙)
farmingButton = Button(640 - 60, 160 - 60, 640 + 60, 160 + 60, 'farming')  # left, bottom, right, top, button_type
armorChoiceButton = Button(45 - 35, 45 - 35, 45 + 35, 45 + 35, 'armor_choice')

buttonList.append(farmingButton)
buttonList.append(armorChoiceButton)

FARMING_CENTER_X = 640
FARMING_CENTER_Y = 160
FARMING_W = 200
FARMING_H = 200

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            game_framework.change_mode(lab_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            game_framework.change_mode(armory_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            userdata.save_userdata()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
            userdata.load_userdata()
        # 마우스 버튼 처리
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx = event.x
            my = 720 - event.y  # pico2d는 원점이 아래이므로 y를 뒤집음
            for button in buttonList:
                if button.left <= mx <= button.right and button.bottom <= my <= button.top:
                    if button.button_type == 'farming':
                        game_framework.change_mode(farming_stage)
                    elif button.button_type == 'armor_choice':
                        if userdata.playerType == 'S':
                            userdata.playerType = 'G'
                        else:
                            userdata.playerType = 'S'
        elif event.type == SDL_MOUSEWHEEL:
            if event.y >0:
                game_framework.change_mode(lab_mode)
            else:
                game_framework.change_mode(armory_mode)

def init():
    global image, font, popup, sword, gun, farming_star
    image = load_image('resources/background/cockpit.png')
    font = load_font('resources/DungGeunMo.TTF', 50)
    popup = load_image('resources/background/ship_popup.png')
    sword = load_image('resources/sprites/sword_icon.png')
    gun = load_image('resources/sprites/gun_icon.png')
    farming_star = load_image('resources/background/farming_stage.png')

def update():
    pass

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)
    popup.draw(640, 360, 1120, 660)

    farming_star.clip_draw(0, 0, farming_star.w, farming_star.h, FARMING_CENTER_X, FARMING_CENTER_Y, FARMING_W, FARMING_H)

    font.draw(FARMING_CENTER_X - 90, FARMING_CENTER_Y - 100, '파밍 맵', (255, 255, 255))
    if userdata.playerType == 'S':
        sword.clip_draw(0, 0, 24, 24, 45, 45, 75, 75)
    else:
        gun.clip_draw(0, 0, 24, 24, 45, 45, 75, 75)

    update_canvas()


def finish():
    global image
    del image

def pause(): pass
def resume(): pass
