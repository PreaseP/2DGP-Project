# python
import math
import random

from pico2d import *

import cockpit_mode
import common
import game_world
import game_framework
import relic_choice1
import relic_choice2
import userdata

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel
SCREEN_W = 1280
SCREEN_H = 720

class Relic:
    image = None

    def __init__(self, type = 0):
        if Relic.image == None:
            Relic.image = load_image('resources/sprites/relic' + str(type) + '.png')
        self.x = common.borders[4] - 100
        self.y = 360

        self.w = 100
        self.h = 100


    def update(self):
        pass

    def draw(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        self.image.draw(sx, sy, self.w, self.h)

        draw_rectangle(*(self.get_bb()))

    def get_bb(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        return sx - self.w/2, sy - self.h/2, sx + self.w/2, sy + self.h/2

    def handle_collision(self, group, other):
        if group == 'player:relic':
            if userdata.stageClear == 0:
                userdata.stageClear = 1
                game_framework.change_mode(relic_choice1)
            elif userdata.stageClear == 1:
                userdata.stageClear = 2
                game_framework.change_mode(relic_choice2)




