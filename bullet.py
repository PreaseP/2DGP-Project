# python
import math
from pico2d import *
import game_world
import game_framework
import userdata

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel
SCREEN_W = 1280
SCREEN_H = 720

class Bullet:
    image = None

    def __init__(self, x, y, target_x, target_y, speed = 15, atk = 10):
        if Bullet.image == None:
            Bullet.image = load_image('resources/sprites/bullet.png')
        self.x = x
        self.y = y
        self.atk = atk
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            self.vx, self.vy = 0, 0
        else:
            self.vx = dx / dist * speed
            self.vy = dy / dist * speed
        self.w = 25
        self.h = 25
        self.to_remove = False

    def update(self):
        dt = game_framework.frame_time
        self.x += self.vx * dt * PIXEL_PER_METER
        self.y += self.vy * dt * PIXEL_PER_METER

        # 화면 밖으로 나가면 삭제
        if self.x < -50 or self.x > SCREEN_W + 50 or self.y < -50 or self.y > SCREEN_H + 50:
            try:
                game_world.remove_object(self)
            except Exception:
                pass

    def draw(self):
        self.image.draw(self.x, self.y, 25, 25)

        draw_rectangle(self.x - self.w/2, self.y - self.h/2,
                       self.x + self.w/2, self.y + self.h/2)

    def get_bb(self):
        return self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2

    def handle_collision(self, group, other):
        if group == 'bullet:monster':
            if userdata.playerWeapon['gun'][0] == 1 and userdata.playerWeapon['gun'][1] == 5:
                pass
            else:
                game_world.remove_object(self)

