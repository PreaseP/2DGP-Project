from pico2d import load_image, load_font, draw_rectangle, get_canvas_width, get_canvas_height, clamp
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT, \
    SDL_BUTTON_RIGHT, SDLK_LSHIFT
from sdl2 import SDLK_w, SDLK_a, SDLK_s, SDLK_d

import game_world
import game_framework
import userdata
import common

from state_machine import StateMachine
from sword_effect import SwordEffect
from whirlwind import Whirlwind
from sword_laser import sLaser
from slam import Slam
from clone import sClone
from sword_dash import DashEffect

def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def mouse_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN

def mouse_release(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONUP

def event_stop(e):
    return e[0] == 'STOP'

def event_skill2(e):
    return e[0] == 'SKILL2'

def event_skill3(e):
    return e[0] == 'SKILL3'

def event_dash(e):
    return e[0] == 'DASH'

def event_run(e):
    return e[0] == 'RUN'

def event_attack(e):
    return e[0] == 'ATTACK'

# Player의 Run Speed 계산

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 * (userdata.playerSkill['general'][2] * 0.1 + 1.0)  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Move Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# Player attack Action Speed
TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 7

# Player Dash Action Speed
DASH_AMOUNT = 7.0 * PIXEL_PER_METER
TIME_PER_DASH = 0.5
DASH_PER_TIME = 1.0 / TIME_PER_DASH
FRAMES_PER_DASH = 8

# Player Skill2 Action Speed
TIME_PER_SKILL2 = 0.5
SKILL2_PER_TIME = 1.0 / TIME_PER_SKILL2
FRAMES_PER_SKILL2 = 9

# Player Skill3 Action Speed
TIME_PER_SKILL3 = 0.5
SKILL3_PER_TIME = 1.0 / TIME_PER_SKILL3
FRAMES_PER_SKILL3 = 11

class Idle:

    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if event_stop(e):
            self.player.face_dir = e[1]  # 이전 방향 유지

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        sx = self.player.x - common.map.window_left  # 화면상의 x 위치
        sy = self.player.y - common.map.window_bottom

        if self.player.face_dir == 1: # right
            self.player.image.clip_composite_draw(0, 35, 33, 22,
                                            0, ' ', sx + 15, sy, 75, 75)
        else: # face_dir == -1: # left
            self.player.image.clip_composite_draw(0, 35, 33, 22,
                                                  0, 'h', sx - 15, sy, 75, 75)

run_sprites = [
    (0, 0, 31), (32, 0, 31), (64, 0, 31), (96, 0, 31),
    (128, 0, 31), (160, 0, 31), (192, 0, 31), (224, 0, 31)
]


class Run:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0
        # 키 입력에 따라 방향 설정
        if self.player.xdir != 0:
            self.player.face_dir = self.player.xdir

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.player.x += self.player.xdir * RUN_SPEED_PPS * game_framework.frame_time * self.player.speed
        self.player.y += self.player.ydir * RUN_SPEED_PPS * game_framework.frame_time * self.player.speed
        if self.player.xdir != 0:
            self.player.face_dir = self.player.xdir

    def draw(self):
        sx = self.player.x - common.map.window_left
        sy = self.player.y - common.map.window_bottom

        if self.player.xdir == 0:
            if self.player.face_dir == 1:
                self.player.image.clip_composite_draw(
                    run_sprites[int(self.player.frame)][0],
                    run_sprites[int(self.player.frame)][1],
                    run_sprites[int(self.player.frame)][2], 22,
                    0, ' ', sx - 15, sy, 75, 75)
            else:
                self.player.image.clip_composite_draw(
                    run_sprites[int(self.player.frame)][0],
                    run_sprites[int(self.player.frame)][1],
                    run_sprites[int(self.player.frame)][2], 22,
                    0, 'h', sx + 15, sy, 75, 75)
        elif self.player.xdir == 1:
            self.player.image.clip_composite_draw(
                run_sprites[int(self.player.frame)][0],
                run_sprites[int(self.player.frame)][1],
                run_sprites[int(self.player.frame)][2], 22,
                0, ' ', sx - 15, sy, 75, 75)
        else:
            self.player.image.clip_composite_draw(
                run_sprites[int(self.player.frame)][0],
                run_sprites[int(self.player.frame)][1],
                run_sprites[int(self.player.frame)][2], 22,
                0, 'h', sx + 15, sy, 75, 75)


attack_sprites = [
    (0, 0, 62), (63, 0, 62), (126, 0, 62), (189, 0, 62),
    (252, 0, 62), (315, 0, 62), (378, 0, 62)
]

class Attack:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0  # 공격 프레임 초기화
        if self.player.skill1_cnt > 0:
            self.player.skill1_cnt -= 1
            effect = SwordEffect(self.player.x + self.player.xdir * 80, self.player.y, self.player.face_dir, self.player.xdir, self.player.atk * 1.5)
        else:
            effect = SwordEffect(self.player.x + self.player.xdir * 80, self.player.y, self.player.face_dir, self.player.xdir, self.player.atk)

        game_world.add_object(effect, 1)
        game_world.add_collision_pair('nonBullet:monster', effect, None)

    def exit(self, e):
        pass

    def do(self):
        # 공격 애니메이션 프레임 업데이트
        self.player.frame = (self.player.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time)
        self.player.x += self.player.xdir * RUN_SPEED_PPS * game_framework.frame_time * self.player.speed
        self.player.y += self.player.ydir * RUN_SPEED_PPS * game_framework.frame_time * self.player.speed
        # 공격 애니메이션이 끝나면 상태 전환

        if self.player.xdir != 0:
            self.player.face_dir = self.player.xdir

        if self.player.frame >= FRAMES_PER_ATTACK:
            if self.player.attacking:
              self.player.frame = 0

              if self.player.skill1_cnt > 0:
                  self.player.skill1_cnt -= 1
                  effect = SwordEffect(self.player.x + self.player.xdir * 80, self.player.y, self.player.face_dir,
                                       self.player.xdir, self.player.atk * 1.5)
              else:
                  effect = SwordEffect(self.player.x + self.player.xdir * 80, self.player.y, self.player.face_dir,
                                       self.player.xdir, self.player.atk)

              game_world.add_object(effect, 1)
              game_world.add_collision_pair('nonBullet:monster', effect, None)
            elif self.player.xdir == 0 and self.player.ydir == 0:
                self.player.state_machine.cur_state = self.player.IDLE
            else:
                self.player.state_machine.cur_state = self.player.RUN

    def draw(self):
        sx = self.player.x - common.map.window_left  # 화면상의 x 위치
        sy = self.player.y - common.map.window_bottom

        if self.player.xdir == 0:
            if self.player.face_dir == 1:  # right
                self.player.attack.clip_composite_draw(attack_sprites[int(self.player.frame)][0], attack_sprites[int(self.player.frame)][1],
                                                       attack_sprites[int(self.player.frame)][2], 31, 0, ' ', sx + 30, sy + 15, 150, 100)
            else:  # face_dir == -1: # left
                self.player.attack.clip_composite_draw(attack_sprites[int(self.player.frame)][0], attack_sprites[int(self.player.frame)][1],
                                                       attack_sprites[int(self.player.frame)][2], 31, 0, 'h', sx - 30, sy + 15, 150, 100)
        elif self.player.xdir == 1:
            self.player.attack.clip_composite_draw(attack_sprites[int(self.player.frame)][0],
                                                   attack_sprites[int(self.player.frame)][1],
                                                   attack_sprites[int(self.player.frame)][2], 31, 0, ' ',
                                                   sx + 30, sy + 15, 150, 100)
        else:
            self.player.attack.clip_composite_draw(attack_sprites[int(self.player.frame)][0],
                                                   attack_sprites[int(self.player.frame)][1],
                                                   attack_sprites[int(self.player.frame)][2], 31, 0, 'h',
                                                   sx - 30, sy + 15, 150, 100)

skill2_sprites = (
    0, 54, 109, 164, 219, 274, 329, 384, 439
)

class Skill2:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0  # 공격 프레임 초기화

        if userdata.playerWeapon['sword'][1] == 5:
            whirlwind = Whirlwind(self.player.atk * 2.5)
            game_world.add_object(whirlwind, 1)
            game_world.add_collision_pair('nonBullet:monster', whirlwind, None)
            laser = sLaser(self.player.x, self.player.y, self.player.x + self.player.face_dir * get_canvas_width(), self.player.y, atk=self.player.atk * 1.75, w=150, h=100)
            game_world.add_object(laser, 1)
            game_world.add_collision_pair('bullet:monster', laser, None)

        elif userdata.playerWeapon['sword'][1] >= 2:
            whirlwind = Whirlwind(self.player.atk * 1.75)
            game_world.add_object(whirlwind, 1)
            game_world.add_collision_pair('nonBullet:monster', whirlwind, None)

    def exit(self, e):
        pass

    def do(self):
        # 공격 애니메이션 프레임 업데이트
        self.player.frame = (self.player.frame + FRAMES_PER_SKILL2 * SKILL2_PER_TIME * game_framework.frame_time)
        self.player.x += self.player.xdir * RUN_SPEED_PPS * game_framework.frame_time * self.player.speed
        self.player.y += self.player.ydir * RUN_SPEED_PPS * game_framework.frame_time * self.player.speed
        # 공격 애니메이션이 끝나면 상태 전환

        if self.player.frame >= FRAMES_PER_SKILL2:
            self.player.frame = 0
            if self.player.xdir == 0 and self.player.ydir == 0:
                self.player.state_machine.cur_state = self.player.IDLE
            else:
                self.player.state_machine.cur_state = self.player.RUN

    def draw(self):
        sx = self.player.x - common.map.window_left  # 화면상의 x 위치
        sy = self.player.y - common.map.window_bottom

        if self.player.face_dir == 1:  # right
            self.player.skill2_image.clip_composite_draw(skill2_sprites[int(self.player.frame)], 0,
                                                    53, 52, 0, ' ', sx - 15, sy, 160, 140)
        else:  # face_dir == -1: # left
            self.player.skill2_image.clip_composite_draw(skill2_sprites[int(self.player.frame)], 0,
                                                    53, 52, 0, 'h', sx + 15, sy, 160, 140)

skill3_sprites = [
    (0, 60), (158, 60), (316, 60), (474, 60), (632, 60), (790, 60), (948, 60),
    (0, 0), (158, 0), (316, 0), (474, 0)
]

class Skill3:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0  # 공격 프레임 초기화
        self.player.protect = True
        if userdata.playerWeapon['sword'][1] == 5:
            slam = Slam(self.player.atk * 3.5)
            game_world.add_object(slam, 1)
            game_world.add_collision_pair('nonBullet:monster', slam, None)
        elif userdata.playerWeapon['sword'][1] >= 2:
            slam = Slam(self.player.atk * 2.75)
            game_world.add_object(slam, 1)
            game_world.add_collision_pair('nonBullet:monster', slam, None)

    def exit(self, e):
        pass

    def do(self):
        # 공격 애니메이션 프레임 업데이트
        self.player.frame = (self.player.frame + FRAMES_PER_SKILL3 * SKILL3_PER_TIME * game_framework.frame_time)
        # 공격 애니메이션이 끝나면 상태 전환

        if self.player.frame >= FRAMES_PER_SKILL3:
            self.player.protect = False
            self.player.frame = 0
            if userdata.playerWeapon['sword'][1] == 5:
                for i in range(120, -120, -50):
                    clone = sClone(self.player.x + self.player.face_dir * 50, self.player.y + i, self.player.x + self.player.face_dir * get_canvas_width(), self.player.y + i, atk=self.player.atk * 2.5)
                    game_world.add_object(clone, 1)
                    game_world.add_collision_pair('bullet:monster', clone, None)

            if self.player.xdir == 0 and self.player.ydir == 0:
                self.player.state_machine.cur_state = self.player.IDLE
            else:
                self.player.state_machine.cur_state = self.player.RUN

    def draw(self):
        sx = self.player.x - common.map.window_left  # 화면상의 x 위치
        sy = self.player.y - common.map.window_bottom

        if self.player.face_dir == 1:  # right
            self.player.skill3_image.clip_composite_draw(skill3_sprites[int(self.player.frame)][0], skill3_sprites[int(self.player.frame)][1],
                                                   157, 59, 0, ' ', sx + 5, sy + 55, 400, 210)
        else:  # face_dir == -1: # left
            self.player.skill3_image.clip_composite_draw(skill3_sprites[int(self.player.frame)][0], skill3_sprites[int(self.player.frame)][1],
                                                   157, 59, 0, 'h', sx - 5, sy + 55, 400, 210)

dash_sprites = [ 0, 67, 134, 201, 268, 335, 402, 469 ]

class Dash:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        # 키 입력에 따라 방향 설정
        self.player.frame = 0.0
        self.player.protect = True
        self.player.x += self.player.face_dir * DASH_AMOUNT

        if self.player.xdir != 0:
            self.player.face_dir = self.player.xdir

        dash_attack = DashEffect(self.player.atk * 1.5)
        game_world.add_object(dash_attack, 1)
        game_world.add_collision_pair('nonBullet:monster', dash_attack, None)

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_DASH * DASH_PER_TIME * game_framework.frame_time)

        if self.player.frame >= FRAMES_PER_DASH:
            self.player.frame = 0.0
            self.player.protect = False
            if self.player.xdir == 0 and self.player.ydir == 0:
                self.player.state_machine.cur_state = self.player.IDLE
            else:
                self.player.state_machine.cur_state = self.player.RUN

    def draw(self):
        sx = self.player.x - common.map.window_left  # 화면상의 x 위치
        sy = self.player.y - common.map.window_bottom

        if self.player.face_dir == 1:  # right
            self.player.dash_image.clip_composite_draw(dash_sprites[int(self.player.frame)], 0, 66, 23,
                                                  0, ' ', sx - 30, sy, 170, 75)
        else:  # face_dir == -1: # left
            self.player.dash_image.clip_composite_draw(dash_sprites[int(self.player.frame)], 0, 66, 23,
                                                  0, 'h', sx + 30, sy, 170, 75)

