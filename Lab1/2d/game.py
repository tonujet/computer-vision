from tkinter import *
from graphics import *
import time

from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 90
    DOWN = 180
    LEFT = 270
    UP_RIGHT = 45
    UP_LEFT = 315
    DOWN_RIGHT = 135
    DOWN_LEFT = 225


class Hero(TkinterShape):
    SCALE_KOEF = 1.05
    direction = Direction.UP
    objects: List[TkinterShape]
    body: Rectangle
    head: Rectangle
    canvas: Canvas

    def __init__(self, canvas: Canvas, speed: int):
        self.speed = speed
        body_edge = 100
        offset = math.sqrt(2) * body_edge / 2

        body = Rectangle.square(canvas, 0, 0, body_edge)
        body.color = "black"
        cannon = Rectangle(canvas, 0.4 * body_edge, 0.1 * body_edge, 0.2 * body_edge, 0.4 * body_edge)
        cannon.color = "red"
        tower = Rectangle.square(canvas, 0.2 * body_edge, 0.2 * body_edge, 0.6 * body_edge)
        tower.color = "green"
        self.objects = [body, tower, cannon]
        self.canvas = canvas
        self.body = body
        self.head = cannon
        self.to_center(offset)

    def to_center(self, center_offset):
        w = self.canvas.winfo_reqwidth()
        h = self.canvas.winfo_reqheight()
        x_offset = w / 2 - center_offset
        y_offset = h / 2 - center_offset
        self.move(x_offset, y_offset)

    def rotate(self, angle: float, x: float, y: float):
        for obj in self.objects:
            is_rotated = obj.rotate(angle, x, y)
            if not is_rotated:
                return False
        return True

    def rotate_around_center(self, new_direction: Direction):
        angle = self.get_angle(new_direction)
        x, y = self.body.get_center()
        if self.rotate(angle, x, y):
            self.direction = new_direction

    def move(self, x: float = 0, y: float = 0):
        for obj in self.objects:
            is_moved = obj.move(x, y)
            if not is_moved:
                return False

        return True

    def up(self):
        self.move(0, -self.speed)
        self.rotate_around_center(Direction.UP)

    def up_right(self):
        self.move(0, -self.speed)
        self.move(self.speed, 0)
        self.rotate_around_center(Direction.UP_RIGHT)

    def up_left(self):
        self.move(0, -self.speed)
        self.move(-self.speed, 0)
        self.rotate_around_center(Direction.UP_LEFT)

    def down(self):
        self.move(0, self.speed)
        self.rotate_around_center(Direction.DOWN)

    def down_left(self):
        self.move(0, self.speed)
        self.move(-self.speed, 0)
        self.rotate_around_center(Direction.DOWN_LEFT)

    def down_right(self):
        self.move(0, self.speed)
        self.move(self.speed, 0)
        self.rotate_around_center(Direction.DOWN_RIGHT)

    def left(self):
        self.move(-self.speed, 0)
        self.rotate_around_center(Direction.LEFT)

    def right(self):
        self.move(self.speed, 0)
        self.rotate_around_center(Direction.RIGHT)

    def scale(self, x_koef: float = 1, y_koef: float = 1):
        x, y = self.body.get_center()
        for obj in self.objects:
            if not obj.scale(x_koef, y_koef, x, y):
                return False
        return True

    def scale_up(self):
        self.scale(self.SCALE_KOEF, self.SCALE_KOEF)

    def scale_down(self):
        self.scale(1 / self.SCALE_KOEF, 1 / self.SCALE_KOEF)

    def clear(self):
        for obj in self.objects:
            obj.clear()

    def draw(self, *args, **kwargs):
        for obj in self.objects:
            obj.draw(*args, **kwargs)

    def handle_pressed_keys(self, pressed_keys):
        if len(pressed_keys) == 1:
            match pressed_keys[0]:
                case 87:
                    self.up()
                case 83:
                    self.down()
                case 65:
                    self.left()
                case 68:
                    self.right()
                case 81:
                    self.scale_up()
                case 69:
                    self.scale_down()
        else:
            if 87 in pressed_keys and 68 in pressed_keys:
                self.up_right()
            elif 87 in pressed_keys and 65 in pressed_keys:
                self.up_left()
            elif 83 in pressed_keys and 68 in pressed_keys:
                self.down_right()
            elif 83 in pressed_keys and 65 in pressed_keys:
                self.down_left()

    def get_angle(self, new_direction: Direction):
        if new_direction.value == self.direction.value:
            return 0
        angle = self.direction.value - new_direction.value
        return angle


class Game:
    root: Tk
    canvas: Canvas
    objects: List[TkinterShape]
    pressed_keys = []
    hero: Hero

    def __init__(self):
        root = Tk()
        root.title("2d graphics")
        root.geometry("800x700")
        self.root = root

        self.key_binds()
        canvas = Canvas(root, bg="white", bd=0, border=0, width=800, height=600, background="skyblue")
        self.hero = Hero(canvas, 4)
        canvas.pack(expand=True)
        self.canvas = canvas
        self.objects = [self.hero]

    def key_binds(self):
        var = StringVar()
        Label(self.root, textvariable=var).pack()

        def keyup(e):
            if e.keycode in self.pressed_keys:
                self.pressed_keys.pop(self.pressed_keys.index(e.keycode))
                var.set(str(self.pressed_keys))

        def keydown(e):
            if not e.keycode in self.pressed_keys:
                self.pressed_keys.append(e.keycode)
                var.set(str(self.pressed_keys))

        self.root.bind("<KeyPress>", keydown)
        self.root.bind("<KeyRelease>", keyup)

    def start(self):
        while 1:
            time.sleep(0.01)
            self.update_objects()
            self.hero.handle_pressed_keys(self.pressed_keys)
            self.root.update()

    def update_objects(self):
        for obj in self.objects:
            obj.clear()
            obj.draw()
