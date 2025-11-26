from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT, \
    SDL_MOUSEMOTION, SDL_BUTTON_RIGHT, SDLK_LSHIFT
from sdl2 import SDLK_w, SDLK_a, SDLK_s, SDLK_d

import game_world
import game_framework
import userdata
from bullet import Bullet
from laser import Laser
from burst import Burst

from state_machine import StateMachine

def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def mouse_click(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN

def mouse_release(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONUP

def event_skill2(e):
    return e[0] == 'SKILL2'

def event_skill3(e):
    return e[0] == 'SKILL3'

def event_stop(e):
    return e[0] == 'STOP'

def event_run(e):
    return e[0] == 'RUN'

def event_slide(e):
    return e[0] == 'SLIDE'

def event_attack(e):
    return e[0] == 'ATTACK'

# Player의 Run Speed 계산

# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Slide Speed
SLIDE_SPEED_PPS = RUN_SPEED_PPS * 1.5

# Player Move Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# Player Slide Action Speed
TIME_PER_SLIDE = 0.5
SLIDE_PER_TIME = 1.0 / TIME_PER_SLIDE
FRAMES_PER_SLIDE = 16

# Player Skill2 Action Speed
TIME_PER_SKILL2 = 0.5
SKILL2_PER_TIME = 1.0 / TIME_PER_SKILL2
FRAMES_PER_SKILL2 = (6, 6, 6, 6, 6, 7)

# Player Skill3 Action Speed
TIME_PER_SKILL3 = 0.5
SKILL3_PER_TIME = 1.0 / TIME_PER_SKILL3
FRAMES_PER_SKILL3 = 6

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
                                            0, ' ', self.player.x + 15, self.player.y, 75, 75)
        else: # face_dir == -1: # left
            self.player.image.clip_composite_draw(0, 41, 17, 50,
                                                  0, 'h', self.player.x - 15, self.player.y, 75, 75)

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
        self.player.x += self.player.xdir * RUN_SPEED_PPS * game_framework.frame_time * self.player.speed
        self.player.y += self.player.ydir * RUN_SPEED_PPS * game_framework.frame_time * self.player.speed

        if self.player.xdir != 0:
            self.player.face_dir = self.player.xdir

    def draw(self):
        if self.player.xdir == 0:
            if self.player.face_dir == 1:  # right
                self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0], run_sprites[int(self.player.frame)][1], 20, 22,
                                                      0, ' ', self.player.x + 5, self.player.y, 75, 75)
            else:  # face_dir == -1: # left
                self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0], run_sprites[int(self.player.frame)][1], 20, 22,
                                                      0, 'h', self.player.x - 5, self.player.y, 75, 75)
        elif self.player.xdir == 1:
            self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0],
                                                  run_sprites[int(self.player.frame)][1], 20, 22,
                                                  0, ' ', self.player.x + 5, self.player.y, 75, 75)
        else:
            self.player.image.clip_composite_draw(run_sprites[int(self.player.frame)][0],
                                                  run_sprites[int(self.player.frame)][1], 20, 22,
                                                  0, 'h', self.player.x - 5, self.player.y, 75, 75)

skill2_sprites = [
    (0, 50, 100, 150, 200, 250),
    (0, 82, 164, 246, 328, 410, 492)
]

