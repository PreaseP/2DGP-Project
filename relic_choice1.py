from pico2d import *

import cockpit_mode
import game_framework
from button import Button
import userdata

font = None

buttonList = []

# 버튼 위치/크기 (화면 중앙)
destroyButton = Button(640 + 350 - 130, 360 - 60 - 160 , 640 + 350 + 130, 360 + 60 - 160, 'destroy')  # left, bottom, right, top, button_type
absorbButton = Button(640 - 350 - 130, 360 - 60 - 160 , 640 - 350 + 130, 360 + 60 - 160, 'absorb')

buttonList.append(destroyButton)
buttonList.append(absorbButton)

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx = event.x
            my = 720 - event.y  # pico2d는 원점이 아래이므로 y를 뒤집음
            for button in buttonList:
                if button.left <= mx <= button.right and button.bottom <= my <= button.top:
                    if button.button_type == 'destroy':
                        userdata.relics['relic1'] = 1 # 파괴 선택
                        game_framework.change_mode(cockpit_mode)
                    elif button.button_type == 'absorb':
                        userdata.relics['relic1'] = 2 # 흡수 선택
                        game_framework.change_mode(cockpit_mode)


def init():
    global image, font, big_font
    image = load_image('resources/background/relic1_choice_screen.png')
    font = load_font('resources/DungGeunMo.TTF', 30)
    big_font = load_font('resources/DungGeunMo.TTF', 40)

def update():
    pass

def draw():
    global swordImage, gunImage
    clear_canvas()
    image.draw(640, 360, 1280, 720)

    big_font.draw(640 - 350 - 90, 360 - 150, "파괴한다", (255, 255, 255))
    big_font.draw(640 + 350 - 90, 360 - 150, "흡수한다", (255, 255, 255))

    update_canvas()


def finish():
    global image
    del image

def pause(): pass
def resume(): pass

