import os

import pygame as pg

from config import *
from views import GameView


def get_back():
    background = pg.image.load(os.path.join("img", "background.png")).convert_alpha()
    return pg.transform.smoothscale(background, WINDOW_SIZE)


def run_game():
    pg.init()
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    screen = pg.display.set_mode(WINDOW_SIZE)
    background = get_back()
    pg.display.set_caption("Color Hit")
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN])
    view = GameView(screen)
    clock = pg.time.Clock()
    run = True
    frame = 0  # 记录帧数

    while run:
        clock.tick(FPS)
        frame += 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                view.on_keydown(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                view.on_mousedown(event)

        screen.blit(background, (0, 0))
        view.update()
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    run_game()
