import game_framework
from pico2d import get_canvas_width, load_image


SPRITE_PATH = 'bird_animation.png'
FRAME_WIDTH = 184
FRAME_HEIGHT = 169
FRAMES_PER_ROW = 5
FRAME_COUNT = 14
ANIMATION_FPS = 12.0
DRAW_WIDTH = 92
DRAW_HEIGHT = 85


class Bird:
    image = None

    def __init__(
        self, x, y, speed=0.0, direction=1, frame=0.0,
        left_bound=None, right_bound=None
    ):
        if direction not in (-1, 1):
            raise ValueError('direction must be -1 or 1')
        if speed < 0:
            raise ValueError('speed must not be negative')
        if (left_bound is not None and right_bound is not None and
                right_bound <= left_bound):
            raise ValueError('right_bound must be greater than left_bound')

        if Bird.image is None:
            Bird.image = load_image(SPRITE_PATH)

        self.x = float(x)
        self.y = float(y)
        self.speed = float(speed)
        self.direction = direction
        self.frame = float(frame) % FRAME_COUNT
        self.left_bound = (
            DRAW_WIDTH / 2 if left_bound is None else float(left_bound)
        )
        self.right_bound = (
            None if right_bound is None else float(right_bound)
        )

    def update(self):
        dt = game_framework.frame_time
        if dt < 0:
            raise ValueError('frame_time must not be negative')

        self.frame = (
            self.frame + ANIMATION_FPS * dt
        ) % FRAME_COUNT
        right_bound = (
            get_canvas_width() - DRAW_WIDTH / 2
            if self.right_bound is None else self.right_bound
        )
        span = right_bound - self.left_bound
        if span <= 0:
            raise ValueError('flight bounds must leave room for the bird')

        position = min(max(self.x, self.left_bound), right_bound)
        phase = (
            position - self.left_bound
            if self.direction > 0 else
            2 * span - (position - self.left_bound)
        )
        phase = (phase + self.speed * dt) % (2 * span)
        if phase < span:
            self.x = self.left_bound + phase
            self.direction = 1
        else:
            self.x = right_bound - (phase - span)
            self.direction = -1

    def draw(self):
        frame_index = int(self.frame) % FRAME_COUNT
        row, column = divmod(frame_index, FRAMES_PER_ROW)
        left = column * FRAME_WIDTH
        top = row * FRAME_HEIGHT
        width = min(FRAME_WIDTH, Bird.image.w - left)
        height = min(FRAME_HEIGHT, Bird.image.h - top)
        bottom = Bird.image.h - top - height

        flip = 'h' if self.direction < 0 else ''
        Bird.image.clip_composite_draw(
            left, bottom, width, height, 0, flip,
            self.x, self.y, DRAW_WIDTH, DRAW_HEIGHT
        )
