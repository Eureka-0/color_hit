from random import randint

import config as c
import pygame as pg
from config import Grid
from pygame.sprite import collide_mask

from src.typing_lib import *
from src.utils import get_image, ordered_colors, read_best_score, rewrite_best_score
from src.widgets import *


class View:
    def __init__(self, screen: Surface):
        self.screen = screen

    def on_keydown(self, event: Event):
        ...

    def on_mousedown(self, event: Event):
        ...

    def get_widgets(self) -> Iterator[Union[Sprite, Group]]:
        for v in self.__dict__.values():
            if isinstance(v, (Sprite, Group)):
                yield v

    def draw(self):
        for widget in self.get_widgets():
            widget.draw()  # type: ignore


class MenuView(View):
    def __init__(self, screen: Surface):
        super().__init__(screen)
        self.icon_img = get_image("color_hit_icon.png", (300, 300))
        self.icon_rect = self.icon_img.get_rect(
            centerx=Grid.WINDOW_SIZE[0] / 2, centery=200
        )
        self.start_button = Button(screen, Grid.START_POS, Grid.START_SIZE, "开始")

        setting_pos = Grid.START_POS + Vector2(0, 90)
        self.setting_button = Button(screen, setting_pos, Grid.START_SIZE, "设置")

        quit_pos = Grid.START_POS + Vector2(0, 180)
        self.quit_button = Button(screen, quit_pos, Grid.START_SIZE, "退出")

    def on_mousedown(self, event: Event):
        if event.button == pg.BUTTON_LEFT:
            self.start_button.check_click(event)
            self.setting_button.check_click(event)
            self.quit_button.check_click(event)

    def update(self, past_sec: float):
        self.start_button.update()
        self.setting_button.update()
        self.quit_button.update()

    def draw(self):
        self.screen.blit(self.icon_img, self.icon_rect)
        super().draw()


def group_bullets(screen: Surface, colors: list[str]) -> OrderedGruop:
    bullets = OrderedGruop(screen)
    for i, color in enumerate(colors):
        pos = (Grid.BULLETS_POS[0], Grid.BULLETS_POS[1] - 3 * i * Grid.BULLET_SIZE[1])
        bullets.add(Bullet(screen, color, pos))
    return bullets


def group_heart_label(screen: Surface) -> OrderedGruop:
    hearts = OrderedGruop(screen)
    for i in range(3):
        pos = (Grid.HEARTS_POS[0], Grid.HEARTS_POS[1] + i * Grid.HEART_SIZE[0])
        hearts.add(Label(screen, pos, Grid.HEART_SIZE, img_name="heart.png"))
    return hearts


def check_hit(pin: Pin, disc: Disc) -> Union[None, bool, Bonus]:
    collision = None
    for sprite in disc:
        if collide_mask(pin, sprite):
            collision = sprite
            break
    if type(collision) is Pie:
        if pin.color == collision.color:
            return True
        else:
            return False
    elif isinstance(collision, (Pin, Balk)):
        return False
    elif isinstance(collision, Bonus):
        return collision


class GameView(View):
    def __init__(self, screen: Surface):
        super().__init__(screen)
        self.hearts = group_heart_label(screen)
        self.best_score = read_best_score()
        self.best_score_board = Label(
            screen,
            Grid.BEST_SCORE_POS,
            Grid.BEST_SCORE_SIZE,
            f"历史最高  {self.best_score}",
        )
        self.best_score_board.set_style(font="FZPSZHUNHJW.TTF", fs=16, fc=c.TEXT_BLUE)
        self.score = 0
        self.score_board = Label(
            screen, Grid.SCORE_POS, Grid.SCORE_SIZE, f"{self.score}"
        )
        self.score_board.set_style(font="TabletGothicBold.OTF", fs=20)

        self.pause = False
        self.pause_button = Button(
            screen,
            Grid.PAUSE_POS,
            Grid.PAUSE_SIZE,
            img_name="pause.png",
            r=Grid.PAUSE_SIZE[0] / 2,
            callback=self.switch_pause,
        )

        self.level = 1
        self.init_level()

    def switch_pause(self):
        if self.pause:
            self.pause = False
            self.pause_button.update(img_name="pause.png")
        else:
            self.pause = True
            self.pause_button.update(img_name="go_on.png")

    def init_level(self):
        self.colors = ordered_colors(self.level)
        self.pin = Pin(self.screen, self.colors[-1])
        self.disc = Disc(self.screen, self.colors, self.level)
        if hasattr(self.disc, "hearts"):
            for heart in self.disc.hearts:
                heart.set_bonusfunc(self.plus_one_heart)
        self.bullets = group_bullets(self.screen, self.colors)
        self.colors.pop()

    def plus_one_heart(self):
        num = len(self.hearts)
        if num < 5:
            pos = (Grid.HEARTS_POS[0], Grid.HEARTS_POS[1] + num * Grid.HEART_SIZE[0])
            self.hearts.add(
                Label(self.screen, pos, Grid.HEART_SIZE, img_name="heart.png")
            )

    def on_keydown(self, event: Event):
        if not self.pause and event.key == pg.K_SPACE and self.pin.mode == c.STILL:
            self.pin.mode = c.SHOOT
            self.bullets.pop_widget()

    def on_mousedown(self, event: Event):
        if event.button == pg.BUTTON_LEFT:
            click = self.pause_button.check_click(event)
            if not click and not self.pause and self.pin.mode == c.STILL:
                self.pin.mode = c.SHOOT
                self.bullets.pop_widget()

    def next_pin(self):
        if len(self.colors) > 0:
            self.pin = Pin(self.screen, self.colors.pop())
        else:
            self.level += 1
            self.init_level()

    def update(self, past_sec: float) -> bool:
        if self.pause:
            self.pause_button.update()
            return False
        else:
            if self.pin.rect.top >= Grid.WINDOW_SIZE[1]:
                self.next_pin()

            if len(self.hearts):
                if self.pin.mode == c.SHOOT:
                    collision = check_hit(self.pin, self.disc)
                    if collision is True:
                        self.pin.mode = c.PRICK
                        self.disc.add(self.pin)
                        self.score += randint(10, 15)
                        self.next_pin()
                    elif collision is False:
                        self.pin.mode = c.DROP
                        self.hearts.pop_widget()
                    elif type(collision) is Heart:
                        collision.on_hit()

                self.pin.update(past_sec)
                self.disc.update(past_sec)
                self.score_board.update(f"{self.score}")
                self.hearts.update()
                self.bullets.update()
                self.pause_button.update()
                return False
            else:
                rewrite_best_score(self.score, self.best_score)
                return True
