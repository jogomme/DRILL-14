from pico2d import *
import game_world
import game_framework
from bird import Bird, DRAW_HEIGHT, DRAW_WIDTH, FRAME_COUNT
from boy import Boy
from grass import Grass

BIRD_COUNT = 1

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
    birds = [
        Bird(
            get_canvas_width() / 2,
            get_canvas_height() - DRAW_HEIGHT / 2,
            speed=90.0,
            direction=1,
            frame=0.0,
            left_bound=left_bound,
            right_bound=right_bound,
        )
    ]
    for bird in birds:
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








