import math
import random
import uuid
from abc import ABC, abstractmethod
import tkinter as tk
from typing import List

import numpy as np


class Shape(ABC):

    @abstractmethod
    def draw(self, *args, **kwargs):
        ...

    @abstractmethod
    def clear(self):
        ...

    def redraw(self):
        self.clear()
        self.draw()


class Tkinter3dShape(Shape):
    canvas: tk.Canvas
    matrix: np.array
    tags: str
    outline_width: int = 1
    outline_color: str = "red"

    def __init__(self, canvas: tk.Canvas, matrix):
        self.canvas = canvas
        self.matrix = matrix
        self.tags = str(uuid.uuid4())

    def set_ouline(self, width: int, color: str):
        self.outline_width = width
        self.outline_color = color

    def set_random_outline_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        self.outline_color = "#{:02x}{:02x}{:02x}".format(red, green, blue)

    def set_random_outline_width(self):
        self.outline_width = random.randint(2, 10)

    def set_random_outline(self):
        self.set_random_outline_color()
        self.set_random_outline_width()

    def to_matrix(self, points: List[float]):
        m_len = int(len(points) / 3)
        matrix = np.ones((m_len, 4))

        for i in range(m_len):
            x = points[i * 3]
            y = points[1 + i * 3]
            z = points[2 + i * 3]
            matrix[i][0] = x
            matrix[i][1] = y
            matrix[i][2] = z

        return matrix

    def to_points(self):
        pass

    def draw(self):
        points = self.to_points()
        self.canvas.create_polygon(points, tags=self.tags, fill="", width=self.outline_width,
                                   outline=self.outline_color)

    def rotate(self, angle_x=0, angle_y=0, angle_z=0):
        self.rotate_x(angle_x)
        self.rotate_y(angle_y)
        self.rotate_z(angle_z)

    def transtion_to_center(self, matrix):
        x = self.canvas.winfo_reqwidth() / 2
        y = self.canvas.winfo_reqheight() / 2
        z = 333
        move_to_center = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1],
        ])

        move_from_center = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1],
        ])

        return np.dot(np.dot(move_to_center, matrix), move_from_center)

    def rotate_x(self, angle):
        rad = math.radians(angle)
        rotate_matrix = np.array([
            [1, 0, 0, 0],
            [0, math.cos(rad), math.sin(rad), 0],
            [0, -math.sin(rad), math.cos(rad), 0],
            [0, 0, 0, 1],
        ])

        transformation_matrix = self.transtion_to_center(rotate_matrix)
        self.update_cords(transformation_matrix)

    def rotate_y(self, angle):
        rad = math.radians(angle)
        rotate_matrix = np.array([
            [math.cos(rad), 0, -math.sin(rad), 0],
            [0, 1, 0, 0],
            [math.sin(rad), 0, math.cos(rad), 0],
            [0, 0, 0, 1],
        ])
        transformation_matrix = self.transtion_to_center(rotate_matrix)
        self.update_cords(transformation_matrix)

    def rotate_z(self, angle):
        rad = math.radians(angle)
        rotate_matrix = np.array([
            [math.cos(rad), -math.sin(rad), 0, 0],
            [math.sin(rad), math.cos(rad), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
        transformation_matrix = self.transtion_to_center(rotate_matrix)
        self.update_cords(transformation_matrix)

    def clear(self):
        self.canvas.delete(self.tags)

    def move(self, x: float = 0, y: float = 0, z: float = 0):
        move_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [x, y, z, 1],
        ])

        self.update_cords(move_matrix)

    def scale(self, koef_x: float, koef_y: float, koef_z: float):
        scale_matrix = np.array([
            [koef_x, 0, 0, 0],
            [0, koef_y, 0, 0],
            [0, 0, koef_z, 0],
            [0, 0, 0, 1],
        ])

        self.update_cords(scale_matrix)

    def random_scale(self):
        koef_x = random.uniform(0.7, 1.4)
        koef_y = random.uniform(0.7, 1.4)
        koef_z = random.uniform(0.7, 1.4)
        self.scale(koef_x, koef_y, koef_z)

    def update_cords(self, transformation_matrix):
        w = self.canvas.winfo_reqwidth()
        h = self.canvas.winfo_reqheight()
        matrix = np.dot(self.matrix, transformation_matrix)
        for raw in matrix:
            if raw[0] < 0 or raw[0] > w or raw[1] < 0 or raw[1] > h:
                return

        self.matrix = matrix

    def get_center(self) -> (int, int):
        x_sum = 0
        y_sum = 0
        z_sum = 0
        m_len = len(self.matrix)
        for raw in self.matrix:
            x_sum += raw[0]
            y_sum += raw[1]
            z_sum += raw[2]

        return x_sum / m_len, y_sum / m_len, z_sum / m_len


class Pyramid(Tkinter3dShape):

    def __init__(self, canvas: tk.Canvas, points):
        super().__init__(canvas, points)
        self.set_random_outline()

    def to_points(self):
        points = []
        for raw in self.matrix:
            for i in range(len(raw) - 2):
                points.append(raw[i])

        return points
