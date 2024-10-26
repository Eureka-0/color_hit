import json
import os
import sys
from itertools import chain
from math import cos, radians, sin
from random import randint, random, sample, shuffle

import pygame as pg

from config import Color, Grid
from typing_lib import *


def is_or_in(k: str, key: Union[str, tuple[str, str]]) -> bool:
    """
    检查 key 是否是指定的 key 或在指定的元组中.

    Args:
        k (str)
        key (Union[str, tuple[str, str]])

    Returns:
        bool
    """
    if type(key) is str:
        if k == key:
            return True
    elif k in key:
        return True
    return False


def draw_border(screen: Surface, rect: Rect, color: str, width: int, radius: int):
    """
    绘制一个边框.

    Args:
        screen (Surface): 要绘制在其上的 Surface.
        rect (Rect): 要绘制边框的矩形区域.
        color (str): 边框颜色.
        width (int): 边框宽度.
        radius (int): 边框圆角半径.
    """
    if width > 0:
        pg.draw.rect(screen, color, rect, width=width, border_radius=radius)


def get_image(img_name: str, img_size: Union[None, Vect2] = None) -> Surface:
    """
    获取图片.

    Args:
        img_name (str): 要获取的图片的文件名.
        img_size (Union[None, Vect2], optional): 输出图片的大小. 默认为 None，输出为原始大小.

    Returns:
        Surface: 读取到的图片.
    """
    image = pg.image.load(os.path.join("img", img_name)).convert_alpha()
    return pg.transform.smoothscale(image, img_size) if img_size else image


def get_path(*args) -> str:
    """
    根据当前是运行应用程序还是直接运行 python 代码获取文件路径.

    Returns:
        str: 文件路径.
    """
    return os.path.join(getattr(sys, "_MEIPASS", ""), *args)


def pil2pg(pilimg: PILImage, size: Vect2) -> Surface:
    """
    将 PILImage 转换为 Surface.

    Args:
        pilimg (PILImage): 要转换的 PILImage.
        size (Vect2): 输出 Surface 的大小.

    Returns:
        Surface: 转换后的 Surface.
    """
    raw = pilimg.tobytes("raw", "RGBA")
    imgsize = pilimg.size
    pgimg = pg.image.fromstring(raw, imgsize, "RGBA").convert_alpha()  # type: ignore
    return pg.transform.smoothscale(pgimg, size)


def vect2vector(vect: Vect2) -> Vector2:
    """
    将 Vect2 转换为 Vector2.
    Vect2 = Union[Vector2, tuple[float, float]] 是自定义的类型简写.

    Args:
        vect (Vect2): 要转换的 Vect2.

    Returns:
        Vector2: 转换后的 Vector2.
    """
    return vect if type(vect) is Vector2 else Vector2(vect)


def rotate(img: Surface, angle: float, pos: Vect2, relative_pos: Vect2):
    """
    旋转图片.

    Args:
        img (Surface): 要旋转的图片.
        angle (float): 旋转角度.
        pos (Vect2): 旋转中心的位置.
        relative_pos (Vect2): 旋转中心相对于图片左上角的位置.

    Returns:
        Surface: 旋转后的图片.
        Rect: 旋转后的图片的矩形区域.
    """
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
    """
    将不重复的颜色及其数量扩展为可重复的列表，每种颜色在列表中出现的次数为其对应的数量，打乱后返回.

    Args:
        colors (list[str]): 不重复的颜色列表.
        num (list[int]): 每种颜色对应的数量.

    Returns:
        list[str]: 扩展并打乱后的颜色列表.
    """
    expand = list(chain.from_iterable([color] * n for color, n in zip(colors, num)))
    shuffle(expand)
    return expand


def rand_colors(num: int) -> list[str]:
    """
    生成不重复的随机颜色列表.

    Args:
        num (int): 要生成颜色的数量，1 至 4 之间的整数.

    Returns:
        list[str]: 随机生成的颜色列表.
    """
    if 1 <= num <= 4:
        colors = list(Color.pin_colors)
        shuffle(colors)
        return colors[0:num]
    else:
        return [Color.black]


def rand_num(n: int, fixed_sum: int, upper: bool = True) -> list[int]:
    """
    生成具有固定总和且不超过上限的随机数列表.

    Args:
        n (int): 要生成的列表的长度.
        fixed_sum (int): 固定总和.
        upper (bool, optional): 是否要设置上限. 默认为 True.

    Returns:
        list[int]: 生成的随机数列表.
    """
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
    """
    根据 level 值生成有序的颜色列表.

    Args:
        level (int):
        setting (_type_): 设置类实例.

    Returns:
        list[str]: 生成的有序颜色列表.
    """
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
    """
    返回列表相邻两项之间的最小差值.

    Args:
        l (list)

    Returns:
        float: 最小差值.
    """
    l.sort()
    diff = l[-1]
    for i in range(len(l) - 1):
        if l[i + 1] - l[i] < diff:
            diff = l[i + 1] - l[i]
    return diff


def read_best_score() -> int:
    """
    读取最高得分.

    Returns:
        int: 读取的最高得分.
    """
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


def rewrite_best_score(score: int, best_score: int):
    """
    重写最高得分.

    Args:
        score (int): 当前得分，若高于最高得分则重写.
        best_score (int): 最高得分.
    """
    if score > best_score:
        with open(get_path("data", "best_score.json"), "w", encoding="utf-8") as f:
            json.dump({"best_score": score}, f, indent=4)


def get_back() -> tuple[Surface, Rect]:
    """
    获取背景图片，并随机地将其旋转一定角度，缩放以填满可视区域.

    Returns:
        Surface: 背景图片.
        Rect: 背景图片的矩形区域.
    """
    s = max(Grid.window_size[0], Grid.window_size[1])
    background = get_image("background.png", (s, s))
    theta = random() * 360
    scale = random() + abs(cos(radians(theta))) + abs(sin(radians(theta)))
    back = pg.transform.rotozoom(background, theta, scale)
    back_rect = back.get_rect(center=Grid.window_size / 2)
    return back, back_rect


def quit_game():
    """
    退出游戏.
    """
    pg.quit()
    sys.exit()
