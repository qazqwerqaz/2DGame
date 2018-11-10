import game_framework
from pico2d import *
import main_state

name = "TitleState"
image = None
mouse_x = 0
mouse_y = 0

def enter():
    global image
    image = load_image('ui\\title.png')
    pass


def exit():
    global image
    del(image)
    pass


def handle_events():
    events = get_events()
    global mouse_x, mouse_y
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif event.type == SDL_MOUSEBUTTONDOWN:
                if (mouse_x > 500 and mouse_x > 600 and mouse_y > 250 and mouse_y < 400):
                    game_framework.change_state(main_state)
            elif event.type == SDL_MOUSEMOTION:
                mouse_x, mouse_y = event.x, event.y




def draw():
    clear_canvas()
    image.draw(500, 300)
    update()
    update_canvas()
    pass


def update():
    global image
    if (mouse_x > 500 and mouse_x > 600 and mouse_y > 250 and mouse_y < 400):
        image = load_image('ui\\title_start.png')
    elif(mouse_x > 500 and mouse_x > 600 and mouse_y > 450 and mouse_y < 600):
        image = load_image('ui\\title_maptool.png')
    else:
        image = load_image('ui\\title.png')
    pass


def pause():
    pass


def resume():
    pass

