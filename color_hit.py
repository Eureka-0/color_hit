import sys
from tkinter import Tk, messagebox

from pygame.event import get as get_events

from utils import *
from views import GameView, Label, MenuView, os


class Game:
    def __init__(self):
        tkwindow = Tk()
        tkwindow.wm_withdraw()
        pg.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pg.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        pg.display.set_caption("Color Hit")
        pg.display.set_icon(get_image("color_hit_icon.png"))
        self.clock = pg.time.Clock()

        self.background, self.back_rect = get_back()
        self.view = MenuView(self.screen)
        self.view.start_button.set_callback(self.start_game)
        fps_size = Vector2(150, 30)
        self.current_fps = Label(
            self.screen, WINDOW_SIZE - fps_size, fps_size, "", fs=14, ta="left"
        )
        self.frame = 0  # 记录帧数

    def start_game(self):
        self.view = GameView(self.screen)

    def update_gameview(self, past_sec: float):
        game_over = self.view.update(past_sec)
        if game_over:
            retry = messagebox.askokcancel(message="Game over! Try again?")
            if retry:
                self.view = GameView(self.screen)
            else:
                self.view = MenuView(self.screen)
        else:
            self.view.draw()

    def update_frame(self):
        for event in get_events():
            if event.type == QUIT:
                if type(self.view) is GameView:
                    rewrite_best_score(self.view.score, self.view.best_score)
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                self.view.on_keydown(event)
            elif event.type == MOUSEBUTTONDOWN:
                self.view.on_mousedown(event)

        self.screen.blit(self.background, self.back_rect)
        past_sec = self.clock.tick(FPS) / 1000
        if type(self.view) is GameView:
            self.update_gameview(past_sec)
        elif type(self.view) is MenuView:
            self.view.update(past_sec)
            self.view.draw()
        self.frame += 1
        if self.frame % 20 == 0:
            self.current_fps.update(f"当前帧率(fps): {self.clock.get_fps():.2f}")
        self.current_fps.draw()
        pg.display.update()


if __name__ == "__main__":
    game = Game()
    while True:
        game.update_frame()
