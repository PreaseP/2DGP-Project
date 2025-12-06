# python
# file: 'lab_mode.py'

from pico2d import *

import cockpit_mode
import game_framework
import lab_guide
import userdata
import common

from button import Button

# -------------------- 레이아웃 상수/헬퍼 --------------------
SCREEN_W, SCREEN_H = 1280, 720
CX, CY = SCREEN_W // 2, SCREEN_H // 2

SLOT_SIZE = 120  # 슬롯(정사각형) 한 변 픽셀
GAP_V = 160      # 세로 간격
GAP_C = 160      # 가운데 열 가로 간격

def make_slot_button(cx, cy, size, tag):
    half = size // 2
    return Button(cx - half, cy - half, cx + half, cy + half, tag)

# -------------------- 리소스/상태 --------------------
image = None
popup = None
font = None
swordSkill = None
gunSkill = None
generalSkill = None

# 클릭 판정용(다른 버튼들과 함께 사용)
buttonList = []
# 스킬 슬롯: (Button, skill_type, skill_id)
skill_buttons = []

def draw_skill(button, skill_type, skill_id):
    global swordSkill, gunSkill, generalSkill, font
    x = (button.left + button.right) // 2
    y = (button.bottom + button.top) // 2

    # 모든 스킬 아이콘을 SLOT_SIZE 크기로 그립니다.
    if skill_type == 'sword':
        swordSkill[skill_id].draw(x, y, SLOT_SIZE, SLOT_SIZE)
    elif skill_type == 'gun':
        gunSkill[skill_id].draw(x, y, SLOT_SIZE, SLOT_SIZE)
    elif skill_type == 'general':
        generalSkill[skill_id].draw(x, y, SLOT_SIZE, SLOT_SIZE)

    font.draw(button.left, button.bottom - 30,
              f"Lv. {userdata.playerSkill[skill_type][skill_id]}",
              (200, 150, 150))

def init():
    global image, popup, font, big_font, swordSkill, gunSkill, generalSkill, skill_buttons, buttonList

    image = load_image('resources/background/lab.png')
    popup = load_image('resources/background/ship_popup.png')
    font = load_font('resources/DungGeunMo.TTF', 30)
    big_font = load_font('resources/DungGeunMo.TTF', 40)

    if swordSkill is None:
        swordSkill = [load_image(f"resources/sprites/sword_skill{i}.png") for i in range(1, 3)]
    if gunSkill is None:
        gunSkill = [load_image(f"resources/sprites/gun_skill{i}.png") for i in range(1, 3)]
    if generalSkill is None:
        generalSkill = [load_image(f"resources/sprites/general_skill{i}.png") for i in range(1, 4)]

    # ---- 슬롯 좌표 배치 ----
    x_left = CX - 350
    x_right = CX + 350
    x_center_l = CX - GAP_C // 1  # 가운데 왼쪽
    x_center_r = CX + GAP_C // 1  # 가운데 오른쪽
    x_center_m = CX               # 가운데 아래

    y_mid = CY
    y_bottom = CY - GAP_V
    y_top_center = CY + 100       # 가운데 윗줄 높이

    skill_buttons = [
        # 왼쪽: sword (위, 아래)
        (make_slot_button(x_left,  y_mid,    SLOT_SIZE, 'sword_0'),   'sword',   0),
        (make_slot_button(x_left,  y_bottom, SLOT_SIZE, 'sword_1'),   'sword',   1),

        # 가운데: general (좌상, 우상, 중앙하)
        (make_slot_button(x_center_l, y_top_center, SLOT_SIZE, 'general_0'), 'general', 0),
        (make_slot_button(x_center_r, y_top_center, SLOT_SIZE, 'general_1'), 'general', 1),
        (make_slot_button(x_center_m, y_mid - 20,   SLOT_SIZE, 'general_2'), 'general', 2),

        # 오른쪽: gun (위, 아래)
        (make_slot_button(x_right, y_mid,    SLOT_SIZE, 'gun_0'),     'gun',     0),
        (make_slot_button(x_right, y_bottom, SLOT_SIZE, 'gun_1'),     'gun',     1),
    ]

    # 클릭 판정 리스트에 등록
    buttonList = [b for (b, _, _) in skill_buttons]

    if not common.playing:
        common.main_bgm = load_music('resources/sound/main.mp3')
        common.main_bgm.set_volume(32)
        common.main_bgm.repeat_play()
        common.playing = True

    if not userdata.guide['lab']:
        userdata.guide['lab'] = True
        game_framework.push_mode(lab_guide)

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            game_framework.change_mode(cockpit_mode)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx, my = event.x, SCREEN_H - event.y
            # 슬롯 클릭 판정
            for b, stype, sid in skill_buttons:
                if b.left <= mx <= b.right and b.bottom <= my <= b.top:
                    userdata.add_skill(stype, sid)
                    pass
        elif event.type == SDL_MOUSEWHEEL:
            if event.y < 0:
                game_framework.change_mode(cockpit_mode)

def update():
    pass

def draw():
    clear_canvas()
    image.draw(CX, CY, SCREEN_W, SCREEN_H)
    popup.draw(CX, CY, 1120, 630)

    # 스킬 아이콘 그리기
    for b, stype, sid in skill_buttons:
        draw_skill(b, stype, sid)

    big_font.draw(640 - 150, 360 + 250, f"Skill Point: {userdata.playerSkillPoint}", (255, 255, 0))

    update_canvas()

def finish():
    global image
    del image

def pause(): pass
def resume(): pass
