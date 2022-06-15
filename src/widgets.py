import os
from random import randint

import config as c
import pygame as pg
import pygame.font as pf
from config import Grid
from PIL import Image, ImageDraw

from src.typing_lib import *
from src.utils import draw_border, get_image, is_or_in, pil2pg, plus_angle, rotate


class _Content:
    def __init__(self, screen: Surface, rect: Rect, text: str, img_name: str):
        self.screen = screen
        self.rect = rect
        self.text = text
        self.img_name = img_name

    def load_image(self):
        if len(self.img_name):
            self.image = get_image(self.img_name, self.img_size)
            img_align = {self.img_align: getattr(self.rect, self.img_align)}
            if self.img_align in ("left", "right"):
                img_align["centery"] = self.rect.centery
            elif self.img_align in ("top", "bottom"):
                img_align["centerx"] = self.rect.centerx
            self.image_rect = self.image.get_rect(**img_align)
        else:
            self.image = None

    def render_text(self):
        if len(self.text):
            self.text_image = self.font.render(self.text, True, self.fontcolor)
            text_align = {self.text_align: getattr(self.rect, self.text_align)}
            if self.text_align in ("left", "right"):
                text_align["centery"] = self.rect.centery
            elif self.text_align in ("top", "bottom"):
                text_align["centerx"] = self.rect.centerx
            self.text_rect = self.text_image.get_rect(**text_align)
        else:
            self.text_image = None

    def set_style(
        self,
        font: str,
        fontsize: int,
        fontcolor: str,
        text_align: str,
        img_size: Vect2,
        img_align: str,
    ):
        self.font = pf.Font(os.path.join("font", font), fontsize)
        self.fontcolor = fontcolor
        self.text_align = text_align
        self.img_size = img_size
        self.img_align = img_align
        self.render_text()
        self.load_image()

    def update(self, text: Union[str, None], img_name: Union[str, None]):
        if type(text) is str:
            self.text = text
            self.render_text()
        if type(img_name) is str:
            self.img_name = img_name
            self.load_image()

    def draw(self):
        if self.image:
            self.screen.blit(self.image, self.image_rect)
        if self.text_image:
            self.screen.blit(self.text_image, self.text_rect)


class _Style(dict):
    content_style_key = ["font", "fs", "fc", "ta", "ms", "ma"]

    def __init__(self, default: dict):
        super().__init__(default.items())

    def __getitem__(self, key: str):
        for k in self:
            if is_or_in(key, k):
                return super().__getitem__(k)
        else:
            raise KeyError(f"Key '{key}' does not exist in {self}!")

    def __setitem__(self, key: str, value):
        for k in self:
            if is_or_in(key, k):
                return super().__setitem__(k, value)
        return super().__setitem__(key, value)

    def replace_default(self, key: str, default, new):
        if self.__getitem__(key) == default:
            self.__setitem__(key, new)

    def update_values(self, **kwargs):
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def get_values(self, keys: Sequence) -> list:
        values = []
        for k in keys:
            values.append(self.__getitem__(k))
        return values

    def get_content_styles(self) -> list:
        return self.get_values(_Style.content_style_key)