class Skill2:
    def __init__(self, player):
        self.player = player
        self.second_burst = False

    def enter(self, e):
        self.player.frame = 0  # 공격 프레임 초기화
        self.burst_atk = self.player.atk

        if userdata.playerWeapon['gun'][1] == 5:
            self.burst_atk *= 1.75  # 스킬2 공격력 증가
            self.second_burst = True
        elif userdata.playerWeapon['gun'][1] >= 2:
            self.burst_atk *= 1.25  # 스킬2 공격력 증가

        burst = Burst(self.player.x + self.player.xdir * 75, self.player.y, self.player.face_dir * 1280, face_dir = self.player.face_dir, xdir = self.player.xdir, atk = self.burst_atk)
        game_world.add_object(burst, 1)
        game_world.add_collision_pair('bullet:monster', burst, None)

    def exit(self, e):
        pass

    def do(self):
        # 공격 애니메이션 프레임 업데이트
        self.player.frame = (self.player.frame + FRAMES_PER_SKILL2[userdata.playerWeapon['gun'][1]] * SKILL2_PER_TIME * game_framework.frame_time)
        # 공격 애니메이션이 끝나면 상태 전환

        if int(self.player.frame) == 3 and self.second_burst:
            burst = Burst(self.player.x - self.player.xdir * 75, self.player.y, self.player.face_dir * -1280,
                          face_dir=self.player.face_dir * -1, xdir=self.player.xdir, atk=self.burst_atk)
            game_world.add_object(burst, 1)
            game_world.add_collision_pair('bullet:monster', burst, None)
            self.second_burst = False

        if self.player.frame >= FRAMES_PER_SKILL2[userdata.playerWeapon['gun'][1]]:
            if self.player.xdir == 0 and self.player.ydir == 0:
                self.player.state_machine.cur_state = self.player.IDLE
            else:
                self.player.state_machine.cur_state = self.player.RUN

    def draw(self):
        if userdata.playerWeapon['gun'][1] == 5:
            if self.player.face_dir == 1:  # right
                self.player.skill2_image2.clip_composite_draw(skill2_sprites[1][int(self.player.frame)], 0,
                                                       81, 28, 0, ' ', self.player.x + 5, self.player.y + 10, 300, 95)
            else:  # face_dir == -1: # left
                self.player.skill2_image2.clip_composite_draw(skill2_sprites[1][int(self.player.frame)], 0,
                                                       81, 28, 0, 'h', self.player.x - 5, self.player.y + 10, 300, 95)
        else:
            if self.player.face_dir == 1:  # right
                self.player.skill2_image1.clip_composite_draw(skill2_sprites[0][int(self.player.frame)], 0,
                                                        49, 27, 0, ' ', self.player.x + 65, self.player.y + 15, 200, 100)
            else:  # face_dir == -1: # left
                self.player.skill2_image1.clip_composite_draw(skill2_sprites[0][int(self.player.frame)], 0,
                                                        49, 27, 0, 'h', self.player.x - 65, self.player.y + 15, 200, 100)

skill3_sprites = [
    (1, 1), (77, 1), (153, 1), (229, 1),
    (305, 1), (381, 1)
]

class Skill3:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0  # 공격 프레임 초기화
        if userdata.playerWeapon['gun'][1] == 5:
            for k in range(2):
                laser = Laser(self.player.x, self.player.y, self.player.face_dir * 1280, self.player.y + 200 - 400 * k, atk=self.player.atk * 2.5, w= 225, h= 110)
                game_world.add_object(laser, 1)
                game_world.add_collision_pair('bullet:monster', laser, None)
        elif userdata.playerWeapon['gun'][1] >= 2:
            laser = Laser(self.player.x, self.player.y, self.player.face_dir * 1280, self.player.y, atk=self.player.atk * 2.0, w= 200, h= 100)
            game_world.add_object(laser, 1)
            game_world.add_collision_pair('bullet:monster', laser, None)

    def exit(self, e):
        pass

    def do(self):
        # 공격 애니메이션 프레임 업데이트
        self.player.frame = (self.player.frame + FRAMES_PER_SKILL3 * SKILL3_PER_TIME * game_framework.frame_time)
        # 공격 애니메이션이 끝나면 상태 전환

        if self.player.frame >= FRAMES_PER_SKILL3:
            if self.player.xdir == 0 and self.player.ydir == 0:
                self.player.state_machine.cur_state = self.player.IDLE
            else:
                self.player.state_machine.cur_state = self.player.RUN

    def draw(self):
        if self.player.face_dir == 1:  # right
            self.player.skill3_image.clip_composite_draw(skill3_sprites[int(self.player.frame)][0], skill3_sprites[int(self.player.frame)][1],
                                                   74, 33, 0, ' ', self.player.x + 120, self.player.y + 20, 300, 115)
        else:  # face_dir == -1: # left
            self.player.skill3_image.clip_composite_draw(skill3_sprites[int(self.player.frame)][0], skill3_sprites[int(self.player.frame)][1],
                                                   74, 33, 0, 'h', self.player.x - 120, self.player.y + 20, 300, 115)

slide_sprites = [ (0, 62), (54, 62), (108, 62),
                  (0, 35), (32, 35), (64, 35),
                  (0, 35), (32, 35), (64, 35),
                  (0, 35), (32, 35), (64, 35),
                  (0, 0), (54, 0), (108, 0), (162, 0)]

