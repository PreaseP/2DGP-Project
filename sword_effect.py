from pico2d import *
import game_world
import game_framework
import common

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 4

effect_sprites = [
    (0, 0, 20), (21, 0, 20), (42, 0, 20), (63, 0, 20)
]

class SwordEffect:
    image = None

    def __init__(self, x = 400, y = 300, face_dir = 1, xdir = 0, atk = 10):
        if SwordEffect.image == None:
            SwordEffect.image = load_image('resources/sprites/sword_hit_effect.png')
        self.x, self.y, self.face_dir, self.xdir = x, y, face_dir, xdir
        if self.xdir == 0:
            self.x += self.face_dir * 80
        self.frame = 0
        self.atk = atk
        self.w = 75
        self.h = 75
        self.atk_available = True

    def draw(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        if self.xdir == 0:
            if self.face_dir == 1:  # right
                self.image.clip_composite_draw(effect_sprites[int(self.frame)][0],
                                                   effect_sprites[int(self.frame)][1],
                                                   effect_sprites[int(self.frame)][2], 32, 0, ' ', sx,
                                                   sy, self.w, self.h)
            else:
                self.image.clip_composite_draw(effect_sprites[int(self.frame)][0],
                                                effect_sprites[int(self.frame)][1],
                                                effect_sprites[int(self.frame)][2], 32, 0, 'h', sx,
                                                sy, self.w, self.h)
        elif self.xdir == 1:
            self.image.clip_composite_draw(effect_sprites[int(self.frame)][0],
                                            effect_sprites[int(self.frame)][1],
                                            effect_sprites[int(self.frame)][2], 32, 0, ' ',
                                            sx, sy, self.w, self.h)
        else:
            self.image.clip_composite_draw(effect_sprites[int(self.frame)][0],
                                            effect_sprites[int(self.frame)][1],
                                            effect_sprites[int(self.frame)][2], 32, 0, 'h',
                                            sx, sy, self.w, self.h)

    def get_bb(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        return sx - self.w/2, sy - self.h/2, sx + self.w/2, sy + self.h/2

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time)
        if self.atk_available and self.frame >= 1.0:
            self.atk_available = False

        if self.frame >= FRAMES_PER_ATTACK:
            game_world.remove_object(self)

    def handle_collision(self, group, other):
        pass



