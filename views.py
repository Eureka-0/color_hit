import json
import os

from pygame.sprite import collide_mask

from widgets import *


def group_bullets(screen: Surface, colors: list[str]) -> OrderedGruop:
    bullets = OrderedGruop(screen)
    for i, color in enumerate(colors):
        pos = (BULLETS_POS[0], BULLETS_POS[1] - 3 * i * BULLET_SIZE[1])
        bullets.add(Bullet(screen, color, pos))
    return bullets


def group_heart_label(screen: Surface) -> OrderedGruop:
    hearts = OrderedGruop(screen)
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
        self.best_score = self.read_best_score()
        self.best_score_board = Label(
            screen, BEST_SCORE_POS, BEST_SCORE_SIZE, f"BESTSCORE  {self.best_score}"
        )
        self.best_score_board.set_style(
            font="TabletGothicBold.OTF", fs=16, fc=TEXT_BLUE
        )
        self.score = 0
        self.score_board = Label(screen, SCORE_POS, SCORE_SIZE, f"{self.score}")
        self.score_board.set_style(font="TabletGothicBold.OTF", fs=20)

        self.pause = False
        self.pause_button = Button(screen, PAUSE_POS, PAUSE_SIZE, img_name="pause.png")
        self.pause_button.set_style(r=PAUSE_SIZE[0] / 2)
        self.pause_button.set_callback(self.switch_pause)

        self.level = 1
        self.init_level()

    def read_best_score(self) -> int:
        best_score = pjoin("res", "best_score.json")
        if not os.path.exists(best_score):
            with open(best_score, "w", encoding="utf-8") as f:
                json.dump({"best_score": 0}, f, indent=4)
            return 0
        with open(best_score, "r", encoding="utf-8") as f:
            return json.load(f)["best_score"]

    def rewrite_best_score(self):
        with open(pjoin("res", "best_score.json"), "w", encoding="utf-8") as f:
            json.dump({"best_score": self.score}, f, indent=4)

    def switch_pause(self):
        if self.pause:
            self.pause = False
            self.pause_button.update(img_name="pause.png")
        else:
            self.pause = True
            self.pause_button.update(img_name="go_on.png")

    def init_level(self):
        self.colors = get_ordered_colors(self.level)
        self.pin = Pin(self.screen, self.colors[-1])
        self.disc = Disc(self.screen, self.colors)
        self.bullets = group_bullets(self.screen, self.colors)
        self.colors.pop()

    def on_keydown(self, event: Event):
        if not self.pause and event.key == pg.K_SPACE and self.pin.mode == STILL:
            self.pin.mode = SHOOT
            self.bullets.pop_widget()

    def on_mousedown(self, event: Event):
        if event.button == pg.BUTTON_LEFT:
            click = self.pause_button.check_click(event)
            if not click and not self.pause and self.pin.mode == STILL:
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
        if self.pause:
            self.pause_button.update()
            return False
        else:
            if self.pin.rect.top >= WINDOW_SIZE[1]:
                self.next_pin()

            if len(self.hearts):
                if self.pin.mode == SHOOT:
                    correct = hit_correct_color(self.pin, self.disc)
                    if correct:
                        self.pin.mode = PRICK
                        self.disc.add(self.pin)
                        self.score += randint(10, 15)
                        self.next_pin()
                    elif correct is False:
                        self.pin.mode = DROP
                        self.hearts.pop_widget()

                self.pin.update(past_sec)
                self.disc.update(past_sec)
                self.score_board.update(f"{self.score}")
                self.hearts.update()
                self.bullets.update()
                self.pause_button.update()
                return False
            else:
                if self.score > self.best_score:
                    self.rewrite_best_score()
                return True

    def draw(self):
        for widget in self.get_widgets():
            widget.draw()  # type: ignore
