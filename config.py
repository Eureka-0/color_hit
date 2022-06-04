FPS = 100  # 游戏帧率


# 主窗口大小，像素
WIDTH = 700
HEIGHT = 700

# 飞镖大小，像素
PIN_WIDTH = 20
PIN_HEIGHT = 80

MARGINAL_WIDTH = 3  # 飞镖圆形头部边缘宽度，像素
PRICK_DEPTH = 30  # 飞镖扎入深度，像素

BULLETS_POS = (50, 500)  # 剩余飞镖的显示位置，像素

# 剩余飞镖显示大小，像素
BULLET_WIDTH = 20
BULLET_HEIGHT = 4

CENTER = (350, 260)  # color disc 圆心位置，像素
RADIUS = 100  # color disc 半径，像素


# 颜色
RED = "#F32424"
GREEN = "#6BCB77"
ORANGE = "#FF7700"
PURPLE = "#541690"


# 飞镖的四种状态，静止、射击、扎入、掉落
STILL = 1
SHOOT = 2
PRICK = 3
DROP = 4


ROTATION_SPEED = 100 // FPS  # 圆盘部分旋转速度，度/帧
SHOOT_SPEED = 2500 // FPS  # 飞镖飞行速度，像素/帧
DROP_SPEED = 500 // FPS  # 飞镖掉落速度，像素/帧


PIN_NUM = 8  # 两关之后的飞镖总数，8 ~ 12
