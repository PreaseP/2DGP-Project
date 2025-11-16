from pico2d import *

import farming_stage
import game_framework
import lab_mode
import armory_mode

# 버튼 위치/크기 (화면 중앙)
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
        # 마우스 버튼 처리
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx = event.x
            my = 720 - event.y  # pico2d는 원점이 아래이므로 y를 뒤집음
            left = FARMING_CENTER_X - FARMING_W // 2
            right = FARMING_CENTER_X + FARMING_W // 2
            bottom = FARMING_CENTER_Y - FARMING_H // 2
            top = FARMING_CENTER_Y + FARMING_H // 2
            if left <= mx <= right and bottom <= my <= top:
                game_framework.change_mode(farming_stage)

def init():
    global image, font
    image = load_image('resources/background/cockpit.png')
    font = load_font('resources/DungGeunMo.TTF', 50)

def update():
    pass

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)

    # 버튼 그리기 (테두리 + 텍스트)
    left = FARMING_CENTER_X - FARMING_W // 2
    right = FARMING_CENTER_X + FARMING_W // 2
    bottom = FARMING_CENTER_Y - FARMING_H // 2
    top = FARMING_CENTER_Y + FARMING_H // 2

    # 버튼 테두리
    draw_rectangle(left, bottom, right, top)

    # 버튼 라벨 (중앙 정렬 수동)
    text = 'Farming Stage'
    font.draw(FARMING_CENTER_X - 160, FARMING_CENTER_Y, text, (255, 255, 255))

    update_canvas()


def finish():
    global image
    del image

def pause(): pass
def resume(): pass

