from widgets import *


def group_bullets(screen: Surface, colors: list[str]) -> OrderedGruop:
    bullets = OrderedGruop()
    for i, color in enumerate(colors):
        pos = (BULLETS_POS[0], BULLETS_POS[1] - 3 * i * BULLET_SIZE[1])
        bullets.add(Bullet(screen, color, pos))
    return bullets


def group_heart_label(screen: Surface) -> OrderedGruop:
    hearts = OrderedGruop()
    for i in range(3):
        pos = (HEARTS_POS[0], HEARTS_POS[1] + i * HEART_SIZE[0])
        hearts.add(Label(screen, pos, HEART_SIZE, img_name="heart.png"))
    return hearts


def hit_correct_color(pin: Pin, disc: Disc) -> Union[None, bool]:
    collision = None
    for spr in disc:
        if collide_mask(pin, spr):
            collision = spr
            break
    if type(collision) is Pie:
        if pin.color == collision.color:
            return True
        else:
            return False
    elif isinstance(collision, (Pin, Balk)):
        return False


class GameView:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.hearts = group_heart_label(screen)
        self.level = 1
        self.init_level()

    def init_level(self):
        self.colors = get_ordered_colors(self.level)
        self.pin = Pin(self.screen, self.colors[-1])
        self.disc = Disc(self.screen, self.colors)
        self.bullets = group_bullets(self.screen, self.colors)
        self.colors.pop()

    def on_keydown(self, event: Event):
        if event.key == pg.K_SPACE and self.pin.mode == STILL:
            self.pin.mode = SHOOT
            self.bullets.pop_widget()

    def on_mousedown(self, event: Event):
        if event.button == pg.BUTTON_LEFT and self.pin.mode == STILL:
            self.pin.mode = SHOOT
            self.bullets.pop_widget()

    def next_pin(self):
        if len(self.colors) > 0:
            self.pin = Pin(self.screen, self.colors.pop())
        else:
            self.level += 1
            self.init_level()

    def get_widgets(self) -> Iterator[Union[Sprite, Group]]:
        for v in self.__dict__.values():
            if isinstance(v, (Sprite, Group)):
                yield v

    def update(self, past_sec: float) -> bool:
        if self.pin.rect.top >= WINDOW_SIZE[1]:
            self.next_pin()

        if len(self.hearts):
            if self.pin.mode == SHOOT:
                correct = hit_correct_color(self.pin, self.disc)
                if correct:
                    self.pin.mode = PRICK
                    self.disc.add(self.pin)
                    self.next_pin()
                elif correct is False:
                    self.pin.mode = DROP
                    self.hearts.pop_widget()

            for widget in self.get_widgets():
                try:
                    widget.update(past_sec)
                except TypeError:
                    widget.update()
            return False
        else:
            return True
