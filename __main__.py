import sys
from math import cos, radians, sin
from random import random
from tkinter import Tk, messagebox

from utils import *
from views import GameView, Label, os


def get_back() -> tuple[Surface, Rect]:
    background = get_image("background.png", WINDOW_SIZE)
    theta = random() * 360
    scale = random() + abs(cos(radians(theta))) + abs(sin(radians(theta)))
    back = pg.transform.rotozoom(background, theta, scale)
    back_rect = back.get_rect(center=WINDOW_SIZE / 2)
    return back, back_rect


def run_game():
    tkwindow = Tk()
    tkwindow.wm_withdraw()
    pg.init()
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pg.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])
    get_events = pg.event.get
    screen = pg.display.set_mode(WINDOW_SIZE)
    pg.display.set_caption("Color Hit")
    pg.display.set_icon(get_image("color_hit_icon.png"))
    clock = pg.time.Clock()

    background, back_rect = get_back()
    view = GameView(screen)
    fps_size = Vector2(150, 30)
    current_fps = Label(screen, WINDOW_SIZE - fps_size, fps_size, "", fs=14, ta="left")
    frame = 0  # 记录帧数

    while True:
        for event in get_events():
            if event.type == QUIT:
                if type(view) is GameView:
                    if view.score > view.best_score:
                        view.rewrite_best_score()
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                view.on_keydown(event)
            elif event.type == MOUSEBUTTONDOWN:
                view.on_mousedown(event)

        screen.blit(background, back_rect)
        past_sec = clock.tick(FPS) / 1000
        if type(view) is GameView:
            game_over = view.update(past_sec)
            if game_over:
                retry = messagebox.askokcancel(message="Game over! Try again?")
                if retry:
                    view = GameView(screen)
                else:
                    pg.quit()
                    sys.exit()
        else:
            view.update(past_sec)
        frame += 1
        if frame % 20 == 0:
            current_fps.update_content(f"当前帧率(fps): {clock.get_fps():.2f}")
        current_fps.update()
        pg.display.update()


if __name__ == "__main__":
    run_game()
