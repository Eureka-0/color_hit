from typing import Callable

import pygame.font as pf
from PIL import Image, ImageDraw

from utils import *


class _Content:
    def __init__(self, screen: Surface, rect: Rect, text: str, img_name: str):
        self.screen = screen
        self.rect = rect
        self.text = text
        self.img_name = img_name

    def load_image(self):
        if len(self.img_name):
            self.image = get_image(self.img_name, self.img_size)
            self.image_rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = None

    def render_text(self):
        if len(self.text):
            self.text_image = self.font.render(self.text, True, self.fontcolor)
            self.text_rect = self.text_image.get_rect(center=self.rect.center)
        else:
            self.text_image = None

    def set_style(self, font: str, fontsize: int, fontcolor: str, img_size: Vect2):
        self.font = pf.Font(pjoin("font", f"{font}.TTF"), fontsize)
        self.fontcolor = fontcolor
        self.img_size = img_size
        self.render_text()
        self.load_image()

    def update(self, text: Union[str, None], img_name: Union[str, None]):
        if type(text) is str:
            self.text = text
            self.render_text()
        if type(img_name) is str:
            self.img_name = img_name
            self.load_image()

        if self.image:
            self.screen.blit(self.image, self.image_rect)
        if self.text_image:
            self.screen.blit(self.text_image, self.text_rect)


