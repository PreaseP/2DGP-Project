# python
import math
from pico2d import *
import game_world
import game_framework
import userdata

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 4

SCREEN_W = 1280
SCREEN_H = 720

effect_sprites = (0, 40, 80, 120)

class Burst:
    image = None

    def __init__(self, x = 400, y = 300, face_dir = 1, xdir = 0, atk = 10):
        if Burst.image == None:
            Burst.image = load_image('resources/sprites/gun_skill2_effect.png')
        self.x, self.y, self.face_dir, self.xdir = x, y, face_dir, xdir
        if self.xdir == 0:
            self.x += self.face_dir * 80
        self.frame = 0
        self.atk = atk
        self.w = 75
        self.h = 75

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time)
        if self.frame >= FRAMES_PER_ATTACK:
            game_world.remove_object(self)

    def draw(self):
        if self.xdir == 0:
            if self.face_dir == 1:  # right
                self.image.clip_composite_draw(effect_sprites[int(self.frame)], 0, 60, 32, 0, ' ', self.x, self.y, self.w, self.h)
            else:
                self.image.clip_composite_draw(effect_sprites[int(self.frame)], 0, 60, 32, 0, 'h', self.x, self.y, self.w, self.h)
        elif self.xdir == 1:
            self.image.clip_composite_draw(effect_sprites[int(self.frame)], 0, 60, 32, 0, ' ', self.x, self.y, self.w, self.h)
        else:
            self.image.clip_composite_draw(effect_sprites[int(self.frame)], 0, 60, 32, 0, 'h',  self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2

    def handle_collision(self, group, other):
        pass

