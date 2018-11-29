import game_framework
from pico2d import *
import title_state
import main_state
name = "PauseState"
image = None
logo_time = 10


def enter():
    global image
    image = load_image('pause.png')
    pass


def exit():
    global image
    del(image)
    pass


def update():
    global logo_time
    delay(0.1)
    logo_time += 1
    pass


def draw():
    global image
    clear_canvas()
    #main_state.draw()
    global logo_time

    if (logo_time >= 20):
        logo_time = 0


    image.draw(500, 300,1000,600)
    update_canvas()
    pass




def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
                game_framework.pop_state()


    pass


def pause(): pass


def resume(): pass




