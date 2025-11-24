# python
import math
from pico2d import *
import game_world
import game_framework
import userdata

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel
SCREEN_W = 1280
SCREEN_H = 720

class Laser:
    image = None

    def __init__(self, x, y, target_x, target_y, speed = 25, atk = 10, w = 200, h = 100):
        if Laser.image == None:
            Laser.image = load_image('resources/sprites/gun_skill3_effect.png')
        self.x = x
        self.y = y
        self.atk = atk
        self.dx = target_x
        self.dy = target_y - y
        dist = math.hypot(self.dx, self.dy)
        if dist == 0:
            self.vx, self.vy = 0, 0
        else:
            self.vx = self.dx / dist * speed
            self.vy = self.dy / dist * speed
        self.w = w
        self.h = h

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
        self.image.draw(self.x, self.y, self.w, self.h)

        draw_rectangle(self.x - self.w/2, self.y - self.h/2,
                       self.x + self.w/2, self.y + self.h/2)

    def get_bb(self):
        return self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2

    def handle_collision(self, group, other):
        pass

