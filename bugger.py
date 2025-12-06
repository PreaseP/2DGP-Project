from pico2d import *

import random
import math

import common
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from damage_font import DamageFont
from zombie import animation_names

# Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 6.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Walk
TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0

animationNames = {'Walk' : 0}

sprites = [
    [(8, 128), (48, 128), (88, 128), (128, 128)]
]

size = [(32, 29)]

class Bugger:
    image = None

    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(common.borders[common.map.left_border] - 50, common.borders[common.map.right_border] + 50)
        self.y = y if y else random.choice([random.randint(-50, -30), random.randint(720 + 30, 720 + 50)])
        self.w = 60
        self.h = 60

        self.hp = 250

        self.speed = 1.0

        self.speed_timer = 4.0

        if Bugger.image == None:
            Bugger.image = load_image('resources/sprites/relic2_bugger.png')

        self.dir = 0.0      # radian 값으로 방향을 표시
        self.frame = random.randint(0, 4)
        self.state = 'Walk'

        self.protect_timer = 0.0
        self.protect = False

        self.build_behavior_tree()


    def get_bb(self):
        sx = self.x - common.map.window_left
        sy = self.y - common.map.window_bottom

        return sx - self.w / 2, sy - self.h / 2, sx + self.w / 2, sy + self.h /2


    def update(self):
        self.bt.run()  # 매 프레임마다 행동트리를 root부터 시작해서 실행함.

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        if self.protect:
            self.protect_timer -= game_framework.frame_time
            if self.protect_timer <= 0:
                self.protect = False

        if self.speed_timer > 0.0:
            self.speed_timer -= game_framework.frame_time
            if self.speed_timer < 0.0:
                self.speed_timer = 0.0

    def draw(self):
        sx = self.x - common.map.window_left
        sy = self.y - common.map.window_bottom

        if math.cos(self.dir) < 0:
            Bugger.image.clip_composite_draw(sprites[animationNames[self.state]][int(self.frame)][0],
                                           sprites[animationNames[self.state]][int(self.frame)][1],
                                           size[animationNames[self.state]][0], size[animationNames[self.state]][1], 0, ' ', sx, sy, self.w, self.h)
        else:
            Bugger.image.clip_composite_draw(sprites[animationNames[self.state]][int(self.frame)][0],
                                           sprites[animationNames[self.state]][int(self.frame)][1],
                                           size[animationNames[self.state]][0], size[animationNames[self.state]][1], 0, 'h', sx, sy, self.w, self.h)

        draw_rectangle(*self.get_bb())

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
        distance = RUN_SPEED_PPS * game_framework.frame_time * self.speed
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def move_to_player(self):
        self.state = 'Walk'
        self.move_little_to(common.player.x, common.player.y)
        if self.distance_less_than(common.player.x, common.player.y, self.x, self.y, 0.5):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def if_speed_cooltime(self):
        if self.speed_timer == 0.0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def increase_speed(self):
        if self.speed < 2.0:
            self.speed = 2.0
        else:
            self.speed = 1.0

        self.speed_timer = 4.0
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        # 목표 지점을 설정하는 액션 노드를 생성.
        a1 = Action('Move to player', self.move_to_player)
        a2 = Action('Increase speed', self.increase_speed)

        c1 = Condition('If speed cooltime', self.if_speed_cooltime)

        speed_boost = Sequence('Speed boost', c1, a2)

        chase_player = Sequence('Chase player', a1)

        root = Selector('Root', speed_boost, chase_player)

        self.bt = BehaviorTree(root)