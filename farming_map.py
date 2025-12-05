from pico2d import load_image, get_canvas_width, get_canvas_height, clamp
import common

class FarmingMap:
    def __init__(self):
        self.image = load_image('resources/background/farming.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def update(self):
        self.window_left = clamp(0, int(common.player.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(common.player.y) - self.ch // 2, self.h - self.ch - 1)

        common.player.x = clamp(50, common.player.x, common.map.w - 50)
        common.player.y = clamp(50, common.player.y, common.map.h - 50)

    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom, self.cw, self.ch,
            0, 0 # 캔버스의 왼쪽 아래 코너에 그리기
        )

    def handle_event(self, event):
        pass