class Slide:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        # 키 입력에 따라 방향 설정
        self.player.frame = 0.0
        self.player.slide = True

        if self.player.xdir != 0:
            self.player.face_dir = self.player.xdir

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_SLIDE * SLIDE_PER_TIME * game_framework.frame_time)
        self.player.x += self.player.face_dir * SLIDE_SPEED_PPS * game_framework.frame_time * self.player.speed
        self.player.y += self.player.ydir * RUN_SPEED_PPS * game_framework.frame_time * self.player.speed

        if self.player.frame >= FRAMES_PER_SLIDE:
            self.player.frame = 0.0
            self.player.slide = False
            if self.player.xdir == 0 and self.player.ydir == 0:
                self.player.state_machine.cur_state = self.player.IDLE
            else:
                self.player.state_machine.cur_state = self.player.RUN

    def draw(self):
        if 3.0 <= self.player.frame < 12.0:
            if self.player.face_dir == 1:  # right
                self.player.slide_image.clip_composite_draw(slide_sprites[int(self.player.frame)][0], slide_sprites[int(self.player.frame)][1], 31, 17,
                                                      0, ' ', self.player.x - 5, self.player.y, 100, 75)
            else:  # face_dir == -1: # left
                self.player.slide_image.clip_composite_draw(slide_sprites[int(self.player.frame)][0], slide_sprites[int(self.player.frame)][1], 31, 17,
                                                      0, 'h', self.player.x + 5, self.player.y, 100, 75)
        else:
            if self.player.face_dir == 1:  # right
                self.player.slide_image.clip_composite_draw(slide_sprites[int(self.player.frame)][0], slide_sprites[int(self.player.frame)][1], 53, 25,
                                                      0, ' ', self.player.x - 5, self.player.y + 10, 230, 90)
            else:  # face_dir == -1: # left
                self.player.slide_image.clip_composite_draw(slide_sprites[int(self.player.frame)][0], slide_sprites[int(self.player.frame)][1], 53, 25,
                                                      0, 'h', self.player.x + 5, self.player.y + 10, 230, 90)

