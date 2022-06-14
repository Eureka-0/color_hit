from typing import Callable, Iterator, Sequence, Union

from PIL.Image import Image as PILImage
from pygame.event import Event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

Vect2 = Union[Vector2, tuple[float, float]]
