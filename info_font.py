from pico2d import *
import game_world
import game_framework

class InfoFont:

    def __init__(self, x = 400, y = 300, message = ''):
        self.x, self.y = x, y
        self.font = load_font('resources/DungGeunMo.TTF', 30)
        self.print_timer = 1.0
        self.message = message
    def draw(self):
        self.font.draw(self.x, self.y, self.message, (255,0,0))

    def update(self):
        if self.print_timer > 0.0:
            self.print_timer -= game_framework.frame_time
            if self.print_timer <= 0.0:
                game_world.remove_object(self)
