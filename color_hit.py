import os
import sys
from tkinter import Tk, messagebox

import pygame as pg
from pygame import KEYDOWN, MOUSEBUTTONDOWN, QUIT
from pygame.event import get as get_events

import config as c
from src.utils import get_back, get_image, quit_game, rewrite_best_score
from src.views import GameView, Label, MenuView


class Game:
    def __init__(self):
        tkwindow = Tk()
        tkwindow.wm_withdraw()
        pg.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pg.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])
        self.screen = pg.display.set_mode(c.WINDOW_SIZE)
        pg.display.set_caption("Color Hit")
        pg.display.set_icon(get_image("color_hit_icon.png"))
        self.clock = pg.time.Clock()

        self.init_menu()
        self.background, self.back_rect = get_back()
        fps_size = c.Vector2(150, 30)
        self.current_fps = Label(
            self.screen, c.WINDOW_SIZE - fps_size, fps_size, "", fs=14, ta="left"
        )
        self.frame = 0  # 记录帧数

    def init_menu(self):
        self.view = MenuView(self.screen)
        self.view.start_button.set_callback(self.init_game)
        self.view.quit_button.set_callback(quit_game)

    def init_game(self):
        self.view = GameView(self.screen)

    def update_gameview(self, past_sec: float):
        game_over = self.view.update(past_sec)
        if game_over:
            retry = messagebox.askokcancel(message="Game over! Try again?")
            if retry:
                self.view = GameView(self.screen)
            else:
                self.init_menu()
        else:
            self.view.draw()

    def update_frame(self):
        for event in get_events():
            if event.type == QUIT:
                if type(self.view) is GameView:
                    rewrite_best_score(self.view.score, self.view.best_score)
                quit_game()
            elif event.type == KEYDOWN:
                self.view.on_keydown(event)
            elif event.type == MOUSEBUTTONDOWN:
                self.view.on_mousedown(event)

        self.screen.blit(self.background, self.back_rect)
        past_sec = self.clock.tick(c.FPS) / 1000
        if type(self.view) is MenuView:
            self.view.update(past_sec)
            self.view.draw()
        elif type(self.view) is GameView:
            self.update_gameview(past_sec)

        self.frame += 1
        if self.frame % 20 == 0:
            self.current_fps.update(f"当前帧率(fps): {self.clock.get_fps():.2f}")
        self.current_fps.draw()
        pg.display.update()


if __name__ == "__main__":
    game = Game()
    while True:
        game.update_frame()
