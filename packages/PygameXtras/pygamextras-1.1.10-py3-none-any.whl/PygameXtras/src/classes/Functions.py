import ctypes
import math
import os

import pygame


def higher_resolution(boolean: bool = True):
    """
    Most Windows PCs (automatically) use scaling to 150% which makes many applications appear
    blurry. To avoid this effect, this function can be called to increase the resolution on
    affected displays without having to manually change the scaling in the computers settings.
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(bool(boolean))


def scale_image(image, factor):
    """
    Changes the size of an image while keeping its proportions.
    """
    return pygame.transform.scale(
        image, (int(image.get_width() * factor), int(image.get_height() * factor))
    )


def rotate_in_place(rect, image, degrees):
    """
    ONLY WORKS WITH SPRITES

    Usage:
    self.rect, self.image = rotate_in_place(self.rect, self.image)
    """
    old_rect_center = rect.center
    new_image = pygame.transform.rotate(image, degrees)
    new_rect = new_image.get_rect()
    new_rect.center = old_rect_center
    return new_rect, new_image


def create_animation(image_ids: list, frames_per_image: list):
    """
    create a dict with image_ids and corresponding
    images before using this function.

    If usage unclear, refer to:
    marcel-python-programs\PYGAME_GAMES\pve\mini_warfare\data\player.py
    """
    assert len(image_ids) == len(
        frames_per_image
    ), "received lists of different lengths"
    seq = []
    for image_id, count in zip(image_ids, frames_per_image):
        for i in range(count):
            seq.append(image_id)
    return seq


def get_distance(xy1: tuple, xy2: tuple, digits_after_comma: int = None) -> float:
    """returns the distance between xy1 and xy2"""
    x1, y1 = xy1[0], xy1[1]
    x2, y2 = xy2[0], xy2[1]
    if digits_after_comma == None:
        return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    else:
        return round_half_up(
            math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2)), digits_after_comma
        )


def get_distance_squared(xy1: tuple, xy2: tuple):
    return (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2


def get_angle_between_points(xy1, xy2):
    vect = pygame.math.Vector2(xy2[0] - xy1[0], xy2[1] - xy1[1]).normalize()
    cos = round_half_up(vect.y, 2)
    deg_cos = int(math.degrees(math.acos(vect.x)))
    if cos <= 0:
        return deg_cos
    else:
        return 180 + (180 - deg_cos)


def get_normalized_vector_between_points(xy1, xy2):
    vect = pygame.math.Vector2(xy2[0] - xy1[0], xy2[1] - xy1[1])
    if vect.length() > 0:
        vect.normalize()
    return vect


def get_normalized_vector_from_angle(angle):
    vect = pygame.Vector2(
        round_half_up(math.cos(math.radians(angle)), 3),
        round_half_up(math.sin(math.radians(angle)), 3),
    )
    return vect.normalize()


def round_half_up(n, decimals=0):
    if isinstance(n, int):
        return n
    multiplier = 10**decimals
    if decimals == 0:
        return int(math.floor(n * multiplier + 0.5) / multiplier)
    else:
        return math.floor(n * multiplier + 0.5) / multiplier


def vect_sum(a: tuple, b: tuple):
    if len(a) != len(b):
        raise ValueError("Received vectors of different dimensions.")
    vect = []
    for num1, num2 in zip(a, b):
        vect.append(num1 + num2)
    return tuple(vect)


def vs(a: tuple, b: tuple):
    """vect_sum(...)"""
    return vect_sum(a, b)


def invert(a: tuple):
    """inverts a vector"""
    return (-a[0], -a[1])


def inv(a: tuple):
    """invert(...)"""
    return invert(a)


def load_image(
    path, size: tuple[int, int] = None, colorkey: tuple[int, int, int] = None
):
    """example for <path>: data/images/image1"""
    assert type(path) == str, f"invalid argument for 'path': {path}"
    if "/" in path:
        splitted = path.split("/")
        path = os.path.join(*splitted)

    try:
        img = pygame.image.load(path)
    except:
        raise Exception("image '" + str(path) + "' not found")

    if size != None:
        # assertions
        assert type(size) in [tuple, list], f"invalid argument for 'size': {size}"
        assert len(size) == 2, f"invalid argument for 'size': {size}"
        for item in size:
            assert type(item) == int, f"invalid argument for 'size': {size}"
            assert item > 0, f"invalid argument for 'size': {size}"

        img = pygame.transform.scale(img, size)

    if colorkey != None:
        # assertions
        assert type(colorkey) in [
            tuple,
            list,
        ], f"invalid argument for 'colorkey': {colorkey}"
        assert len(colorkey) == 3, f"invalid argument for 'colorkey': {colorkey}"
        for item in colorkey:
            assert type(item) == int, f"invalid argument for 'colorkey': {colorkey}"
            assert 0 <= item <= 255, f"invalid argument for 'colorkey': {colorkey}"

        img.set_colorkey(colorkey)

    return img


def draw_rect_alpha(
    surface,
    color,
    rect,
    width: int = 0,
    border_radius: int = -1,
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
    border_bottom_left_radius: int = -1,
    border_bottom_right_radius: int = -1,
):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(
        shape_surf,
        color,
        shape_surf.get_rect(),
        width,
        border_radius,
        border_top_left_radius,
        border_top_right_radius,
        border_bottom_left_radius,
        border_bottom_right_radius,
    )
    surface.blit(shape_surf, rect)


def draw_circle_alpha(
    surface,
    color,
    center,
    radius,
    width: int = 0,
    draw_top_right: bool = None,
    draw_top_left: bool = None,
    draw_bottom_left: bool = None,
    draw_bottom_right: bool = None,
):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(
        shape_surf,
        color,
        (radius, radius),
        radius,
        width,
        draw_top_right,
        draw_top_left,
        draw_bottom_left,
        draw_bottom_right,
    )
    surface.blit(shape_surf, target_rect)


def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
    surface.blit(shape_surf, target_rect)


def ask_filename():
    """temporary method to get filename"""
    import tkinter.filedialog

    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def ask_directory():
    """temporary method to get foldername"""
    import tkinter.filedialog

    top = tkinter.Tk()
    top.withdraw()  # hide window
    dir_name = tkinter.filedialog.askdirectory(parent=top)
    top.destroy()
    return dir_name


def get_fonts():
    return [
        f.removesuffix(".ttf")
        for f in os.listdir(os.path.join(os.path.dirname(__file__), "..", "fonts"))
    ]
