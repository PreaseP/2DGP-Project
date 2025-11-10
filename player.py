from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP
from sdl2 import SDLK_w, SDLK_a, SDLK_s, SDLK_d

import game_world
import game_framework

from state_machine import StateMachine
from sword_effect import SwordEffect


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
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Move Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# Player Move Action Speed
TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 7

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
            self.player.image.clip_composite_draw(0, 35, 33, 22,
                                            0, ' ', self.player.x, self.player.y, 75, 75)
        else: # face_dir == -1: # left
            self.player.image.clip_composite_draw(0, 35, 33, 22,
                                                  0, 'h', self.player.x, self.player.y, 75, 75)

run_sprites = [
    (0, 0), (32, 0), (64, 0), (96, 0),
    (128, 0), (160, 0), (192, 0), (224, 0)
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
        self.player.x += self.player.xdir * RUN_SPEED_PPS * game_framework.frame_time
        self.player.y += self.player.ydir * RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        if self.player.xdir == 0:
            if self.player.face_dir == 1:  # right
                self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0], run_sprites[int(self.player.frame)][1], 31, 22,
                                                      0, ' ', self.player.x, self.player.y, 75, 75)
            else:  # face_dir == -1: # left
                self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0], run_sprites[int(self.player.frame)][1], 31, 22,
                                                      0, 'h', self.player.x, self.player.y, 75, 75)
        elif self.player.xdir == 1:
            self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0],
                                                  run_sprites[int(self.player.frame)][1], 31, 22,
                                                  0, ' ', self.player.x, self.player.y, 75, 75)
        else:
            self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0],
                                                  run_sprites[int(self.player.frame)][1], 31, 22,
                                                  0, 'h', self.player.x, self.player.y, 75, 75)

attack_sprites = [
    (0, 0, 62), (63, 0, 62), (126, 0, 62), (189, 0, 62),
    (252, 0, 62), (315, 0, 62), (378, 0, 62)
]

class Attack:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0  # 공격 프레임 초기화
        effect = SwordEffect(self.player.x + self.player.xdir * 80, self.player.y, self.player.face_dir, self.player.xdir)
        game_world.add_object(effect, 1)

    def exit(self, e):
        pass

    def do(self):
        # 공격 애니메이션 프레임 업데이트
        self.player.frame = (self.player.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time)
        self.player.x += self.player.xdir * RUN_SPEED_PPS * game_framework.frame_time
        self.player.y += self.player.ydir * RUN_SPEED_PPS * game_framework.frame_time
        # 공격 애니메이션이 끝나면 상태 전환

        if self.player.xdir != 0:
            self.player.face_dir = self.player.xdir

        if self.player.frame >= FRAMES_PER_ATTACK:
            if self.player.attacking:
              self.player.frame = 0
              effect = SwordEffect(self.player.x + self.player.xdir * 80, self.player.y, self.player.face_dir, self.player.xdir)
              game_world.add_object(effect, 1)
            elif self.player.xdir == 0 and self.player.ydir == 0:
                self.player.state_machine.cur_state = self.player.IDLE
            else:
                self.player.state_machine.cur_state = self.player.RUN

    def draw(self):
        if self.player.xdir == 0:
            if self.player.face_dir == 1:  # right
                self.player.attack.clip_composite_draw(attack_sprites[int(self.player.frame)][0], attack_sprites[int(self.player.frame)][1],
                                                       attack_sprites[int(self.player.frame)][2], 31, 0, ' ', self.player.x - 5, self.player.y + 15, 100, 100)
            else:  # face_dir == -1: # left
                self.player.attack.clip_composite_draw(attack_sprites[int(self.player.frame)][0], attack_sprites[int(self.player.frame)][1],
                                                       attack_sprites[int(self.player.frame)][2], 31, 0, 'h', self.player.x - 5, self.player.y + 15, 100, 100)
        elif self.player.xdir == 1:
            self.player.attack.clip_composite_draw(attack_sprites[int(self.player.frame)][0],
                                                   attack_sprites[int(self.player.frame)][1],
                                                   attack_sprites[int(self.player.frame)][2], 31, 0, ' ',
                                                   self.player.x - 5, self.player.y + 15, 100, 100)
        else:
            self.player.attack.clip_composite_draw(attack_sprites[int(self.player.frame)][0],
                                                   attack_sprites[int(self.player.frame)][1],
                                                   attack_sprites[int(self.player.frame)][2], 31, 0, 'h',
                                                   self.player.x - 5, self.player.y + 15, 100, 100)

class Player:
    def __init__(self):

        self.x, self.y = 640, 360
        self.frame = 0
        self.face_dir = 1
        self.xdir = 0
        self.ydir = 0
        self.image = load_image('resources/sprites/sword_move.png')
        self.attack = load_image('resources/sprites/sword_attack.png')
        self.attacking = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.ATTACK = Attack(self)  # Attack 상태 인스턴스 생성
        self.state_machine = StateMachine(
            self.IDLE,
            {
                # 이동 키가 눌리면 RUN 상태로 진입
                self.IDLE: {event_run: self.RUN,
                            event_attack: self.ATTACK},
                # RUN 상태에서 키가 눌리거나 떼어져도 RUN 상태를 유지
                self.RUN: {event_stop: self.IDLE,
                           event_attack: self.ATTACK},
                self.ATTACK: {}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.key in (SDLK_a, SDLK_d, SDLK_w, SDLK_s) or event.type in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
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
            elif event.type == SDL_MOUSEBUTTONDOWN:
                self.attacking = True
                self.state_machine.handle_state_event(('ATTACK', event))
            elif event.type == SDL_MOUSEBUTTONUP:
                self.attacking = False
                self.state_machine.handle_state_event(('INPUT', event))

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

