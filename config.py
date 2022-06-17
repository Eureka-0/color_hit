from random import randint

from pygame.math import Vector2


FPS = 100  # 游戏最高帧率

# 飞镖的四种状态，静止、射击、扎入、掉落
STILL = 1
SHOOT = 2
PRICK = 3
DROP = 4


class Grid:
    """
    组件尺寸与布局相关设置，单位均为像素.
    """

    window_size = Vector2(600, 700)  # 主窗口大小

    start_size = Vector2(140, 60)  # 菜单页面开始按钮大小
    start_pos = Vector2((window_size[0] - start_size[0]) / 2, 350)  # 菜单页面开始按钮位置

    pin_size = Vector2(35, 100)  # 飞镖大小
    marginal_width = 3  # 飞镖圆形头部边缘宽度
    prick_depth = 45  # 飞镖扎入深度

    center = Vector2(window_size[0] / 2, 260)  # color disc 圆心位置
    radius = 120  # color disc 半径

    balk_size = Vector2(78, 78)  # 障碍物大小
    balk_radius = radius - 20  # 障碍物旋转半径

    heart_bonus_size = Vector2(40, 40)  # 心形道具显示大小
    heart_bonus_radius = radius  # 心形道具旋转半径

    bullets_pos = Vector2(50, 500)  # 剩余飞镖的显示位置
    bullet_size = Vector2(20, 4)  # 剩余飞镖图标大小

    hearts_pos = Vector2(window_size[0] - 50, 100)  # 生命值显示位置
    heart_size = Vector2(25, 25)  # 生命值图标大小

    best_score_size = Vector2(200, 24)  # 最高得分显示大小
    best_score_pos = Vector2((window_size[0] - best_score_size[0]) / 2, 8)  # 最高得分显示位置
    score_size = Vector2(100, 30)  # 当前得分显示大小
    score_pos = Vector2((window_size[0] - score_size[0]) / 2, 30)  # 当前得分显示位置

    pause_pos = Vector2(window_size[0] - 55, 10)  # 暂停按钮显示位置
    pause_size = Vector2(35, 35)  # 暂停按钮大小


class Color:
    # 圆盘与飞镖颜色
    red = "#F32424"
    green = "#6BCB77"
    orange = "#FF7700"
    blue = "#3DB2FF"
    pin_colors = (red, green, orange, blue)

    # Button、Label 的背景及文字颜色
    lime_green = "#00b63e"
    dark_green = "#009233"
    white = "#ffffff"
    aqua = "#00FFAB"
    lime_blue = "#34B3F1"

    black = "#000000"
    light_red = "#ff0000"


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
