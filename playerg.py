from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT, \
    SDL_MOUSEMOTION
from sdl2 import SDLK_w, SDLK_a, SDLK_s, SDLK_d

import game_world
import game_framework
import userdata
from bullet import Bullet

from state_machine import StateMachine

def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def mouse_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN

def mouse_release(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONUP

def event_stop(e):
    return e[0] == 'STOP'

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
        if self.player.face_dir == 1: # right
            self.player.image.clip_composite_draw(0, 41, 17, 50,
                                            0, ' ', self.player.x, self.player.y, 75, 75)
        else: # face_dir == -1: # left
            self.player.image.clip_composite_draw(0, 41, 17, 50,
                                                  0, 'h', self.player.x, self.player.y, 75, 75)

run_sprites = [
    (6, 0), (40, 0), (75, 0), (110, 0),
    (143, 0), (178, 0), (210, 0), (245, 0)
]

class Run:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        # 키 입력에 따라 방향 설정
        if self.player.xdir != 0:
            self.player.face_dir = self.player.xdir

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        # self.player.frame = 7
        self.player.x += self.player.xdir * RUN_SPEED_PPS * game_framework.frame_time
        self.player.y += self.player.ydir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.player.xdir == 0:
            if self.player.face_dir == 1:  # right
                self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0], run_sprites[int(self.player.frame)][1], 20, 22,
                                                      0, ' ', self.player.x, self.player.y, 75, 75)
            else:  # face_dir == -1: # left
                self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0], run_sprites[int(self.player.frame)][1], 20, 22,
                                                      0, 'h', self.player.x, self.player.y, 75, 75)
        elif self.player.xdir == 1:
            self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0],
                                                  run_sprites[int(self.player.frame)][1], 20, 22,
                                                  0, ' ', self.player.x, self.player.y, 75, 75)
        else:
            self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0],
                                                  run_sprites[int(self.player.frame)][1], 20, 22,
                                                  0, 'h', self.player.x, self.player.y, 75, 75)

class PlayerG:
    def __init__(self):

        self.x, self.y = 640, 360
        self.frame = 0
        self.face_dir = 1
        self.xdir = 0
        self.ydir = 0
        self.image = load_image('resources/sprites/gun_move.png')
        self.attacking = False
        self.atk = ((userdata.weaponAtk[userdata.playerWeapon['gun'][0]] + userdata.weaponAtk[userdata.playerWeapon['gun'][0]]
                     * userdata.weaponUp[userdata.playerWeapon['gun'][1]]) *
                    (1.0 + 0.1 * (userdata.playerSkill['general'][0])))
        self.hp = userdata.maxHealth

        # 연속 발사 관련
        self.fire_rate = 1.5  # 초당 발사 수 (원하면 조정)
        self.fire_interval = 1.0 / self.fire_rate
        self.fire_cooldown = 0.0
        self.last_mouse_x = self.x
        self.last_mouse_y = self.y

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                # 이동 키가 눌리면 RUN 상태로 진입
                self.IDLE: {event_run: self.RUN},
                # RUN 상태에서 키가 눌리거나 떼어져도 RUN 상태를 유지
                self.RUN: {event_stop: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()
        # 발사 쿨타임 감소 및 연속 발사 처리
        dt = game_framework.frame_time
        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt
        if self.attacking and self.fire_cooldown <= 0:
            # 마우스 좌표는 이미 pico2d 좌표로 변환되어 있어야 함
            b = Bullet(self.x, self.y, self.last_mouse_x, self.last_mouse_y, atk=self.atk)
            game_world.add_object(b, 1)
            game_world.add_collision_pair('bullet:monster', b, None)
            self.fire_cooldown = self.fire_interval

    def handle_event(self, event):
        if event.key in (SDLK_a, SDLK_d, SDLK_w, SDLK_s) or event.type in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP, SDL_MOUSEMOTION):
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
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_a:
                    self.xdir += 1
                elif event.key == SDLK_d:
                    self.xdir -= 1
                elif event.key == SDLK_w:
                    self.ydir -= 1
                elif event.key == SDLK_s:
                    self.ydir += 1
            elif event.type == SDL_MOUSEMOTION:
                self.last_mouse_x = event.x
                self.last_mouse_y = 720 - event.y
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                # 좌표 변환 (SDL 위쪽 원점 -> pico2d 아래 원점)
                self.last_mouse_x = event.x
                self.last_mouse_y = 720 - event.y
                self.attacking = True
            elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
                self.attacking = False


            if cur_xdir != self.xdir or cur_ydir != self.ydir:  # 방향키에 따른 변화가 있으면
                if self.xdir == 0 and self.ydir == 0:  # 멈춤
                    self.state_machine.handle_state_event(('STOP', self.face_dir))  # 스탑 시 이전 방향 전달
                else:  # 움직임
                    self.state_machine.handle_state_event(('RUN', None))
        else:
            self.state_machine.handle_state_event(('INPUT', event))
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40

    def handle_collision(self, group, other):
        pass

