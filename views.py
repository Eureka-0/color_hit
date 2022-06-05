from functools import reduce
from random import randint, sample, shuffle
from typing import Union

import pygame as pg
from pygame.event import Event
from pygame.sprite import Group, Sprite

from config import *
from widgets import Bullets, Disc, Pie, Pin


def collide_mask(sprite1, sprite2):
    return True if pg.sprite.collide_mask(sprite1, sprite2) else False


def hit_correct_color(pin: Pin, disc: Disc) -> Union[None, bool]:
    collision = pg.sprite.spritecollideany(pin, disc, collide_mask)
    if isinstance(collision, Pie):
        if pin.color == collision.color:
            return True
        else:
            return False
    elif isinstance(collision, Pin):
        return False


def expand_colors(colors: list[str], num: list[int]) -> list[str]:
    expand = reduce(list.__add__, [[color] * n for color, n in zip(colors, num)])
    shuffle(expand)
    return expand


def rand_colors(num: int) -> list[str]:
    if 1 <= num <= 4:
        shuffle(COLORS)
        return COLORS[0:num]
    else:
        return ["#000000"]


def rand_num(n: int) -> list[int]:
    sam = [0] + sample(range(1, PIN_NUM), n - 1) + [PIN_NUM]
    sam.sort()
    num = [sam[i + 1] - sam[i] for i in range(n)]
    upper = round(PIN_NUM / n) + 2
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
        self.level = 1
        self.init_level()

    def init_level(self):
        self.colors = get_ordered_colors(self.level)
        self.pin = Pin(self.screen, self.colors[-1])
        self.disc = Disc(self.screen, self.colors)
        self.bullets = Bullets(self.screen, self.colors)
        self.colors.pop()

    def on_keydown(self, event: Event):
        if event.key == pg.K_SPACE and self.pin.mode == STILL:
            self.pin.mode = SHOOT
            self.bullets.number -= 1

    def on_mousedown(self, event: Event):
        if event.button == pg.BUTTON_LEFT and self.pin.mode == STILL:
            self.pin.mode = SHOOT
            self.bullets.number -= 1

    def next_pin(self):
        if len(self.colors) > 0:
            self.pin = Pin(self.screen, self.colors.pop())
        else:
            self.level += 1
            self.init_level()

    def get_widgets(self) -> list[Union[Sprite, Group]]:
        widgets = []
        for v in self.__dict__.values():
            if isinstance(v, (Sprite, Group)):
                widgets.append(v)
        return widgets

    def update(self):
        if self.pin.rect.top >= WINDOW_SIZE[1]:
            self.next_pin()

        if self.pin.mode == SHOOT:
            correct = hit_correct_color(self.pin, self.disc)
            if correct:
                self.pin.mode = PRICK
                self.disc.add(self.pin)
                self.next_pin()
            elif correct is False:
                self.pin.mode = DROP

        for widget in self.get_widgets():
            widget.update()
