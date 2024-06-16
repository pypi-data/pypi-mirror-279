import pygame
import math
from enum import Enum
from .Functions import round_half_up

class PS(Enum):
    cross = 0
    circle = 1
    square = 2
    triangle = 3
    share = 4
    ps = 5
    options = 6
    l1 = 9
    l3 = 7
    r1 = 10
    r3 = 8
    arrow_up = 11
    arrow_down = 12
    arrow_left = 13
    arrow_right = 14
    touch_pad = 15

class PlayStationController:
    def __init__(self, joystick_num, threshold: float = 0.05):
        """
        Makes handling of controller input easier.
        """
        self.joystick_num = joystick_num
        assert threshold >= 0, f"threshold must be at least 0 (currently {threshold})"
        assert threshold < 1, f"threshold must be less than 1 (currently {threshold})"
        self.threshold = threshold
        pygame.init()
        self.js = pygame.joystick.Joystick(joystick_num)
        self.js.init()
        self.pressed = {}

        self.update()

    def update(self):
        keys = self.get_pressed()
        self.cross = True if keys.get(PS.cross.value) else False
        self.circle = True if keys.get(PS.circle.value) else False
        self.square = True if keys.get(PS.square.value) else False
        self.triangle = True if keys.get(PS.triangle.value) else False
        self.share = True if keys.get(PS.share.value) else False
        self.ps = True if keys.get(PS.ps.value) else False
        self.options = True if keys.get(PS.options.value) else False
        self.l1 = True if keys.get(PS.l1.value) else False
        self.l3 = True if keys.get(PS.l3.value) else False
        self.r1 = True if keys.get(PS.r1.value) else False
        self.r3 = True if keys.get(PS.r3.value) else False
        self.arrow_up = True if keys.get(PS.arrow_up.value) else False
        self.arrow_down = True if keys.get(PS.arrow_down.value) else False
        self.arrow_left = True if keys.get(PS.arrow_left.value) else False
        self.arrow_right = True if keys.get(PS.arrow_right.value) else False
        self.touch_pad = True if keys.get(PS.touch_pad.value) else False

    def get_pressed(self):
        """
        Returns a dict of all keys pressed on the controller.
        Usage:
            keys = self.get_pressed()
            if keys[<key_num>]:
                action()
        """
        self.pressed = {}
        for button_num in range(self.js.get_numbuttons()):
            self.pressed[button_num] = self.js.get_button(button_num)
        return self.pressed

    def get_left_stick(self, custom_threshold=None) -> tuple[float, float]:
        """ returns a tuple representing the position of the left joystick """
        # pygame.event.pump()
        if custom_threshold == None:
            threshold = self.threshold
        elif type(custom_threshold) in [int, float]:
            assert custom_threshold >= 0
            threshold = custom_threshold
        else:
            raise TypeError(
                f"<custom_threshold> must be either None or an Integer or a float (not '{custom_threshold}')")

        vect = pygame.Vector2((self.js.get_axis(0), self.js.get_axis(1)))
        if vect.length() < threshold:
            return (0, 0)
        else:
            return vect

    def get_left_stick_angle(self, always_positive=True, decimals=1, default_return_value=0,
                             custom_threshold=None) -> int:
        """ returns the current angle of the left joystick; 0 == down """
        assert type(always_positive) == bool
        assert type(decimals) == int

        js = self.get_right_stick(custom_threshold)
        if js == (0, 0):
            return default_return_value
        deg = round_half_up(math.degrees(math.atan2(js[0], js[1])), decimals)

        if always_positive:
            return abs(deg)
        return deg

    def get_right_stick(self, custom_threshold=None) -> tuple[float, float]:
        """ returns a tuple representing the position of the right joystick """
        if custom_threshold == None:
            threshold = self.threshold
        elif type(custom_threshold) in [int, float]:
            assert custom_threshold >= 0
            threshold = custom_threshold
        else:
            raise TypeError(
                f"<custom_threshold> must be either None or an Integer or a float (not '{custom_threshold}')")

        vect = pygame.Vector2((self.js.get_axis(2), self.js.get_axis(3)))
        if vect.length() < threshold:
            return (0, 0)
        else:
            return vect

    def get_right_stick_angle(
            self, always_positive=True, decimals=1, default_return_value=0, custom_threshold=None) -> int:
        """ returns the current angle of the right joystick; 0 == down """
        assert type(always_positive) == bool
        assert type(decimals) == int

        js = self.get_right_stick(custom_threshold)
        if js == (0, 0):
            return default_return_value
        deg = round_half_up(math.degrees(math.atan2(js[0], js[1])), decimals)

        if always_positive:
            return abs(deg)
        return deg

    def get_l2(self, decimals=1) -> float:
        """ returns a float (-1 <= x <= 1) representing how much the paddle is pressed """
        return round_half_up(self.js.get_axis(4), decimals)

    def get_r2(self, decimals=1) -> float:
        """ returns a float (-1 <= x <= 1) representing how much the paddle is pressed """
        return round_half_up(self.js.get_axis(5), decimals)
