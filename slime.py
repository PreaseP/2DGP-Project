import random
import math
import game_framework
import game_world

from pico2d import *

# slime Action Speed
TIME_PER_ACTION = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0

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

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 30

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

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

