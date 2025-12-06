from pico2d import *

import boss_stage
import cockpit_guide
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

buttonList = []

# 버튼 위치/크기 (화면 중앙)
farmingButton = Button(640 - 60, 160 - 60, 640 + 60, 160 + 60, 'farming')  # left, bottom, right, top, button_type
stageButton = Button(640 - 100, 160 + 250, 640 + 100, 160 + 450, 'stage_select')
armorChoiceButton = Button(45 - 35, 45 - 35, 45 + 35, 45 + 35, 'armor_choice')

buttonList.append(farmingButton)
buttonList.append(stageButton)
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
            info = InfoFont(1280 - 220, 50, '저장 성공')
            game_world.add_object(info)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
            userdata.load_userdata()
            info = InfoFont(1280 - 280, 50, '불러오기 성공')
            game_world.add_object(info)
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
                    elif button.button_type == 'stage_select':
                        if userdata.stageClear == 0:
                            change_mode(stage1)
                        elif userdata.stageClear == 1:
                            change_mode(stage2)
                        elif userdata.stageClear == 2:
                            change_mode(boss_stage)
        elif event.type == SDL_MOUSEWHEEL:
            if event.y >0:
                game_framework.change_mode(lab_mode)
            else:
                game_framework.change_mode(armory_mode)

def init():
    global image, font, popup, sword, gun, farming_star, stage_star
    image = load_image('resources/background/cockpit.png')
    font = load_font('resources/DungGeunMo.TTF', 50)
    popup = load_image('resources/background/ship_popup.png')
    sword = load_image('resources/sprites/sword_icon.png')
    gun = load_image('resources/sprites/gun_icon.png')
    farming_star = load_image('resources/background/farming_stage.png')
    stage_star = load_image('resources/background/stage' + str(userdata.stageClear + 1) + '_star.png')

    if not userdata.guide['cockpit']:
        userdata.guide['cockpit'] = True
        game_framework.push_mode(cockpit_guide)

def update():
    game_world.update()

def draw():
    clear_canvas()
    image.draw(640, 360, 1280, 720)
    popup.draw(640, 360, 1120, 660)

    farming_star.clip_draw(0, 0, farming_star.w, farming_star.h, FARMING_CENTER_X, FARMING_CENTER_Y, FARMING_W, FARMING_H)

    font.draw(FARMING_CENTER_X - 90, FARMING_CENTER_Y - 100, '파밍 맵', (255, 255, 255))

    stage_star.clip_draw(0, 0, stage_star.w, stage_star.h, FARMING_CENTER_X, FARMING_CENTER_Y + 350, FARMING_W, FARMING_H)

    if userdata.stageClear == 0:
        font.draw(FARMING_CENTER_X - 120, FARMING_CENTER_Y + 200, '스테이지 1', (255, 255, 255))
    elif userdata.stageClear == 1:
        font.draw(FARMING_CENTER_X - 120, FARMING_CENTER_Y + 200, '스테이지 2', (255, 255, 255))
    elif userdata.stageClear == 2:
        font.draw(FARMING_CENTER_X - 150, FARMING_CENTER_Y + 200, '보스 스테이지', (255, 255, 255))

    if userdata.playerType == 'S':
        sword.clip_draw(0, 0, 24, 24, 45, 45, 75, 75)
    else:
        gun.clip_draw(0, 0, 24, 24, 45, 45, 75, 75)

    game_world.render()
    update_canvas()


def finish():
    global image
    del image

def pause(): pass
def resume(): pass
