from pico2d import *
import game_world
import game_framework
import common

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 9

class Whirlwind:
    def __init__(self, atk = 10):
        self.x = common.player.x
        self.y = common.player.y
        self.frame = 0
        self.atk = atk
        self.w = 150
        self.h = 135
        self.face_dir = common.player.face_dir
        self.atk_available = True

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.w/2 - 10 * common.player.face_dir, self.y - self.h/2, self.x + self.w/2 - 10 * common.player.face_dir, self.y + self.h/2

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time)
        self.x = common.player.x
        self.y = common.player.y
        if self.atk_available and self.frame >= 6.0:
            self.atk_available = False

        if self.frame >= FRAMES_PER_ATTACK:
            game_world.remove_object(self)

    def handle_collision(self, group, other):
        pass



