from typing import Callable

from PIL import Image, ImageDraw, PyAccess
from matplotlib import pyplot


def map_from_to(x: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


Center = (int, int) or int
RGB = tuple[int, int, int]
PixelCallback = Callable[['CbParams'], RGB]


class CbParams:
    r: int
    g: int
    b: int
    x: int
    y: int
    w: int
    h: int
    center_w: Center
    center_h: Center

    def __less_then_center(self, num: int, center: Center):
        if isinstance(center, tuple):
            return num < center[0]
        return num < center

    def less_then_center_w(self) -> bool:
        return self.__less_then_center(self.x, self.center_w)

    def less_then_center_h(self) -> bool:
        return self.__less_then_center(self.y, self.center_h)

    def __greater_then_center(self, num: int, center: Center) -> bool:
        if isinstance(center, tuple):
            return num > center[1]
        return num > center

    def greater_then_center_w(self) -> bool:
        return self.__greater_then_center(self.x, self.center_w)

    def greater_then_center_h(self) -> bool:
        return self.__greater_then_center(self.y, self.center_h)

    def x_center_ration(self) -> float:
        if self.less_then_center_w():
            if isinstance(self.center_w, tuple):
                return self.x / self.center_w[0]
            else:
                return self.x / self.center_w
        elif self.greater_then_center_w():
            diff = (self.w - self.x - 1)
            if isinstance(self.center_w, tuple):
                return diff / self.center_w[1]
            else:
                return diff / self.center_w
        else:
            return 1

    def y_center_ration(self) -> float:
        if self.less_then_center_h():
            if isinstance(self.center_h, tuple):
                return self.y / self.center_h[0]
            else:
                return self.y / self.center_h
        elif self.greater_then_center_h():
            diff = (self.h - self.y - 1)
            if isinstance(self.center_h, tuple):
                return diff / self.center_h[1]
            else:
                return diff / self.center_h
        else:
            return 1

    def center_ratio(self) -> (float, float):
        return self.x_center_ration(), self.y_center_ration()

    def center_ratio_map_to(self, _from: float, to: float) -> (float, float):
        return map_from_to(self.x_center_ration(), 0, 1, _from, to), \
            map_from_to(self.y_center_ration(), 0, 1, _from, to)

    def x_start_ration(self) -> float:
        return self.x / self.w

    def y_start_ration(self) -> float:
        return self.y / self.w

    def start_ration(self) -> (float, float):
        return self.x_start_ration(), self.y_start_ration()

    def start_ration_map_to(self, _from: float, to: float) -> (float, float):
        return map_from_to(self.x_start_ration(), 0, 1, _from, to), \
            map_from_to(self.y_start_ration(), 0, 1, _from, to)

    def __init__(self, canvas, r: int, g: int, b: int, x: int, y: int):
        self.r = r
        self.b = b
        self.g = g
        self.x = x
        self.y = y
        self.w = canvas.width
        self.h = canvas.height
        self.center_w = canvas.get_center_width()
        self.center_h = canvas.get_center_height()

    def __str__(self) -> str:
        return f"w:{self.w}; h:{self.h}; center_w: {self.center_w}; center_h: {self.center_h}; x: {self.x}; y: {self.y}; x_ratio: {self.x_center_ration()}; y_ration: {self.y_center_ration()};"


class Canvas:
    file_name: str
    show: bool
    image: Image
    draw: ImageDraw
    pixels: PyAccess
    width: int
    height: int

    def get_center_width(self):
        return self.__get_center(self.width)

    def get_center_height(self):
        return self.__get_center(self.height)

    def __init__(self, file_name: str, show: bool):
        self.file_name = file_name
        self.show = show

    @staticmethod
    def edit_pixels_by_cb(file_name: str, pixel_cb: PixelCallback, show=True) -> None:
        canvas = Canvas(file_name, show)
        canvas.draw_pixels_and_close(pixel_cb)

    def __enter__(self) -> 'Canvas':
        self.image = Image.open(self.file_name)
        self.draw = ImageDraw.Draw(self.image)
        self.pixels = self.image.load()
        width, height = self.image.size
        self.width = width
        self.height = height
        print(f"|-Image: {self.file_name} \n|---width: {width} \n|---height: {height}")
        if self.show: self.__show_image();
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback) -> None:
        self.image.close()

    def __show_image(self) -> None:
        pyplot.imshow(self.image)
        pyplot.show()

    def __get_center(self, num) -> Center:
        if num % 2 == 0:
            center = (num // 2 - 1, num // 2)
        else:
            center = num // 2

        return center

    def draw_pixels_and_close(self, pixel_callback: PixelCallback) -> None:
        with self as canvas:
            for x in range(canvas.width):
                for y in range(canvas.height):
                    r, g, b = canvas.pixels[x, y]
                    params = CbParams(canvas, r, g, b, x, y)
                    res = pixel_callback(params)
                    canvas.draw.point((x, y), self.__normalize(res))
            canvas.__show_image()

    def __normalize(self, res: RGB) -> RGB:
        def bound(val):
            if val < 0:
                val = 0
            elif val > 255:
                val = 255
            return val

        return tuple(map(bound, res))


def gray_shade(file_name: str, _from: float = 0.1, to: float = 1.8):
    def pixel_cb(params: CbParams) -> RGB:
        x_ratio, y_ratio = params.center_ratio_map_to(_from, to)
        try:
            mean = int((params.r + params.g + params.b) // 3 * x_ratio * y_ratio)
        except ZeroDivisionError:
            mean = 255
        return mean, mean, mean

    Canvas.edit_pixels_by_cb(file_name, pixel_cb)


def serpia_shade(file_name: str, depth: int = 20, _from: float = 0.4, to: float = 1.6):
    def pixel_cb(params: CbParams) -> RGB:
        x_ratio, y_ratio = params.center_ratio_map_to(_from, to)
        try:
            mean = int((params.r + params.g + params.b) // (3 * x_ratio * y_ratio))
        except ZeroDivisionError:
            mean = 255

        r = mean + depth * 4
        g = mean + depth
        b = mean
        return r, g, b

    Canvas.edit_pixels_by_cb(file_name, pixel_cb)


def negative(file_name: str, _from: float = 0.3, to: float = 3):
    def pixel_cb(params: CbParams) -> RGB:
        x_ratio, y_ratio = params.start_ration_map_to(_from, to)
        color = lambda i: int(255 - i * x_ratio * y_ratio)
        return color(params.r), color(params.g), color(params.b)

    Canvas.edit_pixels_by_cb(file_name, pixel_cb)


def brightness(file_name: str, factor: int = 70, _from: float = -3, to: float = 3):
    def pixel_cb(params: CbParams) -> RGB:
        x_ratio = params.x_start_ration()
        x_ratio = map_from_to(x_ratio, 0, 1, _from, to)
        color = lambda i: int(i + factor * x_ratio)
        return color(params.r), color(params.g), color(params.b)

    Canvas.edit_pixels_by_cb(file_name, pixel_cb)


gray_shade("example1.jpg")
serpia_shade("example2.jpg")
negative("example3.jpg")
brightness("example4.jpg")
