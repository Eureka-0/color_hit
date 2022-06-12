import json
import os
from functools import reduce
from os.path import join as pjoin
from random import randint, sample, shuffle

import pygame as pg

from config import *


def is_or_in(k: str, key: tuple[str, tuple[str, str]]) -> bool:
    if type(key) is str:
        if k == key:
            return True
    elif k in key:
        return True
    return False


def draw_border(screen: Surface, rect: Rect, color: str, width: int, radius: int):
    if width > 0:
        pg.draw.rect(screen, color, rect, width=width, border_radius=radius)


def plus_angle(angle: float, theta: float) -> float:
    return (angle + theta) % 360


def get_image(img_name: str, img_size: Union[None, Vect2] = None) -> Surface:
    image = pg.image.load(pjoin("img", img_name)).convert_alpha()
    return pg.transform.smoothscale(image, img_size) if img_size else image


def pil2pg(pilimg: PILImage, size: Vect2) -> Surface:
    raw = pilimg.tobytes("raw", "RGBA")
    imgsize = pilimg.size
    pgimg = pg.image.fromstring(raw, imgsize, "RGBA").convert_alpha()  # type: ignore
    return pg.transform.smoothscale(pgimg, size)


def vect2vector(vect: Vect2) -> Vector2:
    return vect if type(vect) is Vector2 else Vector2(vect)


def rotate(img: Surface, angle: float, pos: Vect2, relative_pos: Vect2):
    pos = vect2vector(pos)
    relative_pos = vect2vector(relative_pos)
    rect = img.get_rect(topleft=pos - relative_pos)
    offset = pos - Vector2(rect.center)
    rotated_offset = offset.rotate(angle)
    rotated_center = pos - rotated_offset
    rotated_img = pg.transform.rotozoom(img, -angle, 1)
    rotated_rect = rotated_img.get_rect(center=rotated_center)
    return rotated_img, rotated_rect


def expand_colors(colors: list[str], num: list[int]) -> list[str]:
    expand = reduce(list.__add__, [[color] * n for color, n in zip(colors, num)])
    shuffle(expand)
    return expand


def rand_colors(num: int) -> list[str]:
    if 1 <= num <= 4:
        colors = list(COLORS)
        shuffle(colors)
        return colors[0:num]
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


def read_best_score() -> int:
    best_score = pjoin("res", "best_score.json")
    if not os.path.exists(best_score):
        with open(best_score, "w", encoding="utf-8") as f:
            json.dump({"best_score": 0}, f, indent=4)
        return 0
    with open(best_score, "r", encoding="utf-8") as f:
        return json.load(f)["best_score"]


def rewrite_best_score(score, best_score):
    if score > best_score:
        with open(pjoin("res", "best_score.json"), "w", encoding="utf-8") as f:
            json.dump({"best_score": score}, f, indent=4)
