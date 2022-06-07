from typing import Sequence, Union

from PIL.Image import Image as PILImage
from pygame import KEYDOWN, MOUSEBUTTONDOWN, QUIT
from pygame.event import Event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

Vect2 = Union[Vector2, tuple[float, float]]


FPS = 100  # 游戏帧率


# 组件尺寸，单位为像素
WINDOW_SIZE = Vector2(700, 700)  # 主窗口大小
PIN_SIZE = Vector2(35, 100)  # 飞镖大小
MARGINAL_WIDTH = 3  # 飞镖圆形头部边缘宽度
PRICK_DEPTH = 50  # 飞镖扎入深度
BULLETS_POS = Vector2(50, 500)  # 剩余飞镖的显示位置
BULLET_SIZE = Vector2(20, 4)  # 剩余飞镖显示大小
CENTER = Vector2(350, 260)  # color disc 圆心位置
RADIUS = 120  # color disc 半径


# 圆盘与飞镖颜色
RED = "#F32424"
GREEN = "#6BCB77"
ORANGE = "#FF7700"
BLUE = "#3DB2FF"
COLORS = (RED, GREEN, ORANGE, BLUE)


# Button 背景及文字颜色
B_GREEN = "#00b63e"
B_HOVER_GREEN = "#058b30"
B_WHITE = "#ffffff"


# 飞镖的四种状态，静止、射击、扎入、掉落
STILL = 1
SHOOT = 2
PRICK = 3
DROP = 4


# 组件移动速度，平移像素/帧，旋转度/帧
ROTATION_SPEED = 100 // FPS  # 圆盘部分旋转速度
SHOOT_SPEED = 2500 // FPS  # 飞镖飞行速度
DROP_SPEED = 500 // FPS  # 飞镖掉落速度


PIN_NUM = 8  # 两关之后的飞镖总数，8 ~ 12
