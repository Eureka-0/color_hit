import os

import pygame as pg
from PIL import Image, ImageDraw
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

from config import *


def draw_border(screen, rect: Rect):
    pg.draw.rect(screen, (255, 0, 0), rect, width=2)


def plus_angle(angle: float) -> float:
    angle += ROTATION_SPEED
    return angle - 360 if angle > 360 else angle


def pil2pg(pilimg: Image.Image) -> Surface:
    raw = pilimg.tobytes("raw", "RGBA")
    size = pilimg.size
    return pg.image.fromstring(raw, size, "RGBA").convert_alpha()  # type: ignore


def rotate(
    img: Surface, angle: float, pos: Vector2, relative_pos: Vector2
) -> tuple[Surface, Rect]:
    rect = img.get_rect(topleft=pos - relative_pos)
    offset = pos - Vector2(rect.center)
    rotated_offset = offset.rotate(angle)
    rotated_center = pos - rotated_offset
    rotated_img = pg.transform.rotate(img, -angle)
    rotated_rect = rotated_img.get_rect(center=rotated_center)
    return rotated_img, rotated_rect


class Pie(Sprite):
    def __init__(self, screen, color, start_degree, degree_range):
        super().__init__()
        self.screen = screen
        self.color = color
        self.origin_image = self.get_image(start_degree, degree_range)
        self.image: Surface = self.origin_image.copy()
        self.rect: Rect = self.image.get_rect(center=CENTER)
        self.angle = 0

    def get_image(self, start_degree, degree_range):
        size = (2000, 2000)
        image = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        xy = ((0.0, 0.0), size)
        end = start_degree + degree_range
        draw.pieslice(xy, start_degree, end, fill=self.color, outline=self.color)
        return pg.transform.smoothscale(pil2pg(image), (2 * RADIUS, 2 * RADIUS))

    def update(self):
        self.angle = plus_angle(self.angle)
        self.image, self.rect = rotate(
            self.origin_image, self.angle, CENTER, Vector2(RADIUS, RADIUS)
        )

        self.screen.blit(self.image, self.rect)


class Pin(Sprite):
    def __init__(self, screen, color):
        super().__init__()
        self.screen = screen
        self.color = color
        self.origin_image = self.get_image()
        self.image: Surface = self.origin_image.copy()
        self.rect: Rect = self.image.get_rect(
            centerx=WINDOW_SIZE[0] // 2, bottom=WINDOW_SIZE[1] - 20
        )
        self.mode = STILL
        self.angle = 0

    def get_image(self):
        image = Image.open(os.path.join("img", "pin.png"))
        draw = ImageDraw.Draw(image)
        size = image.size
        w = MARGINAL_WIDTH * size[0] / 20
        xy = (w, size[1] - size[0] + w, size[0] - w, size[1] - w)
        draw.ellipse(xy, fill=self.color)
        return pg.transform.smoothscale(pil2pg(image), PIN_SIZE)

    def update(self):
        if self.mode == SHOOT:
            self.rect.centery -= SHOOT_SPEED
        elif self.mode == PRICK:
            self.angle = plus_angle(self.angle)
            relative_pos = Vector2(PIN_SIZE[0] / 2, PRICK_DEPTH - RADIUS)
            self.image, self.rect = rotate(
                self.origin_image, self.angle, CENTER, relative_pos
            )
        elif self.mode == DROP:
            self.rect.centery += DROP_SPEED
            self.rect.centerx += DROP_SPEED // 2

        self.screen.blit(self.image, self.rect)


class Disc(Group):
    def __init__(self, screen, colors: list):
        self.screen = screen
        self.sector_num = len(set(colors))
        self.colors = list(set(colors))
        super().__init__(*self.generate_pies())

    def generate_pies(self):
        sector_degree = 360 / len(self.colors)
        pies = []
        for i in range(self.sector_num):
            color = self.colors[i]
            start_degree = i * sector_degree
            pies.append(Pie(self.screen, color, start_degree, sector_degree))
        return pies

    def update(self):
        sorted_sprites = []
        for spr in self.sprites():
            if isinstance(spr, Pie):
                sorted_sprites.append(spr)
            else:
                sorted_sprites.insert(0, spr)

        for spr in sorted_sprites:
            spr.update()


class _Bullet(Sprite):
    def __init__(self, screen, color, pos):
        super().__init__()
        self.screen = screen
        self.color = color
        self.rect: Rect = pg.Rect(pos[0], pos[1], BULLET_SIZE[0], BULLET_SIZE[1])

    def update(self):
        pg.draw.rect(self.screen, self.color, self.rect)


class Bullets(Group):
    def __init__(self, screen, colors):
        self.screen = screen
        self.colors = colors
        self.number = len(colors)
        bullets = []
        for i, color in enumerate(self.colors):
            pos = (BULLETS_POS[0], BULLETS_POS[1] - 3 * i * BULLET_SIZE[1])
            bullets.append(_Bullet(self.screen, color, pos))
        super().__init__(*bullets)

    def update(self):
        if self.number < len(self.sprites()) and len(self.sprites()):
            self.remove(self.sprites()[-1])
        for bullet in self.sprites():
            bullet.update()
