# python
import math
import random

from pico2d import *

import common
import game_world
import game_framework
import userdata

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel
SCREEN_W = 1280
SCREEN_H = 720

class Bullet:
    image = None

    def __init__(self, x, y, target_x, target_y, speed = 15, atk = 10, piercing = False, heal = False):
        if Bullet.image == None:
            Bullet.image = load_image('resources/sprites/bullet.png')
        self.x = x
        self.y = y
        self.atk = atk
        self.dx = target_x - x
        self.dy = target_y - y
        dist = math.hypot(self.dx, self.dy)
        if dist == 0:
            self.vx, self.vy = 0, 0
        else:
            self.vx = self.dx / dist * speed
            self.vy = self.dy / dist * speed
        self.w = 25
        self.h = 25
        self.to_remove = False
        self.piercing = piercing
        self.heal = heal

    def update(self):
        dt = game_framework.frame_time
        self.x += self.vx * dt * PIXEL_PER_METER
        self.y += self.vy * dt * PIXEL_PER_METER

        # 화면 밖으로 나가면 삭제
        if self.x < -50 or self.x > common.map.w + 50 or self.y < -50 or self.y > common.map.h + 50:
            try:
                game_world.remove_object(self)
                game_world.remove_collision_object(self)
            except Exception:
                pass

    def draw(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        self.image.draw(sx, sy, 25, 25)

        draw_rectangle(*(self.get_bb()))

    def get_bb(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        return sx - self.w/2, sy - self.h/2, sx + self.w/2, sy + self.h/2

    def handle_collision(self, group, other):
        if group == 'bullet:monster':
            if self.heal:
                if common.player.hp < userdata.maxHealth:
                    common.player.hp += 1
                    if common.player.hp > userdata.maxHealth:
                        common.player.hp = userdata.maxHealth
                if common.player.slide_time > 0.0:
                    common.player.slide_time -= 1.0
            if self.piercing:
                pass
            else:
                try:
                    game_world.remove_object(self)
                    game_world.remove_collision_object(self)
                except Exception:
                    pass



