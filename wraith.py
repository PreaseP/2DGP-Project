from pico2d import *

import random
import math

import common
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from damage_font import DamageFont
from keese_bullet import KeeseBullet

# Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 7.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Walk
TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5.0

# Disappear / Appear
TIME_PER_APPEAR = 1.5
APPEAR_PER_TIME = 1.0 / TIME_PER_APPEAR
FRAMES_PER_APPEAR = 12.0

animationNames = {'Walk' : 0, 'Disappear' : 2, 'Appear' : 1}

sprites = [
    [(5, 230), (30, 230), (55, 230), (80, 230), (105, 230)],
    [(5, 284), (30, 284), (54, 284), (79, 284), (101, 284), (125, 284),
     (149, 284), (173, 284), (197, 284), (221, 284), (245, 284), (269, 284)],
    [(269, 284), (245, 284), (221, 284), (197, 284), (173, 284), (149, 284),
     (125, 284), (101, 284), (79, 284), (54, 284), (30, 284), (5, 284)]
]

size = [(25, 31), (24, 38), (24, 38)]

class Wraith:
    image = None

    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(common.borders[common.map.left_border] - 50, common.borders[common.map.right_border] + 50)
        self.y = y if y else random.choice([random.randint(-50, -30), random.randint(720 + 30, 720 + 50)])
        self.w = 50
        self.h = 50

        self.hp = 150

        if Wraith.image == None:
            Wraith.image = load_image('resources/sprites/relic1_wraith.png')

        self.dir = 0.0      # radian 값으로 방향을 표시
        self.frame = random.randint(0, 5)
        self.state = 'Walk'

        self.protect_timer = 0.0
        self.protect = False

        self.tel_timer = 6.0

        self.build_behavior_tree()


    def get_bb(self):
        if self.state == 'Walk':
            sx = self.x - common.map.window_left
            sy = self.y - common.map.window_bottom

            return sx - self.w / 2, sy - self.h / 2, sx + self.w / 2, sy + self.h /2
        else:
            return -9999, -9999, -9999, -9999


    def update(self):
        self.bt.run()  # 매 프레임마다 행동트리를 root부터 시작해서 실행함.

        if self.state == 'Walk':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        else:
            self.frame = (self.frame + FRAMES_PER_APPEAR * APPEAR_PER_TIME * game_framework.frame_time) % FRAMES_PER_APPEAR

        if self.protect:
            self.protect_timer -= game_framework.frame_time
            if self.protect_timer <= 0:
                self.protect = False

        if self.tel_timer > 0.0:
            self.tel_timer -= game_framework.frame_time
            if self.tel_timer < 0.0:
                self.tel_timer = 0.0

    def draw(self):
        sx = self.x - common.map.window_left
        sy = self.y - common.map.window_bottom

        if math.cos(self.dir) < 0:
            Wraith.image.clip_composite_draw(sprites[animationNames[self.state]][int(self.frame)][0],
                                           sprites[animationNames[self.state]][int(self.frame)][1],
                                           size[animationNames[self.state]][0], size[animationNames[self.state]][1], 0, ' ', sx, sy, self.w, self.h)
        else:
            Wraith.image.clip_composite_draw(sprites[animationNames[self.state]][int(self.frame)][0],
                                           sprites[animationNames[self.state]][int(self.frame)][1],
                                           size[animationNames[self.state]][0], size[animationNames[self.state]][1], 0, 'h', sx, sy, self.w, self.h)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if (group == 'nonBullet:monster' and self.protect == False and other.atk_available == True) or (
                group == 'bullet:monster' and self.protect == False):
            self.hp -= other.atk
            print_damage = DamageFont(*self.get_bb(), other.atk)
            game_world.add_object(print_damage, 3)
            self.protect = True
            self.protect_timer = 0.6
            if group == 'nonBullet:monster':
                if other.face_dir > 0:
                    self.x += 10
                else:
                    self.x -= 10
            elif group == 'bullet:monster':
                if other.dx > 0:
                    self.x += 10
                else:
                    self.x -= 10
            if self.hp <= 0:
                common.monsterCount -= 1
                game_world.remove_object(self)

    # 거리 비교 함수
    def distance_less_than(self, x1, y1, x2, y2, r): #r은 미터 단위
        distance2 = (x1 - x2) **2 + (y1 - y2) **2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_little_to(self, tx, ty):
        # frame_time 을 사용하여 이동 거리를 계산.
        self.dir = math.atan2(ty - self.y, tx - self.x)  # 각도 구하기
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def move_to_player(self):
        self.state = 'Walk'
        self.move_little_to(common.player.x, common.player.y)
        if self.distance_less_than(common.player.x, common.player.y, self.x, self.y, 0.5):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_teleport_available(self):
        if self.tel_timer == 0.0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def disappear(self):
        if self.state != 'Disappear':
            self.frame = 0
            self.state = 'Disappear'
        if int(self.frame) == FRAMES_PER_APPEAR - 1:
            self.frame = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.x = random.randint(common.borders[common.map.left_border] + 50, common.borders[common.map.right_border] - 50)
        self.y = random.randint(0 + 50, 720 - 50)
        return BehaviorTree.SUCCESS

    def appear(self):
        if self.state != 'Appear':
            self.frame = 0
            self.state = 'Appear'
        if int(self.frame) == FRAMES_PER_APPEAR - 1:
            self.frame = 0
            self.tel_timer = 7.0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        a1 = Action('Move to player', self.move_to_player)
        a2 = Action('Disappear', self.disappear)
        a3 = Action('Set random location', self.set_random_location)
        a4 = Action('Appear', self.appear)

        chase_player = Sequence('Chase player', a1)

        c1 = Condition('teleport 쿨타임이 지났는가?', self.is_teleport_available)

        teleport_randomly = Sequence('랜덤 텔레포트', c1, a2, a3, a4)

        root = attack_or_chase_player = Selector('텔레포트 아니면 추적', teleport_randomly, chase_player)

        self.bt = BehaviorTree(root)