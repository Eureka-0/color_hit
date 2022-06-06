from widgets import *


def hit_correct_color(pin: Pin, disc: Disc) -> Union[None, bool]:
    collision = pg.sprite.spritecollideany(pin, disc, collide_mask)
    if isinstance(collision, Pie):
        if pin.color == collision.color:
            return True
        else:
            return False
    elif isinstance(collision, (Pin, Balk)):
        return False


class GameView:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.level = 1
        self.init_level()

    def init_level(self):
        self.colors = get_ordered_colors(self.level)
        self.pin = Pin(self.screen, self.colors[-1])
        self.disc = Disc(self.screen, self.colors)
        self.bullets = Bullets(self.screen, self.colors)
        self.colors.pop()

    def on_keydown(self, event: Event):
        if event.key == pg.K_SPACE and self.pin.mode == STILL:
            self.pin.mode = SHOOT
            self.bullets.number -= 1

    def on_mousedown(self, event: Event):
        if event.button == pg.BUTTON_LEFT and self.pin.mode == STILL:
            self.pin.mode = SHOOT
            self.bullets.number -= 1

    def next_pin(self):
        if len(self.colors) > 0:
            self.pin = Pin(self.screen, self.colors.pop())
        else:
            self.level += 1
            self.init_level()

    def get_widgets(self) -> list[Union[Sprite, Group]]:
        widgets = []
        for v in self.__dict__.values():
            if isinstance(v, (Sprite, Group)):
                widgets.append(v)
        return widgets

    def update(self):
        if self.pin.rect.top >= WINDOW_SIZE[1]:
            self.next_pin()

        if self.pin.mode == SHOOT:
            correct = hit_correct_color(self.pin, self.disc)
            if correct:
                self.pin.mode = PRICK
                self.disc.add(self.pin)
                self.next_pin()
            elif correct is False:
                self.pin.mode = DROP

        for widget in self.get_widgets():
            widget.update()
