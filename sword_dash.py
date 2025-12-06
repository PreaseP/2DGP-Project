from pico2d import *
import game_world
import game_framework
import common
import userdata

TIME_PER_ATTACK = 0.2
ATTACK_PER_TIME = 1.0 / TIME_PER_ATTACK
FRAMES_PER_ATTACK = 5


sprite = (
    0, 49, 98, 147, 196
)

class DashEffect:
    image = None
    def __init__(self, atk = 10):
        self.x = common.player.x - common.player.face_dir * 130
        self.y = common.player.y
        self.frame = 0.0
        self.atk = atk
        self.w = 200
        self.h = 80
        self.atk_available = True
        self.face_dir = common.player.face_dir

        if DashEffect.image == None:
            DashEffect.image = load_image('resources/sprites/sword_dash_effect.png')

    def draw(self):
        sx = self.x - common.map.window_left  # 화면상의 x 위치
        sy = self.y - common.map.window_bottom

        if self.face_dir == 1:  # right
            DashEffect.image.clip_composite_draw(sprite[int(self.frame)], 0,
                                             48, 20, 0, ' ', sx, sy, self.w, self.h)
        else:  # face_dir == -1: # left
            DashEffect.image.clip_composite_draw(sprite[int(self.frame)], 0,
                                             48, 20, 0, 'h', sx, sy, self.w, self.h)

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
        if group == 'nonBullet:monster' and other.protect == False and self.atk_available == True:
            if userdata.playerSkill['sword'][1] == 2:
                if common.player.dash_time > 0.0:
                    common.player.dash_time -= 0.5

                if common.player.hp < userdata.maxHealth:
                    common.player.hp += 1
                    if common.player.hp > userdata.maxHealth:
                        common.player.hp = userdata.maxHealth



