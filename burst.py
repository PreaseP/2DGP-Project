# python
import math
from pico2d import *
import game_world
import game_framework
import userdata
import common

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 4

effect_sprites = (0, 53, 106, 159)

class Burst:
    image = None

    def __init__(self, x, y, target_x, speed = 10, face_dir = 1, xdir = 0, atk = 10):
        if Burst.image == None:
            Burst.image = load_image('resources/sprites/gun_skill2_effect.png')
        self.x, self.y, self.face_dir, self.xdir = x, y, face_dir, xdir
        if self.xdir == 0:
            self.x += self.face_dir * 75
        self.frame = 0
        self.atk = atk
        self.dx = target_x - x

        dist = math.hypot(self.dx, 0.0)
        if dist == 0:
            self.vx = 0
        else:
            self.vx = self.dx / dist * speed
        self.w = 100
        self.h = 100

    def update(self):
        dt = game_framework.frame_time
        self.x += self.vx * dt * PIXEL_PER_METER

        self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time)
        # self.frame = 3
        if self.frame >= FRAMES_PER_ATTACK:
            game_world.remove_object(self)

    def draw(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        if self.xdir == 0:
            if self.face_dir == 1:  # right
                self.image.clip_composite_draw(effect_sprites[int(self.frame)], 0, 52, 33, 0, ' ', sx, sy, self.w, self.h)
            else:
                self.image.clip_composite_draw(effect_sprites[int(self.frame)], 0, 52, 33, 0, 'h', sx, sy, self.w, self.h)
        elif self.xdir == 1:
            self.image.clip_composite_draw(effect_sprites[int(self.frame)], 0, 52, 33, 0, ' ', sx, sy, self.w, self.h)
        else:
            self.image.clip_composite_draw(effect_sprites[int(self.frame)], 0, 52, 33, 0, 'h',  sx, sy, self.w, self.h)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        return sx - self.w/2, sy - self.h/2, sx + self.w/2, sy + self.h/2

    def handle_collision(self, group, other):
        pass