class PlayerS:
    def __init__(self):

        self.x = common.map.w / 2
        self.y = common.map.h / 2

        self.frame = 0
        self.face_dir = 1
        self.xdir = 0
        self.ydir = 0
        self.image = load_image('resources/sprites/sword_move.png')
        self.attack = load_image('resources/sprites/sword_attack.png')
        self.skill2_image = load_image('resources/sprites/sword_skill2_set.png')
        self.skill3_image = load_image('resources/sprites/sword_skill3_set.png')
        self.font = load_font('resources/DungGeunMo.TTF', 20)
        self.dash_image = load_image('resources/sprites/sword_dash.png')
        self.attacking = False
        self.atk = ((userdata.weaponAtk[userdata.playerWeapon['sword'][0]] + userdata.weaponAtk[
            userdata.playerWeapon['sword'][0]]
                     * userdata.weaponUp[userdata.playerWeapon['sword'][1]]) *
                    (1.0 + 0.1 * (userdata.playerSkill['general'][0])))
        if userdata.relics['relic2'] == 2:
            self.atk *= 5.0
        self.hp = userdata.maxHealth
        self.speed = 1.0 + 0.1 * (userdata.playerSkill['general'][2])

        self.weapon_time = 0.0
        self.dash_time = 0.0

        self.skill1_cnt = 0
        self.protect_timer = 0.0
        self.protect = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.ATTACK = Attack(self)  # Attack 상태 인스턴스 생성
        self.SKILL2 = Skill2(self)
        self.SKILL3 = Skill3(self)
        self.DASH = Dash(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                # 이동 키가 눌리면 RUN 상태로 진입
                self.IDLE: {event_run: self.RUN,
                            event_attack: self.ATTACK, event_skill2: self.SKILL2, event_skill3: self.SKILL3, event_dash: self.DASH},
                # RUN 상태에서 키가 눌리거나 떼어져도 RUN 상태를 유지
                self.RUN: {event_stop: self.IDLE,
                           event_attack: self.ATTACK, event_skill2: self.SKILL2, event_skill3: self.SKILL3, event_dash: self.DASH},
                self.ATTACK: {},
                self.SKILL2: {},
                self.SKILL3: {},
                self.DASH: {}
            }
        )

    def update(self):
        self.state_machine.update()

        if self.weapon_time > 0.0:
            self.weapon_time -= game_framework.frame_time
            if self.weapon_time < 0.0:
                self.weapon_time = 0.0

        if self.dash_time > 0.0:
            self.dash_time -= game_framework.frame_time
            if self.dash_time < 0.0:
                self.dash_time = 0.0

        if self.protect_timer > 0.0:
            self.protect_timer -= game_framework.frame_time
            if self.protect_timer < 0.0:
                self.protect_timer = 0.0
                self.protect = False

    def handle_event(self, event):
        if event.key in (SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_LSHIFT) or event.type in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
            cur_xdir, cur_ydir = self.xdir, self.ydir
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_a:
                    self.xdir -= 1
                elif event.key == SDLK_d:
                    self.xdir += 1
                elif event.key == SDLK_w:
                    self.ydir += 1
                elif event.key == SDLK_s:
                    self.ydir -= 1
                elif event.key == SDLK_LSHIFT:
                    if userdata.playerSkill['sword'][1] >= 1 and self.dash_time <= 0.0:
                        self.state_machine.handle_state_event(('DASH', None))
                        self.dash_time = 6.0
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_a:
                    self.xdir += 1
                elif event.key == SDLK_d:
                    self.xdir -= 1
                elif event.key == SDLK_w:
                    self.ydir -= 1
                elif event.key == SDLK_s:
                    self.ydir += 1
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                self.attacking = True
                self.state_machine.handle_state_event(('ATTACK', event))
            elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
                self.attacking = False
                self.state_machine.handle_state_event(('INPUT', event))
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
                if userdata.playerWeapon['sword'][1] >= 2 and self.weapon_time <= 0.0:
                    if userdata.playerWeapon['sword'][0] == 0:
                        self.skill1()
                    elif userdata.playerWeapon['sword'][0] == 1:
                        self.state_machine.handle_state_event(('SKILL2', event))
                    elif userdata.playerWeapon['sword'][0] == 2:
                        self.state_machine.handle_state_event(('SKILL3', event))
                    self.weapon_time = 10.0  # 스킬 쿨타임 설정

            if cur_xdir != self.xdir or cur_ydir != self.ydir:  # 방향키에 따른 변화가 있으면
                if self.xdir == 0 and self.ydir == 0:  # 멈춤
                    self.state_machine.handle_state_event(('STOP', self.face_dir))  # 스탑 시 이전 방향 전달
                else:  # 움직임
                    self.state_machine.handle_state_event(('RUN', None))
        else:
            self.state_machine.handle_state_event(('INPUT', event))
    def draw(self):
        if self.protect_timer > 0.5 and int(self.protect_timer * 10) % 2 == 0:
            pass
        else:
            self.state_machine.draw()

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        return sx - 30, sy - 40, sx + 30, sy + 40

    def handle_collision(self, group, other):
        if group == 'player:monster' and self.protect == False:
            if self.hp > 0:
                self.hp -= 1
            self.protect = True
            self.protect_timer = 1.5

    def skill1(self):
        if userdata.playerWeapon['sword'][1] == 5:
            self.skill1_cnt = 5
        elif userdata.playerWeapon['sword'][1] >= 2:
            self.skill1_cnt = 2