class Button(Sprite):
    default_style = {
        ("radius", "r"): None,
        ("background", "bg"): c.BUTTON_GREEN,
        ("hover_back", "hb"): c.BUTTON_HOVER_GREEN,
        ("border_width", "bw"): 0,
        ("border_color", "bc"): c.PIE_RED,
        ("border_radius", "br"): 0,
        "font": "FZKATJW.TTF",
        ("fontsize", "fs"): 36,
        ("fontcolor", "fc"): c.TEXT_WHITE,
        ("text_align", "ta"): "center",
        ("img_size", "ms"): None,
        ("img_align", "ma"): "center",
    }

    def __init__(
        self,
        screen: Surface,
        pos: Vect2,
        size: Vect2,
        text: str = "",
        img_name: str = "",
        callback: Callable = lambda: 1,
        **kwargs,
    ):
        super().__init__()
        self.screen = screen
        self.size = size
        self.rect: Rect = Rect(pos[0], pos[1], size[0], size[1])
        self.content = _Content(screen, self.rect, text, img_name)
        self.style = _Style(Button.default_style)
        self.set_style(**kwargs)
        self.hover = False
        self.callback = callback

    def set_style(self, **kwargs):
        self.style.update_values(**kwargs)
        self.style.replace_default("img_size", None, self.size)
        self.style.replace_default("radius", None, min(self.size[:]) * 0.3)
        self.content.set_style(*self.style.get_content_styles())
        radius = self.style["radius"]
        background = self.style["background"]
        if background:
            self.set_back(radius, background)
        else:
            self.back_image = None

        hover_back = self.style["hover_back"]
        if hover_back:
            self.set_hover_back(radius, hover_back)
        else:
            self.hover_back = None

    def set_callback(self, callback: Callable):
        self.callback = callback

    def set_back(self, radius: float, color: str):
        back_size = (int(self.size[0] * 10), int(self.size[1] * 10))
        back_image = Image.new("RGBA", back_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(back_image)
        xy = (10, 10, back_size[0] - 10, back_size[1] - 10)
        draw.rounded_rectangle(xy, radius * 10, color)
        self.back_image = pil2pg(back_image, self.size)

    def set_hover_back(self, radius: float, hover_color: str):
        back_size = (int(self.size[0] * 10), int(self.size[1] * 10))
        back_image = Image.new("RGBA", back_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(back_image)
        xy = (10, 10, back_size[0] - 10, back_size[1] - 10)
        draw.rounded_rectangle(xy, radius * 10, hover_color)
        self.hover_back = pil2pg(back_image, self.size)

    def check_mouse_pos(self, mouse_pos) -> bool:
        return True if self.rect.collidepoint(mouse_pos) else False

    def check_click(self, event: Event, *args, **kwargs) -> bool:
        if self.check_mouse_pos(event.pos):
            self.callback(*args, **kwargs)
            return True
        else:
            return False

    def update(self, text: Union[str, None] = None, img_name: Union[str, None] = None):
        self.content.update(text, img_name)
        mouse_pos = pg.mouse.get_pos()
        if self.check_mouse_pos(mouse_pos):
            self.hover = True
        else:
            self.hover = False

    def draw(self):
        if self.hover_back and self.hover:
            self.screen.blit(self.hover_back, self.rect)
        elif self.back_image:
            self.screen.blit(self.back_image, self.rect)
        self.content.draw()
        style = self.style
        draw_border(self.screen, self.rect, style["bc"], style["bw"], style["br"])


class Label(Sprite):
    default_style = {
        ("radius", "r"): 0,
        ("background", "bg"): None,
        ("border_width", "bw"): 0,
        ("border_color", "bc"): c.PIE_RED,
        ("border_radius", "br"): 0,
        "font": "FZPSZHUNHJW.TTF",
        ("fontsize", "fs"): 16,
        ("fontcolor", "fc"): c.TEXT_WHITE,
        ("text_align", "ta"): "center",
        ("img_size", "ms"): None,
        ("img_align", "ma"): "center",
    }

    def __init__(
        self,
        screen: Surface,
        pos: Vect2,
        size: Vect2,
        text: str = "",
        img_name: str = "",
        **kwargs,
    ):
        super().__init__()
        self.screen = screen
        self.size = size
        self.rect: Rect = Rect(pos[0], pos[1], size[0], size[1])
        self.content = _Content(screen, self.rect, text, img_name)
        self.style = _Style(Label.default_style)
        self.set_style(**kwargs)

    def set_style(self, **kwargs):
        self.style.update_values(**kwargs)
        self.style.replace_default("img_size", None, self.size)
        self.content.set_style(*self.style.get_content_styles())
        background = self.style["background"]
        if background:
            self.set_back(self.style["radius"], background)
        else:
            self.back_image = None

    def set_back(self, radius: float, color: str):
        back_size = (int(self.size[0] * 10), int(self.size[1] * 10))
        back_image = Image.new("RGBA", back_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(back_image)
        xy = (10, 10, back_size[0] - 10, back_size[1] - 10)
        draw.rounded_rectangle(xy, radius * 10, color)
        self.back_image = pil2pg(back_image, self.size)

    def update(self, text: Union[str, None] = None, img_name: Union[str, None] = None):
        self.content.update(text, img_name)

    def draw(self):
        if self.back_image:
            self.screen.blit(self.back_image, self.rect)
        self.content.draw()
        style = self.style
        draw_border(self.screen, self.rect, style["bc"], style["bw"], style["br"])


class Pin(Sprite):
    def __init__(self, screen: Surface, color: str):
        super().__init__()
        self.screen = screen
        self.color = color
        self.set_image()
        self.rect: Rect = self.image.get_rect(
            centerx=Grid.WINDOW_SIZE[0] // 2, bottom=Grid.WINDOW_SIZE[1] - 20
        )
        self.mode = c.STILL
        self.angle: float = 0
        self.relative_pos = Vector2(
            Grid.PIN_SIZE[0] / 2, Grid.PRICK_DEPTH - Grid.RADIUS
        )

    def set_image(self):
        image = Image.open(os.path.join("img", "pin.png"))
        draw = ImageDraw.Draw(image)
        imgsize = image.size
        size = (450, 1800)
        w = Grid.MARGINAL_WIDTH * imgsize[0] / Grid.PIN_SIZE[0]
        xy = (
            w + 125,
            imgsize[1] - 100 - size[0] + w,
            imgsize[0] - 125 - w,
            imgsize[1] - 100 - w,
        )
        draw.ellipse(xy, fill=self.color)
        self.origin_image = pil2pg(image, Grid.PIN_SIZE)
        self.image: Surface = self.origin_image.copy()

    def update(self, delta: float):
        if self.mode == c.SHOOT:
            self.rect.centery -= round(c.SHOOT_SPEED * delta)
        elif self.mode == c.DROP:
            self.rect.centery += round(c.DROP_SPEED * delta)
            self.rect.centerx += round(c.DROP_SPEED * delta) // 2

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Pie(Sprite):
    def __init__(
        self, screen: Surface, color: str, start_degree: float, degree_range: float
    ):
        super().__init__()
        self.screen = screen
        self.color = color
        self.set_image(start_degree, degree_range)
        self.angle: float = 0
        self.relative_pos = (Grid.RADIUS, Grid.RADIUS)

    def set_image(self, start_degree: float, degree_range: float):
        size = (2200, 2200)
        image = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)
        xy = ((100.0, 100.0), (size[0] - 100, size[1] - 100))
        end = start_degree + degree_range
        draw.pieslice(xy, start_degree, end, fill=self.color, outline=self.color)
        self.origin_image = pil2pg(image, (2 * Grid.RADIUS, 2 * Grid.RADIUS))
        self.image: Surface = self.origin_image.copy()
        self.rect: Rect = self.image.get_rect(center=Grid.CENTER)

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Balk(Sprite):
    def __init__(self, screen: Surface, disc: Group):
        super().__init__(disc)
        self.screen = screen


class Bonus(Sprite):
    def __init__(self, screen: Surface, disc: Group, angle: float, relative_pos: Vect2):
        super().__init__(disc)
        self.screen = screen
        self.angle = angle
        self.relative_pos = relative_pos

    def set_image(self, image: Surface):
        self.origin_image = image
        self.image: Surface = self.origin_image.copy()
        self.rect: Rect = self.image.get_rect(
            centerx=Grid.CENTER[0], top=Grid.CENTER[1] + self.relative_pos[1]
        )

    def set_bonusfunc(self, bonusfunc: Callable):
        self.bonusfunc = bonusfunc

    def on_hit(self, *args, **kwargs):
        self.kill()
        self.bonusfunc(*args, **kwargs)

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Heart(Bonus):
    def __init__(self, screen: Surface, disc: Group, angle: float):
        relative_pos = (Grid.HEART_BONUS_SIZE[0] // 2, -Grid.HEART_BONUS_RADIUS)
        super().__init__(screen, disc, angle, relative_pos)
        image = get_image("heart.png", Grid.HEART_BONUS_SIZE)
        super().set_image(pg.transform.rotozoom(image, 180, 1))


def _get_pies(screen: Surface, colors: set) -> list[Pie]:
    sector_degree = 360 / len(colors)
    pies = []
    for i, color in enumerate(colors):
        start_degree = i * sector_degree
        pies.append(Pie(screen, color, start_degree, sector_degree))
    return pies


class Disc(Group):
    def __init__(self, screen: Surface, colors: list):
        super().__init__(*_get_pies(screen, set(colors)))
        if randint(0, 1):
            self.heart = Heart(screen, self, randint(0, 360))

    def sorted_sprites(self) -> list[Union[Pin, Pie, Bonus]]:
        sorted_sprites = []
        for spr in self.sprites():
            if type(spr) is Pie:
                sorted_sprites.append(spr)
            else:
                sorted_sprites.insert(0, spr)
        return sorted_sprites

    def __iter__(self) -> Iterator[Union[Pin, Pie, Bonus]]:
        return iter(self.sorted_sprites())

    def update(self, past_sec: float):
        theta = c.ROTATION_SPEED * past_sec
        for sprite in self:
            sprite.angle = plus_angle(sprite.angle, theta)
            sprite.image, sprite.rect = rotate(
                sprite.origin_image, sprite.angle, Grid.CENTER, sprite.relative_pos
            )
            if hasattr(sprite, "update"):
                sprite.update(theta)

    def draw(self):
        for sprite in self:
            sprite.draw()


class Bullet(Sprite):
    def __init__(self, screen: Surface, color: str, pos: tuple[float, float]):
        super().__init__()
        self.screen = screen
        self.color = color
        self.rect: Rect = Rect(pos[0], pos[1], Grid.BULLET_SIZE[0], Grid.BULLET_SIZE[1])

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)


class OrderedGruop(Group):
    def __init__(self, screen: Surface, *sprites):
        self.screen = screen
        self.widget_list = []
        super().__init__(*sprites)

    def add(self, *sprites):
        super().add(*sprites)
        self.widget_list.extend(sprites)

    def __iter__(self) -> Iterator[Union[Bullet, Label]]:
        return iter(self.widget_list)

    def pop_widget(self):
        self.remove(self.widget_list.pop())

    def draw(self):
        for sprite in self:
            sprite.draw()


__all__ = [
    "Button",
    "Label",
    "Pin",
    "Pie",
    "Balk",
    "Bonus",
    "Heart",
    "Disc",
    "Bullet",
    "OrderedGruop",
]
