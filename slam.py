from pico2d import *
import game_world
import game_framework
import common

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 11

class Slam:
    def __init__(self, atk = 10):
        self.x = common.player.x
        self.y = common.player.y
        self.frame = 0
        self.atk = atk
        self.w = 340
        self.h = 220
        self.face_dir = common.player.face_dir
        self.atk_available = True

    def draw(self):
        pass

    def get_bb(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        return sx - self.w/2 + 30 * self.face_dir, sy - self.h/2 + 60, sx + self.w/2 + 30 * self.face_dir, sy + self.h/2 + 50

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time)

        if self.frame >= FRAMES_PER_ATTACK:
            game_world.remove_object(self)

    def handle_collision(self, group, other):
        pass