class _BasePanel(Sprite):
    def __init__(
        self,
        screen: Surface,
        pos: Vect2,
        size: Vect2,
        text: str,
        img_name: str,
        **style,
    ):
        super().__init__()
        self.screen = screen
        self.size = size
        self.rect: Rect = Rect(pos[0], pos[1], size[0], size[1])
        self.content = _Content(screen, self.rect, text, img_name)
        self.set_style(**style)

    def set_style(self, **style):
        pass

    def set_back(self, radius: float, color: str):
        back_size = (int(self.size[0] * 100), int(self.size[1] * 100))
        back_image = Image.new("RGBA", back_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(back_image)
        xy = (100, 100, back_size[0] - 100, back_size[1] - 100)
        draw.rounded_rectangle(xy, radius * 100, color)
        self.back_image = pil2pg(back_image, self.size)

    def update(self, text: Union[str, None] = None, img_name: Union[str, None] = None):
        if self.back_image:
            self.screen.blit(self.back_image, self.rect)
        self.content.update(text, img_name)


class Label(_BasePanel):
    def __init__(
        self,
        screen: Surface,
        pos: Vect2,
        size: Vect2,
        text: str = "",
        img_name: str = "",
        **style,
    ):
        super().__init__(screen, pos, size, text, img_name, **style)

    def set_style(
        self,
        font: str = "MSYHMONO",
        fontsize: int = 16,
        fontcolor: str = B_WHITE,
        radius: float = 0,
        background: Union[str, None] = None,
        img_size: Union[Vect2, None] = None,
    ):
        img_size = self.size if img_size is None else img_size
        self.content.set_style(font, fontsize, fontcolor, img_size)
        if background:
            self.set_back(radius, background)
        else:
            self.back_image = None


class Button(_BasePanel):
    def __init__(
        self,
        screen: Surface,
        pos: Vect2,
        size: Vect2,
        text: str = "",
        img_name: str = "",
        callback: Callable = lambda: 1,
        **style,
    ):
        super().__init__(screen, pos, size, text, img_name, **style)
        self.callback = callback

    def set_style(
        self,
        radius: Union[float, None] = None,
        background: Union[str, None] = B_GREEN,
        hover_back: Union[str, None] = B_HOVER_GREEN,
        font: str = "FZKATJW",
        fontsize: int = 36,
        fontcolor: str = B_WHITE,
        img_size: Union[Vect2, None] = None,
    ):
        img_size = self.size if img_size is None else img_size
        self.content.set_style(font, fontsize, fontcolor, img_size)
        radius = min(self.size[:]) * 0.3 if radius is None else radius
        if background:
            self.set_back(radius, background)
        else:
            self.back_image = None

        if hover_back:
            self.set_hover_back(radius, hover_back)
        else:
            self.hover_back = None

    def set_hover_back(self, radius: float, hover_color: str):
        back_size = (int(self.size[0] * 100), int(self.size[1] * 100))
        back_image = Image.new("RGBA", back_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(back_image)
        xy = (100, 100, back_size[0] - 100, back_size[1] - 100)
        draw.rounded_rectangle(xy, radius * 100, hover_color)
        self.hover_back = pil2pg(back_image, self.size)

    def check_mouse_pos(self, mouse_pos) -> bool:
        return True if self.rect.collidepoint(mouse_pos) else False

    def check_click(self, event: Event):
        if self.check_mouse_pos(event.pos):
            self.callback()

    def update(self, text: Union[str, None] = None, img_name: Union[str, None] = None):
        background = self.back_image
        if self.hover_back:
            mouse_pos = pg.mouse.get_pos()
            if self.check_mouse_pos(mouse_pos):
                background = self.hover_back

        if background:
            self.screen.blit(background, self.rect)
        self.content.update(text, img_name)


class Pin(Sprite):
    def __init__(self, screen: Surface, color: str):
        super().__init__()
        self.screen = screen
        self.color = color
        self.set_image()
        self.rect: Rect = self.image.get_rect(
            centerx=WINDOW_SIZE[0] // 2, bottom=WINDOW_SIZE[1] - 20
        )
        self.mode = STILL
        self.angle: float = 0

    def set_image(self):
        image = Image.open(pjoin("img", "pin.png"))
        draw = ImageDraw.Draw(image)
        imgsize = image.size
        size = (450, 1800)
        w = MARGINAL_WIDTH * imgsize[0] / PIN_SIZE[0]
        xy = (
            w + 125,
            imgsize[1] - 100 - size[0] + w,
            imgsize[0] - 125 - w,
            imgsize[1] - 100 - w,
        )
        draw.ellipse(xy, fill=self.color)
        self.origin_image = pil2pg(image, PIN_SIZE)
        self.image: Surface = self.origin_image.copy()

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


class Pie(Sprite):
    def __init__(
        self, screen: Surface, color: str, start_degree: float, degree_range: float
    ):
        super().__init__()
        self.screen = screen
        self.color = color
        self.set_image(start_degree, degree_range)
        self.rect: Rect = self.image.get_rect(center=CENTER)
        self.angle: float = 0

    def set_image(self, start_degree: float, degree_range: float):
        size = (2200, 2200)
        image = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        xy = ((100.0, 100.0), (size[0] - 100, size[1] - 100))
        end = start_degree + degree_range
        draw.pieslice(xy, start_degree, end, fill=self.color, outline=self.color)
        self.origin_image = pil2pg(image, (2 * RADIUS, 2 * RADIUS))
        self.image: Surface = self.origin_image.copy()

    def update(self):
        self.angle = plus_angle(self.angle)
        self.image, self.rect = rotate(
            self.origin_image, self.angle, CENTER, Vector2(RADIUS, RADIUS)
        )

        self.screen.blit(self.image, self.rect)


class Balk(Sprite):
    def __init__(self):
        pass


class Bonus(Sprite):
    def __init__(self):
        pass


class Disc(Group):
    def __init__(self, screen: Surface, colors: list):
        self.screen = screen
        self.sector_num = len(set(colors))
        self.colors = list(set(colors))
        super().__init__(*self.generate_pies())

    def generate_pies(self) -> list[Pie]:
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
    def __init__(self, screen: Surface, color: str, pos: tuple[float, float]):
        super().__init__()
        self.screen = screen
        self.color = color
        self.rect: Rect = Rect(pos[0], pos[1], BULLET_SIZE[0], BULLET_SIZE[1])

    def update(self):
        pg.draw.rect(self.screen, self.color, self.rect)


class Bullets(Group):
    def __init__(self, screen: Surface, colors: list[str]):
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
