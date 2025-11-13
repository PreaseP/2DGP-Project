from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 0.2  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class DamageFont:

    def __init__(self, left = 0, bottom = 0, x = 400, y = 300, damage = 0):
        self.x, self.y = x, y
        self.font = load_font('resources/DungGeunMo.TTF', 30)
        self.print_timer = 0.6
        self.damage = damage
    def draw(self):
        self.font.draw(self.x, self.y, f'{self.damage}', (255,0,0))

    def update(self):
        # 위치 업데이트
        if self.print_timer > 0.0:
            self.print_timer -= game_framework.frame_time
            self.y += RUN_SPEED_PPS * game_framework.frame_time * PIXEL_PER_METER
            if self.print_timer < 0.0:
                game_world.remove_object(self)



