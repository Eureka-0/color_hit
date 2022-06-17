from random import randint

from pygame.math import Vector2

FPS = 100  # 游戏最高帧率


class Grid:
    """
    组件尺寸与布局相关设置，单位均为像素.
    """

    WINDOW_SIZE = Vector2(600, 700)  # 主窗口大小

    START_SIZE = Vector2(140, 60)  # 菜单页面开始按钮大小
    START_POS = Vector2((WINDOW_SIZE[0] - START_SIZE[0]) / 2, 350)  # 菜单页面开始按钮位置

    PIN_SIZE = Vector2(35, 100)  # 飞镖大小
    MARGINAL_WIDTH = 3  # 飞镖圆形头部边缘宽度
    PRICK_DEPTH = 45  # 飞镖扎入深度

    CENTER = Vector2(WINDOW_SIZE[0] / 2, 260)  # color disc 圆心位置
    RADIUS = 120  # color disc 半径

    BALK_SIZE = Vector2(78, 78)  # 障碍物大小
    BALK_RADIUS = RADIUS - 20  # 障碍物旋转半径

    HEART_BONUS_SIZE = Vector2(40, 40)  # 心形道具显示大小
    HEART_BONUS_RADIUS = RADIUS  # 心形道具旋转半径

    BULLETS_POS = Vector2(50, 500)  # 剩余飞镖的显示位置
    BULLET_SIZE = Vector2(20, 4)  # 剩余飞镖图标大小

    HEARTS_POS = Vector2(WINDOW_SIZE[0] - 50, 100)  # 生命值显示位置
    HEART_SIZE = Vector2(25, 25)  # 生命值图标大小

    BEST_SCORE_SIZE = Vector2(200, 24)  # 最高得分显示大小
    BEST_SCORE_POS = Vector2((WINDOW_SIZE[0] - BEST_SCORE_SIZE[0]) / 2, 8)  # 最高得分显示位置
    SCORE_SIZE = Vector2(100, 30)  # 当前得分显示大小
    SCORE_POS = Vector2((WINDOW_SIZE[0] - SCORE_SIZE[0]) / 2, 30)  # 当前得分显示位置

    PAUSE_POS = Vector2(WINDOW_SIZE[0] - 55, 10)  # 暂停按钮显示位置
    PAUSE_SIZE = Vector2(35, 35)  # 暂停按钮大小


# 圆盘与飞镖颜色
PIE_RED = "#F32424"
PIE_GREEN = "#6BCB77"
PIE_ORANGE = "#FF7700"
PIE_BLUE = "#3DB2FF"
COLORS = (PIE_RED, PIE_GREEN, PIE_ORANGE, PIE_BLUE)


# Button、Label 的背景及文字颜色
BUTTON_GREEN = "#00b63e"
BUTTON_HOVER_GREEN = "#058b30"
TEXT_WHITE = "#ffffff"
TEXT_LIGHTGREEN = "#00FFAB"
TEXT_BLUE = "#34B3F1"


# 飞镖的四种状态，静止、射击、扎入、掉落
STILL = 1
SHOOT = 2
PRICK = 3
DROP = 4


class Setting:
    """
    游戏玩法相关设置.
    """

    shoot_speed = 2500  # 飞镖飞行速度，像素/s
    drop_speed = 500  # 飞镖掉落速度，像素/s
    pin_num = 10  # 飞镖总数上限，8 ~ 12
    init_hp = 2  # 初始生命值
    highest_hp = 3  # 最高生命值

    def __init__(self):
        """
        存储一些可随着 level 数的改变而改变的设置.
        """
        self.rotation_speed = 80  # 圆盘部分旋转速度，度/s

    def change_speed(self):
        self.rotation_speed = randint(80, 150)
