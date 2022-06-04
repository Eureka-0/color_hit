from functools import reduce
from random import randint, shuffle, sample

import pygame as pg

from config import *
from widgets import Disc, Pie, Pin, Bullets


def collide_mask(sprite1, sprite2):
    return False if pg.sprite.collide_mask(sprite1, sprite2) is None else True


def expand_colors(colors: list[str], num: list[int]):
    expand = reduce(lambda x, y: x + y, [[color] * n for n, color in zip(num, colors)])
    shuffle(expand)
    return expand


def rand_colors(num: int) -> list[str]:
    if 1 <= num <= 4:
        colors = [RED, GREEN, ORANGE, PURPLE]
        shuffle(colors)
        return colors[0:num]
    else:
        return ["#000000"]


def rand_num(n):
    sam = [0] + sample(range(1, PIN_NUM), n - 1) + [PIN_NUM]
    sam.sort()
    num = [sam[i + 1] - sam[i] for i in range(n)]
    upper = round(PIN_NUM * 3 / (n + 2))
    while max(num) > upper:
        sam = [0] + sample(range(1, PIN_NUM), n - 1) + [PIN_NUM]
        sam.sort()
        num = [sam[i + 1] - sam[i] for i in range(n)]
    return num


def get_ordered_colors(level: int) -> list[str]:
    if 1 <= level <= 2:
        colors = rand_colors(1)
        num = [randint(2 * level + 1, 2 * level + 3)]
    elif 3 <= level <= 4:
        colors = rand_colors(2)
        num = rand_num(2)
    elif 5 <= level <= 7:
        colors = rand_colors(3)
        num = rand_num(3)
    else:
        colors = rand_colors(4)
        num = rand_num(4)
    return expand_colors(colors, num)


class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.level = 8
        self.init_level()

    def init_level(self):
        self.colors = get_ordered_colors(self.level)
        self.pin = Pin(self.screen, self.colors[-1])
        self.disc = Disc(self.screen, self.colors)
        self.bullets = Bullets(self.screen, self.colors)
        self.colors.pop()

    def on_keydown(self, event):
        if event.key == pg.K_SPACE and self.pin.mode == STILL:
            self.pin.mode = SHOOT
            self.bullets.number -= 1

    def on_mousedown(self, event):
        if event.button == pg.BUTTON_LEFT and self.pin.mode == STILL:
            self.pin.mode = SHOOT
            self.bullets.number -= 1

    def next_pin(self):
        if len(self.colors) > 0:
            self.pin = Pin(self.screen, self.colors.pop())
        else:
            self.level += 1
            self.init_level()

    def get_widgets(self):
        widgets = []
        for v in self.__dict__.values():
            if isinstance(v, (pg.sprite.Sprite, pg.sprite.Group)):
                widgets.append(v)
        return widgets

    def update(self):
        if self.pin.rect.top >= HEIGHT:
            self.next_pin()

        collision = pg.sprite.spritecollideany(self.pin, self.disc, collide_mask)
        if isinstance(collision, Pie):
            if self.pin.color == collision.color:
                self.pin.mode = PRICK
                self.disc.add(self.pin)
                self.next_pin()
            else:
                self.pin.mode = DROP
        elif isinstance(collision, Pin):
            self.pin.mode = DROP

        for widget in self.get_widgets():
            widget.update()
