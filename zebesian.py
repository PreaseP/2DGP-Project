from pico2d import *

import random
import math

import common
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from damage_font import DamageFont

# Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 6.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Walk
TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8.0

# Attack
TIME_PER_ATTACK = 0.7
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 12.0

animationNames = {'Walk' : 0, 'Attack' : 1}

sprites = [
    [(0, 704), (73, 704), (146, 704), (219, 704), (292, 704), (365, 704), (438, 704), (511, 704)],
    [(0, 530), (73, 530), (146, 530), (219, 530), (292, 530), (365, 530),
     (438, 530), (511, 530), (584, 530), (657, 530), (730, 530), (803, 530)]
]

size = [(73, 58), (73, 58)]

class Zebesian:
    image = None

    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(common.borders[common.map.left_border] - 50, common.borders[common.map.right_border] + 50)
        self.y = y if y else random.choice([random.randint(-50, -30), random.randint(720 + 30, 720 + 50)])
        self.w = 90
        self.h = 90

        self.r = 1.8

        self.hp = 350

        if Zebesian.image == None:
            Zebesian.image = load_image('resources/sprites/relic2_zebesian.png')

        self.dir = 0.0      # radian 값으로 방향을 표시
        self.frame = random.randint(0, 8)
        self.state = 'Walk'

        self.protect_timer = 0.0
        self.protect = False

        self.build_behavior_tree()


    def get_bb(self):
        sx = self.x - common.map.window_left
        sy = self.y - common.map.window_bottom

        return sx - self.w / 2 + 15, sy - self.h / 2 + 5, sx + self.w / 2 - 10, sy + self.h /2


    def update(self):
        self.bt.run()  # 매 프레임마다 행동트리를 root부터 시작해서 실행함.

        if self.state == 'Walk':
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        elif self.state == 'Attack':
            self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time) % FRAMES_PER_ATTACK

        if self.protect:
            self.protect_timer -= game_framework.frame_time
            if self.protect_timer <= 0:
                self.protect = False

    def draw(self):
        sx = self.x - common.map.window_left
        sy = self.y - common.map.window_bottom

        if math.cos(self.dir) < 0:
            Zebesian.image.clip_composite_draw(sprites[animationNames[self.state]][int(self.frame)][0],
                                           sprites[animationNames[self.state]][int(self.frame)][1],
                                           size[animationNames[self.state]][0], size[animationNames[self.state]][1], 0, ' ', sx - 10, sy, self.w, self.h)
        else:
            Zebesian.image.clip_composite_draw(sprites[animationNames[self.state]][int(self.frame)][0],
                                           sprites[animationNames[self.state]][int(self.frame)][1],
                                           size[animationNames[self.state]][0], size[animationNames[self.state]][1], 0, 'h', sx + 10, sy, self.w, self.h)

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
        if self.distance_less_than(common.player.x, common.player.y, self.x, self.y, self.r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def if_player_in_attack(self):
        if self.distance_less_than(common.player.x, common.player.y, self.x, self.y, self.r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def attack_player(self):
        # 공격 상태 진입
        if self.state != 'Attack':
            self.state = 'Attack'
            self.frame = 0

        # 공격 범위 안에 있는지 확인
        if self.distance_less_than(common.player.x, common.player.y, self.x, self.y, self.r):
            # 애니메이션이 끝났는지 확인
            if self.frame >= FRAMES_PER_ATTACK - 0.1:
                self.frame = 0  # 프레임 초기화 후 반복
            return BehaviorTree.SUCCESS
        else:
            self.frame = 0
            return BehaviorTree.FAIL

    def build_behavior_tree(self):
        # 목표 지점을 설정하는 액션 노드를 생성.
        a1 = Action('Move to player', self.move_to_player)
        a2 = Action('Attack player', self.attack_player)

        chase_player = Sequence('Chase player', a1)

        c1 = Condition('플레이어가 공격 거리 안에 있는가?', self.if_player_in_attack)

        attack_player = Sequence('플레이어 공격(공격 거리 안에 있으면)', c1, a2)

        root = attack_or_chase_player = Selector('공격 아니면 추적', attack_player, chase_player)

        self.bt = BehaviorTree(root)