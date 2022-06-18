import json
import os
import sys
from functools import reduce
from math import cos, radians, sin
from random import randint, random, sample, shuffle

import pygame as pg
from config import Color, Grid

from src.typing_lib import *


def is_or_in(k: str, key: Union[str, tuple[str, str]]) -> bool:
    if type(key) is str:
        if k == key:
            return True
    elif k in key:
        return True
    return False


def draw_border(screen: Surface, rect: Rect, color: str, width: int, radius: int):
    if width > 0:
        pg.draw.rect(screen, color, rect, width=width, border_radius=radius)


def get_image(img_name: str, img_size: Union[None, Vect2] = None) -> Surface:
    image = pg.image.load(os.path.join("img", img_name)).convert_alpha()
    return pg.transform.smoothscale(image, img_size) if img_size else image


def get_path(*args):
    return os.path.join(getattr(sys, "_MEIPASS", ""), *args)


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
        colors = list(Color.pin_colors)
        shuffle(colors)
        return colors[0:num]
    else:
        return [Color.black]


def rand_num(n: int, fixed_sum: int, upper: bool = True) -> list[int]:
    sam = [0] + sample(range(1, fixed_sum), n - 1) + [fixed_sum]
    sam.sort()
    num = [sam[i + 1] - sam[i] for i in range(n)]
    if upper:
        up = round(fixed_sum / n) + 2
        while max(num) > up:
            sam = [0] + sample(range(1, fixed_sum), n - 1) + [fixed_sum]
            sam.sort()
            num = [sam[i + 1] - sam[i] for i in range(n)]
    return num


def ordered_colors(level: int, setting) -> list[str]:
    x = random()
    if 0 <= x < (level + 11) / (16 * level):
        num_of_pies = 1
    elif (level + 11) / (16 * level) <= x < (5 * level + 11) / (16 * level):
        num_of_pies = 2
    elif (5 * level + 11) / (16 * level) <= x < (11 * level + 5) / (16 * level):
        num_of_pies = 3
    else:
        num_of_pies = 4
    colors = rand_colors(num_of_pies)
    num_of_bullets = rand_num(num_of_pies, setting.pin_num - randint(0, 4))
    return expand_colors(colors, num_of_bullets)


def min_diff(l: list) -> float:
    l.sort()
    diff = l[-1]
    for i in range(len(l) - 1):
        if l[i + 1] - l[i] < diff:
            diff = l[i + 1] - l[i]
    return diff


def read_best_score() -> int:
    data_path = get_path("data")
    best_score_path = get_path("data", "best_score.json")
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    if not os.path.exists(best_score_path):
        with open(best_score_path, "w", encoding="utf-8") as f:
            json.dump({"best_score": 0}, f, indent=4)
        return 0
    with open(best_score_path, "r", encoding="utf-8") as f:
        return json.load(f)["best_score"]


def rewrite_best_score(score, best_score):
    if score > best_score:
        with open(get_path("data", "best_score.json"), "w", encoding="utf-8") as f:
            json.dump({"best_score": score}, f, indent=4)


def get_back() -> tuple[Surface, Rect]:
    s = max(Grid.window_size[0], Grid.window_size[1])
    background = get_image("background.png", (s, s))
    theta = random() * 360
    scale = random() + abs(cos(radians(theta))) + abs(sin(radians(theta)))
    back = pg.transform.rotozoom(background, theta, scale)
    back_rect = back.get_rect(center=Grid.window_size / 2)
    return back, back_rect


def quit_game():
    pg.quit()
    sys.exit()
