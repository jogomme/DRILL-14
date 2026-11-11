from pico2d import *
import game_world
import game_framework
from bird import Bird, DRAW_HEIGHT, DRAW_WIDTH, FRAME_COUNT
from boy import Boy
from grass import Grass

BIRD_COUNT = 10

boy = None
birds = []


def handle_events():


    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy, birds

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)

    left_bound = DRAW_WIDTH / 2
    right_bound = get_canvas_width() - DRAW_WIDTH / 2
    lane_count = max(1, int(get_canvas_height() / (DRAW_HEIGHT * 1.5)))
    lane_spacing = get_canvas_height() / (lane_count + 1)
    flight_width = right_bound - left_bound
    birds = []

    for index in range(BIRD_COUNT):
        bird = Bird(
            left_bound + flight_width * (index + 0.5) / BIRD_COUNT,
            lane_spacing * (index % lane_count + 1),
            speed=80.0 + (index % 4) * 15.0,
            direction=1 if index % 2 == 0 else -1,
            frame=FRAME_COUNT * index / BIRD_COUNT,
            left_bound=left_bound,
            right_bound=right_bound,
        )
        birds.append(bird)
        game_world.add_oject(bird)


def pause():
    boy.pause()


def resume():
    pass


def finish():
    global boy, birds
    game_world.clear()
    boy = None
    birds = []


def update():
    game_world.update()

def render():
    clear_canvas()
    game_world.render()
    update_canvas()







