import random
import math
import game_framework
import game_world

from pico2d import *

# slime Action Speed
TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

slime_sprite = [
    [(0, 26), (26, 26), (54, 26), (80, 26)],
    [(0, 80), (26, 80), (54, 80), (80, 81)],
    [(0, 136), (26, 136), (54, 136), (80, 137)]
]

slime_size = (26, 28)

class Slime:
    image = None

    def __init__(self):
        self.x, self.y = random.randint(0 + 100, 1280 - 100), random.randint(0 + 70, 720 - 70)
        if Slime.image == None:
            Slime.image = load_image("resources/sprites/farming_slimes.png")
        self.frame = random.randint(0, 3)
        self.type = random.randint(0, 2)
        self.dir = random.choice([-1,1])
        self.xdir = self.ydir = 0
        if random.randint(0, 10) < 5:
            self.xdir = self.dir
        else:
            self.ydir = random.choice([-1, 1])
        self.move_timer = 0.0

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 30

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.xdir * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.ydir * RUN_SPEED_PPS * game_framework.frame_time
        self.move_timer += game_framework.frame_time
        if self.move_timer >= 2.0:
            if self.xdir or self.ydir:
                self.xdir = self.ydir = 0
            else:
                if random.randint(0, 10) < 5:
                    self.dir = random.choice([-1, 1])
                    self.xdir = self.dir
                    self.move_timer = 0.0
                else:
                    self.ydir = random.choice([-1,1])
                    self.move_timer = 0.0

        if self.xdir:
            if self.x < 0 + 50 or self.x > 1280 - 50:
                self.xdir *= -1
                self.dir *= -1
        if self.ydir:
            if self.y < 0 + 50 or self.y > 720 - 50:
                self.ydir *= -1

    def draw(self):
        sprite_x = slime_sprite[self.type][int(self.frame)][0]
        sprite_y = slime_sprite[self.type][int(self.frame)][1]

        if self.dir > 0:
            Slime.image.clip_composite_draw(sprite_x, sprite_y, slime_size[0], slime_size[1],
                                       0, 'h', self.x, self.y, 75, 75)
        else:
            Slime.image.clip_composite_draw(sprite_x, sprite_y, slime_size[0], slime_size[1],
                                       0, ' ', self.x, self.y, 75, 75)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'sword:monster' and other.frame < 1.0:
            game_world.remove_object(self)

