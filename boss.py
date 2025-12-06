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
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Walk
TIME_PER_ACTION = 0.9
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 12.0

# Disappear / Appear
TIME_PER_APPEAR = 0.9
APPEAR_PER_TIME = 1.0 / TIME_PER_APPEAR
FRAMES_PER_APPEAR = 5.0

# Attack
TIME_PER_ATTACK = 0.7
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 7.0

# death
TIME_PER_DEATH = 1.5
DEATH_PER_TIME = 1.0 / TIME_PER_DEATH
FRAMES_PER_DEATH = 15.0

animationNames = {'Walk' : 0, 'Disappear' : 2, 'Appear' : 1, 'Attack' : 3, 'Death' : 4}

sprites = [
    [(6, 465), (45, 465), (84, 465), (123, 465), (162, 465), (201, 465),
     (240, 465), (279, 465), (318, 465), (357, 465), (396, 465), (435, 465)],
    [(6, 2), (71, 2), (136, 2), (201, 2), (266, 2)],
    [(266, 2), (201, 2), (136, 2), (71, 2), (6, 2)],
    [(6, 107), (87, 107), (168, 107), (249, 107), (330, 107),
     (411, 107), (492, 107)],
    [(6, 357), (105, 357), (204, 357), (303, 357), (402, 357),
     (6, 259), (105, 259), (204, 259), (303, 259), (402, 259),
     (6, 161), (105, 161), (204, 161), (303, 161), (402, 161)]
]

size = [(38, 52), (64, 50), (64, 50), (80, 43), (98, 97)]

class Boss:
    image = None

    def __init__(self, x=None, y=None):
        self.x, self.y = 1280 - 100, 360
        self.w = 100
        self.h = 100

        self.hp = 2400

        self.r = 2.0

        if Boss.image == None:
            Boss.image = load_image('resources/sprites/boss.png')

        self.dir = 0.0      # radian 값으로 방향을 표시
        self.frame = random.randint(0, 12)
        self.state = 'Walk'

        self.protect_timer = 0.0
        self.protect = False

        self.tel_timer = 6.0

        self.build_behavior_tree()


    def get_bb(self):
        if self.state == 'Walk' or self.state == 'Attack':
            sx = self.x - common.map.window_left
            sy = self.y - common.map.window_bottom

            return sx - self.w / 2, sy - self.h / 2, sx + self.w / 2, sy + self.h /2
        else:
            return -9999, -9999, -9999, -9999


    def update(self):
        self.bt.run()  # 매 프레임마다 행동트리를 root부터 시작해서 실행함.

        if self.state == 'Walk':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        elif self.state == 'Appear' or self.state == 'Disappear':
            self.frame = (self.frame + FRAMES_PER_APPEAR * APPEAR_PER_TIME * game_framework.frame_time) % FRAMES_PER_APPEAR
        elif self.state == 'Death':
            self.frame = (self.frame + FRAMES_PER_DEATH * DEATH_PER_TIME * game_framework.frame_time) % FRAMES_PER_DEATH
        elif self.state == 'Attack':
            self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % FRAMES_PER_ATTACK

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
            Boss.image.clip_composite_draw(sprites[animationNames[self.state]][int(self.frame)][0],
                                           sprites[animationNames[self.state]][int(self.frame)][1],
                                           size[animationNames[self.state]][0], size[animationNames[self.state]][1], 0, 'h', sx, sy, self.w, self.h)
        else:
            Boss.image.clip_composite_draw(sprites[animationNames[self.state]][int(self.frame)][0],
                                           sprites[animationNames[self.state]][int(self.frame)][1],
                                           size[animationNames[self.state]][0], size[animationNames[self.state]][1], 0, ' ', sx, sy, self.w, self.h)

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

    def if_player_in_attack(self):
        if self.distance_less_than(common.player.x, common.player.y, self.x, self.y, self.r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def attack_player(self):
        if self.state != 'Attack':
            self.frame = 0
            self.state = 'Attack'
        if int(self.frame) == FRAMES_PER_ATTACK - 1:
            self.frame = 0
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
        self.x = random.choice([random.randint(int(common.player.x) - 100, int(common.player.x) - 50), random.randint(int(common.player.x) + 50, int(common.player.x) + 100)])
        self.y = random.choice([random.randint(int(common.player.y) - 100, int(common.player.y) - 50), random.randint(int(common.player.y) + 50, int(common.player.y) + 100)])
        return BehaviorTree.SUCCESS

    def shoot_bullet(self):
        bullet = KeeseBullet(self.x, self.y, common.player.x, common.player.y, 6)
        game_world.add_object(bullet, 1)
        game_world.add_collision_pair('player:monster', None, bullet)
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

    def if_hp_0(self):
        if self.hp <= 0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def if_hp_half(self):
        if self.hp <= 1200:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def death(self):
        if self.state != 'Death':
            self.w = 200
            self.h = 200
            self.x -= 50
            self.y += 50
            self.frame = 0
            self.state = 'Death'

        if int(self.frame) == FRAMES_PER_DEATH - 1:
            self.frame = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def end(self):
        pass

    def build_behavior_tree(self):
        a1 = Action('Move to player', self.move_to_player)
        a2 = Action('Disappear', self.disappear)
        a3 = Action('Set random location', self.set_random_location)
        a4 = Action('Appear', self.appear)

        a5 = Action('Death', self.death)

        a6 = Action('Attack player', self.attack_player)

        a7 = Action('Shoot bullet', self.shoot_bullet)

        a8 = Action('End', self.end)

        chase_player = Sequence('Chase player', a1)

        c1 = Condition('teleport 쿨타임이 지났는가?', self.is_teleport_available)
        c2 = Condition('체력이 0 이하인가?', self.if_hp_0)
        c3 = Condition('플레이어가 공격 거리 안에 있는가?', self.if_player_in_attack)
        c4 = Condition('체력이 절반 이하인가?', self.if_hp_half)

        attack_player = Sequence('Attack player', c3, a6)

        boss_death = Sequence('보스 죽음', c2, a5, a8)

        teleport_randomly = Sequence('랜덤 텔레포트', c1, a2, a3, a4, c4, a7)

        root = Selector(' ', boss_death, teleport_randomly, attack_player, chase_player)

        self.bt = BehaviorTree(root)