from pico2d import *

import armory_guide
import cockpit_mode
import game_framework
from button import Button
import userdata
import common

swordImage = None
gunImage = None
image = None
popup = None
font = None

buttonList = []

# 버튼 위치/크기 (화면 중앙)
makeGunButton = Button(640 + 350 - 130, 360 - 60 - 160 , 640 + 350 + 130, 360 + 60 - 160, 'make_gun')  # left, bottom, right, top, button_type
makeSwordButton = Button(640 - 350 - 130, 360 - 60 - 160 , 640 - 350 + 130, 360 + 60 - 160, 'make_sword')
upgradeGunButton = Button(640 + 350 - 130, 360 - 60 , 640 + 350 + 130, 360 + 60, 'upgrade_gun')
upgradeSwordButton = Button(640 - 350 - 130, 360 - 60 , 640 - 350 + 130, 360 + 60, 'upgrade_sword')

buttonList.append(makeGunButton)
buttonList.append(makeSwordButton)
buttonList.append(upgradeGunButton)
buttonList.append(upgradeSwordButton)

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP:
            game_framework.change_mode(cockpit_mode)
            # 마우스 버튼 처리
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx = event.x
            my = 720 - event.y  # pico2d는 원점이 아래이므로 y를 뒤집음
            for button in buttonList:
                if button.left <= mx <= button.right and button.bottom <= my <= button.top:
                    if button.button_type == 'make_gun':
                        if userdata.spend_gold(userdata.makeCost):
                            userdata.make_weapon('gun')
                    elif button.button_type == 'make_sword':
                        if userdata.spend_gold(userdata.makeCost):
                            userdata.make_weapon('sword')
                    elif button.button_type == 'upgrade_gun':
                        if userdata.playerWeapon['gun'][1] < 5 and userdata.spend_gold(userdata.upgradeCost[userdata.playerWeapon['gun'][1]]):
                            userdata.upgrade_weapon('gun')
                    elif button.button_type == 'upgrade_sword':
                        if userdata.playerWeapon['sword'][1] < 5 and userdata.spend_gold(userdata.upgradeCost[userdata.playerWeapon['sword'][1]]):
                            userdata.upgrade_weapon('sword')
        elif event.type == SDL_MOUSEWHEEL:
            if event.y >0:
                game_framework.change_mode(cockpit_mode)


def init():
    global image, popup, font, big_font, swordImage, gunImage
    image = load_image('resources/background/armory.png')
    popup = load_image('resources/background/ship_popup.png')
    font = load_font('resources/DungGeunMo.TTF', 30)
    big_font = load_font('resources/DungGeunMo.TTF', 40)

    if swordImage is None:
        swordImage = [load_image(f"resources/sprites/sword_{i}.png") for i in range(1, 4)]
    if gunImage is None:
        gunImage = [load_image(f"resources/sprites/gun_{i}.png") for i in range(1, 4)]

    if not common.playing:
        common.main_bgm = load_music('resources/sound/main.mp3')
        common.main_bgm.set_volume(32)
        common.main_bgm.repeat_play()
        common.playing = True

    if not userdata.guide['armory']:
        userdata.guide['armory'] = True
        game_framework.push_mode(armory_guide)

def update():
    pass

def draw():
    global swordImage, gunImage
    clear_canvas()
    image.draw(640, 360, 1280, 720)
    popup.draw(640, 360, 1120, 630)
    swordImage[userdata.playerWeapon['sword'][0]].clip_draw(0, 0, 100, 100, 640 - 350 , 720 - 150)
    gunImage[userdata.playerWeapon['gun'][0]].clip_draw(0, 0, 100, 100, 640 + 350, 720 - 150)

    for button in buttonList:
        button.fill_draw()

    big_font.draw(640 - 70, 360 + 200, f"Gold: {userdata.playerGold}", (255, 255, 0))

    font.draw(640 - 350 - 30, 720 - 250, f"+{userdata.playerWeapon['sword'][1]}", (160, 160, 255))
    font.draw(640 + 350 - 30, 720 - 250, f"+{userdata.playerWeapon['gun'][1]}", (255, 160, 160))

    #버튼의 위치에 맞춰 업그레이드/제작 비용 그리기
    if userdata.playerWeapon['sword'][0] < 2:
        big_font.draw(640 - 350 - 90, 360 - 140, "무기 연성", (0, 0, 0))
        font.draw(640 - 350 - 30, 360 - 180, str(userdata.makeCost), (160, 160, 0))
    else:
        big_font.draw(640 - 350 - 90, 360 - 150, "Max Grade", (0, 0, 0))
    if userdata.playerWeapon['gun'][0] < 2:
        big_font.draw(640 + 350 - 90, 360 - 140, "무기 연성", (0, 0, 0))
        font.draw(640 + 350 - 30, 360 - 180, str(userdata.makeCost), (160, 160, 0))
    else:
        big_font.draw(640 + 350 - 90, 360 - 150, "Max Grade", (0, 0, 0))

    if userdata.playerWeapon['sword'][1] < 5:
        big_font.draw(640 - 350 - 90, 360 + 20, f"무기 강화", (0, 0, 0))
        font.draw(640 - 350 - 30, 360 - 30, str(userdata.upgradeCost[userdata.playerWeapon['sword'][1]]), (160, 160, 0))
    else:
        big_font.draw(640 - 350 - 90, 360, "Max Level", (0, 0, 0))
    if userdata.playerWeapon['gun'][1] < 5:
        big_font.draw(640 + 350 - 90, 360 + 20, f"무기 강화", (0, 0, 0))
        font.draw(640 + 350 - 30, 360 - 30, str(userdata.upgradeCost[userdata.playerWeapon['gun'][1]]), (160, 160, 0))
    else:
        big_font.draw(640 + 350 - 90, 360, "Max Level", (0, 0, 0))


    update_canvas()


def finish():
    global image
    del image

def pause(): pass
def resume(): pass

