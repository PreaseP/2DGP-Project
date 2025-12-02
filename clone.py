# python
import math
from pico2d import *
import game_world
import game_framework
import userdata
import common

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel
SCREEN_W = 1280
SCREEN_H = 720

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 6

sprite = (
    0, 79, 158, 237, 316, 395
)

class sClone:
    image = None

    def __init__(self, x, y, target_x, target_y, speed = 10, atk = 10):
        if sClone.image == None:
            sClone.image = load_image('resources/sprites/sword_skill3_effect.png')
        self.x = x
        self.y = y
        self.frame = 0
        self.atk = atk
        self.dx = target_x
        self.dy = target_y - y
        self.face_dir = common.player.face_dir
        self.duration = 0.0
        dist = math.hypot(self.dx, self.dy)
        if dist == 0:
            self.vx, self.vy = 0, 0
        else:
            self.vx = self.dx / dist * speed
            self.vy = self.dy / dist * speed
        self.w = 150
        self.h = 125

    def update(self):
        dt = game_framework.frame_time
        self.x += self.vx * dt * PIXEL_PER_METER
        self.y += self.vy * dt * PIXEL_PER_METER
        if self.frame >= 1.5 and self.duration < 0.5:
            self.duration += dt
        else:
            self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * dt)

        if self.frame >= FRAMES_PER_ATTACK:
            game_world.remove_object(self)

    def draw(self):
        if 1.5 <= self.frame < 2.0:
            if self.face_dir == 1:  # right
                sClone.image.clip_composite_draw(sprite[int(self.frame)] + 31, 0,
                                                 47, 44, 0, ' ', self.x + 25, self.y, self.w - 50, self.h)
            else:  # face_dir == -1: # left
                sClone.image.clip_composite_draw(sprite[int(self.frame)] + 31, 0,
                                                 47, 44, 0, 'h', self.x - 25, self.y, self.w - 50, self.h)
        else:
            if self.face_dir == 1:  # right
                sClone.image.clip_composite_draw(sprite[int(self.frame)], 0,
                                                             78, 44, 0, ' ', self.x, self.y, self.w, self.h)
            else:  # face_dir == -1: # left
                sClone.image.clip_composite_draw(sprite[int(self.frame)], 0,
                                                             78, 44, 0, 'h', self.x, self.y, self.w, self.h)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.face_dir == 1:  # right
            return self.x - self.w/2 + 50, self.y - self.h/2 + 10, self.x + self.w/2 + 5, self.y + self.h/2 - 25
        else:  # face_dir == -1: # left
            return self.x - self.w/2 - 5, self.y - self.h/2 + 10, self.x + self.w/2 - 50, self.y + self.h/2 - 25

    def handle_collision(self, group, other):
        pass

