import os
import sys
from math import cos, radians, sin
from random import random

from views import *


def get_back() -> tuple[Surface, Rect]:
    background = get_image("background.png", WINDOW_SIZE)
    theta = random() * 360
    scale = random() + abs(cos(radians(theta))) + abs(sin(radians(theta)))
    back = pg.transform.rotozoom(background, theta, scale)
    back_rect = back.get_rect(center=WINDOW_SIZE / 2)
    return back, back_rect


def run_game():
    pg.init()
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pg.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])
    get_events = pg.event.get

    screen = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("Color Hit")
    background, back_rect = get_back()
    view = GameView(screen)
    fps_size = Vector2(140, 40)
    current_fps = Label(screen, WINDOW_SIZE - fps_size, fps_size, "", fontsize=14)
    button = Button(screen, (10, 10), (100, 50), "开始")
    clock = pg.time.Clock()
    frame = 0  # 记录帧数

    while True:
        for event in get_events():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                view.on_keydown(event)
            elif event.type == MOUSEBUTTONDOWN:
                view.on_mousedown(event)

        screen.blit(background, back_rect)
        button.update()
        view.update()
        frame += 1
        if frame % 20 == 0:
            current_fps.update(f"当前帧率:{clock.get_fps():.2f}fps")
        else:
            current_fps.update()
        pg.display.update()

        s = clock.tick(FPS) / 1000
        # print(frame, ":", s)


if __name__ == "__main__":
    run_game()
