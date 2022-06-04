import sys
import os

import pygame as pg

from config import *
from views import GameView

background = "#717171"


def run_game():
    pg.init()
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Color Hit")
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN])
    view = GameView(screen)
    clock = pg.time.Clock()
    run = True
    frame = 0

    while run:
        # frame += 1
        # if frame % 40 == 0:
        #     view.pin.mode = SHOOT

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                view.on_keydown(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                view.on_mousedown(event)

        screen.fill(background)
        view.update()
        pg.display.update()
        clock.tick(FPS)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    run_game()
