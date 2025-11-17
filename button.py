from pico2d import draw_rectangle

class Button:
    def __init__(self, left, bottom, right, top, button_type):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
        self.button_type = button_type

    def draw(self, r = 255, g = 255, b = 255, a = 255):
        draw_rectangle(self.left, self.bottom, self.right, self.top, r, g, b, a)

    def fill_draw(self, r = 255, g = 255, b = 255, a = 255):
        # 채워진 사각형: draw_rectangle을 여러 번 그려 채움 효과를 냄
        # 버튼 영역의 각 y에 대해 1픽셀 높이의 가로선을 그림
        y = self.bottom
        while y <= self.top:
            draw_rectangle(self.left, y, self.right, y + 1, r, g, b, a)
            y += 1