class PlayerG:
    def __init__(self):

        self.x, self.y = 640, 360
        self.frame = 0
        self.face_dir = 1
        self.xdir = 0
        self.ydir = 0
        self.image = load_image('resources/sprites/gun_move.png')
        self.skill2_image1 = load_image('resources/sprites/gun_skill2_set1.png')
        self.skill2_image2 = load_image('resources/sprites/gun_skill2_set2.png')
        self.skill3_image = load_image('resources/sprites/gun_skill3_set.png')
        self.slide_image = load_image('resources/sprites/gun_slide.png')
        self.font = load_font('resources/DungGeunMo.TTF', 20)
        self.attacking = False
        self.slide = False
        self.atk = ((userdata.weaponAtk[userdata.playerWeapon['gun'][0]] + userdata.weaponAtk[userdata.playerWeapon['gun'][0]]
                     * userdata.weaponUp[userdata.playerWeapon['gun'][1]]) *
                    (1.0 + 0.1 * (userdata.playerSkill['general'][0])))
        self.hp = userdata.maxHealth
        self.speed = 1.0 + 0.1 * (userdata.playerSkill['general'][2])

        # 연속 발사 관련
        self.fire_rate = 1.5  # 초당 발사 수 (원하면 조정)
        self.fire_interval = 1.0 / self.fire_rate
        self.fire_cooldown = 0.0
        self.last_mouse_x = self.x
        self.last_mouse_y = self.y

        self.weapon_time = 0.0

        self.slide_time = 0.0

        self.protect_time = 0.0
        self.protect = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.SKILL2 = Skill2(self)
        self.SKILL3 = Skill3(self)
        self.SLIDE = Slide(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                # 이동 키가 눌리면 RUN 상태로 진입
                self.IDLE: {event_run: self.RUN, event_skill2: self.SKILL2, event_skill3: self.SKILL3, event_slide: self.SLIDE},
                # RUN 상태에서 키가 눌리거나 떼어져도 RUN 상태를 유지
                self.RUN: {event_run: self.RUN, event_stop: self.IDLE, event_skill2: self.SKILL2, event_skill3: self.SKILL3, event_slide: self.SLIDE},
                self.SKILL3: {},
                self.SKILL2: {},
                self.SLIDE: {}
            }
        )

    def update(self):
        self.state_machine.update()
        # 발사 쿨타임 감소 및 연속 발사 처리
        dt = game_framework.frame_time
        if self.fire_cooldown > 0.0:
            self.fire_cooldown -= dt
            if self.fire_cooldown < 0.0:
                self.fire_cooldown = 0.0

        if self.weapon_time > 0.0:
            self.weapon_time -= dt
            if self.weapon_time < 0.0:
                self.weapon_time = 0.0

        if self.slide_time > 0.0:
            self.slide_time -= dt
            if self.slide_time < 0.0:
                self.slide_time = 0.0

        if self.attacking and self.fire_cooldown <= 0:
            # 마우스 좌표는 이미 pico2d 좌표로 변환되어 있어야 함
            heal = False
            if self.slide is True and userdata.playerSkill['gun'][1] == 2:
                heal = True
            b = Bullet(self.x, self.y, self.last_mouse_x, self.last_mouse_y, atk=self.atk, heal=heal)
            game_world.add_object(b, 1)
            game_world.add_collision_pair('bullet:monster', b, None)
            self.fire_cooldown = self.fire_interval

        if self.protect_time > 0.0:
            self.protect_time -= dt
            if self.protect_time < 0.0:
                self.protect_time = 0.0
                self.protect = False

    def handle_event(self, event):
        if event.key in (SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_LSHIFT) or event.type in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP, SDL_MOUSEMOTION):
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
                    if userdata.playerSkill['gun'][1] >= 1 and self.slide_time <= 0.0:
                        self.state_machine.handle_state_event(('SLIDE', None))
                        self.slide_time = 8.0
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
                if self.slide is True and userdata.playerSkill['gun'][1] == 1:
                    return
                self.attacking = True
            elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
                self.attacking = False
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
                if userdata.playerWeapon['gun'][1] >= 2 and self.weapon_time <= 0.0 and self.slide is False:
                    if userdata.playerWeapon['gun'][0] == 0:
                        self.skill1()
                    elif userdata.playerWeapon['gun'][0] == 1:
                        self.state_machine.handle_state_event(('SKILL2', event))
                    elif userdata.playerWeapon['gun'][0] == 2:
                        self.state_machine.handle_state_event(('SKILL3', event))
                    self.weapon_time = 1.0  # 스킬 쿨타임 설정

            if cur_xdir != self.xdir or cur_ydir != self.ydir:  # 방향키에 따른 변화가 있으면
                if self.xdir == 0 and self.ydir == 0:  # 멈춤
                    self.state_machine.handle_state_event(('STOP', self.face_dir))  # 스탑 시 이전 방향 전달
                else:  # 움직임
                    self.state_machine.handle_state_event(('RUN', None))
        else:
            self.state_machine.handle_state_event(('INPUT', event))
    def draw(self):
        if self.protect_time > 0.5 and int(self.protect_time * 10) % 2 == 0:
            pass
        else:
            self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        if self.weapon_time > 0.0:
            self.font.draw(480, 100, f'weapon skill cooldown: {self.weapon_time:.1f}s', (255, 255, 0))
        if self.slide_time > 0.0:
            self.font.draw(480, 80, f'slide skill cooldown: {self.slide_time:.1f}s', (255, 255, 0))


    def skill1(self):
        # 플레이어 기준 상하좌우로 총알 발사
        directions = [(1280, 0), (-1280, 0), (0, 720), (0, -720)]  # 오른쪽, 왼쪽, 위, 아래
        for dir_x, dir_y in directions:
            target_x = self.x + dir_x
            target_y = self.y + dir_y
            b = Bullet(self.x, self.y, target_x, target_y, atk = self.atk, piercing = True)
            game_world.add_object(b, 1)
            game_world.add_collision_pair('bullet:monster', b, None)


    def get_bb(self):
        return self.x - 30, self.y - 40, self.x + 30, self.y + 40

    def handle_collision(self, group, other):
        if group == 'player:monster' and self.protect == False:
            if self.hp > 0:
                self.hp -= 1
            self.protect = True
            self.protect_time = 1.5

