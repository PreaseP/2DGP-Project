from pico2d import *

import farming_stage
import game_framework
import lab_mode
import armory_mode
import userdata
from button import Button

buttonList = []

# 버튼 위치/크기 (화면 중앙)
farmingButton = Button(640 - 175, 160 - 40, 640 + 175, 160 + 40, 'farming')  # left, bottom, right, top, button_type
armorChoiceButton = Button(45 - 35, 45 - 35, 45 + 35, 45 + 35, 'armor_choice')

buttonList.append(farmingButton)
buttonList.append(armorChoiceButton)

FARMING_CENTER_X = 640
FARMING_CENTER_Y = 160
FARMING_W = 350
FARMING_H = 80

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
    global image, font, sword, gun
    image = load_image('resources/background/cockpit.png')
    font = load_font('resources/DungGeunMo.TTF', 50)
    sword = load_image('resources/sprites/sword_icon.png')
    gun = load_image('resources/sprites/gun_icon.png')

def update():
    pass

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)
    buttonList[0].fill_draw()

    font.draw(FARMING_CENTER_X - 160, FARMING_CENTER_Y, 'Farming Stage', (0, 0, 0))
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
