import os
from random import randint

import pygame as pg
from config import DROP, PRICK, SHOOT, STILL, Color, Grid, Setting
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
            centerx=Grid.window_size[0] / 2, centery=200
        )
        self.start_button = Button(screen, Grid.start_pos, Grid.start_size, "开始")

        setting_pos = Grid.start_pos + Vector2(0, 90)
        self.setting_button = Button(screen, setting_pos, Grid.start_size, "设置")

        quit_pos = Grid.start_pos + Vector2(0, 180)
        self.quit_button = Button(screen, quit_pos, Grid.start_size, "退出")

        pg.mixer.music.load(os.path.join("sounds", "happy_tune.wav"))
        pg.mixer.music.set_volume(0.2)

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
        pos = (Grid.bullets_pos[0], Grid.bullets_pos[1] - 3 * i * Grid.bullet_size[1])
        bullets.add(Bullet(screen, color, pos))
    return bullets


def group_heart_label(screen: Surface) -> OrderedGruop:
    hearts = OrderedGruop(screen)
    for i in range(2):
        pos = (Grid.hearts_pos[0], Grid.hearts_pos[1] + i * Grid.heart_size[0])
        hearts.add(Label(screen, pos, Grid.heart_size, img_name="heart.png"))
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
        self.setting = Setting()
        self.hearts = group_heart_label(screen)
        self.best_score = read_best_score()
        self.best_score_board = Label(
            screen,
            Grid.best_score_pos,
            Grid.best_score_size,
            f"历史最高  {self.best_score}",
        )
        self.best_score_board.set_style(font="FZPSZHUNHJW.TTF", fs=16, fc=Color.aqua)
        self.score = 0
        self.score_board = Label(
            screen, Grid.score_pos, Grid.score_size, f"{self.score}"
        )
        self.score_board.set_style(font="TabletGothicBold.OTF", fs=20)

        self.pause = False
        self.pause_button = Button(
            screen,
            Grid.pause_pos,
            Grid.pause_size,
            img_name="pause.png",
            r=Grid.pause_size[0] / 2,
            callback=self.switch_pause,
        )

        self.level = 1
        self.init_level()

        pg.mixer.music.load(os.path.join("sounds", "jazz.wav"))
        pg.mixer.music.set_volume(0.2)
        self.shoot_sound = pg.mixer.Sound(os.path.join("sounds", "shoot.wav"))
        self.shoot_sound.set_volume(0.2)
        self.win_sound = pg.mixer.Sound(os.path.join("sounds", "win.wav"))
        self.win_sound.set_volume(0.4)

    def switch_pause(self):
        if self.pause:
            self.pause = False
            self.pause_button.update(img_name="pause.png")
        else:
            self.pause = True
            self.pause_button.update(img_name="go_on.png")

    def init_level(self):
        if self.level > 1:
            self.win_sound.play()
        self.setting.change_speed()
        self.colors = ordered_colors(self.level, self.setting)
        self.pin = Pin(self.screen, self.colors[-1])
        self.disc = Disc(self.screen, self.colors, self.level)
        for bonus in self.disc.bonuses:
            if type(bonus) is Heart:
                bonus.set_bonusfunc(self.plus_one_heart)
            elif type(bonus) is Star:
                bonus.set_bonusfunc(self.plus_score)
        self.bullets = group_bullets(self.screen, self.colors)
        self.colors.pop()

    def plus_one_heart(self):
        num = len(self.hearts)
        if num < 3:
            pos = (Grid.hearts_pos[0], Grid.hearts_pos[1] + num * Grid.heart_size[0])
            self.hearts.add(
                Label(self.screen, pos, Grid.heart_size, img_name="heart.png")
            )

    def plus_score(self):
        self.score += randint(10, 15)

    def on_keydown(self, event: Event):
        if not self.pause and event.key == pg.K_SPACE and self.pin.mode == STILL:
            self.shoot_sound.play()
            self.pin.mode = SHOOT
            self.bullets.pop_widget()

    def on_mousedown(self, event: Event):
        if event.button == pg.BUTTON_LEFT:
            click = self.pause_button.check_click(event)
            if not click and not self.pause and self.pin.mode == STILL:
                self.shoot_sound.play()
                self.pin.mode = SHOOT
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
            if self.pin.rect.top >= Grid.window_size[1]:
                self.next_pin()

            if len(self.hearts):
                if self.pin.mode == SHOOT:
                    collision = check_hit(self.pin, self.disc)
                    if collision is True:
                        self.pin.mode = PRICK
                        self.disc.add(self.pin)
                        self.plus_score()
                        self.next_pin()
                    elif collision is False:
                        self.pin.mode = DROP
                        self.hearts.pop_widget()
                    elif isinstance(collision, Bonus):
                        collision.on_hit()

                self.pin.update(past_sec, self.setting)
                self.disc.update(past_sec, self.setting)
                self.score_board.update(f"{self.score}")
                self.hearts.update()
                self.bullets.update()
                self.pause_button.update()
                return False
            else:
                rewrite_best_score(self.score, self.best_score)
                return True
