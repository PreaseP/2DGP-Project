from pico2d import *
import game_world
import game_framework

TIME_PER_ATTACK = 0.5
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 4

effect_sprites = [
    (0, 0, 20), (21, 0, 20), (42, 0, 20), (63, 0, 20)
]

class SwordEffect:
    image = None

    def __init__(self, x = 400, y = 300, face_dir = 1, xdir = 0):
        if SwordEffect.image == None:
            SwordEffect.image = load_image('resources/sprites/sword_hit_effect.png')
        self.x, self.y, self.face_dir, self.xdir = x, y, face_dir, xdir
        if self.xdir == 0:
            self.x += self.face_dir * 80
        self.frame = 0

    def draw(self):
        if self.xdir == 0:
            if self.face_dir == 1:  # right
                self.image.clip_composite_draw(effect_sprites[int(self.frame)][0],
                                                   effect_sprites[int(self.frame)][1],
                                                   effect_sprites[int(self.frame)][2], 32, 0, ' ', self.x,
                                                   self.y, 75, 75)
            else:
                self.image.clip_composite_draw(effect_sprites[int(self.frame)][0],
                                                effect_sprites[int(self.frame)][1],
                                                effect_sprites[int(self.frame)][2], 32, 0, 'h', self.x,
                                                self.y, 75, 75)
        elif self.xdir == 1:
            self.image.clip_composite_draw(effect_sprites[int(self.frame)][0],
                                            effect_sprites[int(self.frame)][1],
                                            effect_sprites[int(self.frame)][2], 32, 0, ' ',
                                            self.x, self.y, 75, 75)
        else:
            self.image.clip_composite_draw(effect_sprites[int(self.frame)][0],
                                            effect_sprites[int(self.frame)][1],
                                            effect_sprites[int(self.frame)][2], 32, 0, 'h',
                                            self.x, self.y, 75, 75)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 40, self.x + 40, self.y + 40

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ATTACK * ATTACK_PER_TIME * game_framework.frame_time)
        if self.frame >= FRAMES_PER_ATTACK:
            game_world.remove_object(self)



