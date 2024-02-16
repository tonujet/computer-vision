import math
import uuid
from abc import ABC, abstractmethod
import tkinter as tk
from typing import List
import numpy as np


class Shape(ABC):

    @abstractmethod
    def draw(self):
        ...

    @abstractmethod
    def clear(self):
        ...

    @abstractmethod
    def move(self):
        ...



class TkinterShape(Shape):
    canvas: tk.Canvas
    points: List[float]
    matrix: np.array
    color: str = "black"
    tags: str

    def __calc_matrix(self, p: List[float]):
        matrix = np.ones((4, 3))
        for i in range(int(len(self.points) / 2)):
            x = p[i * 2]
            y = p[1 + i * 2]
            matrix[i][0] = x
            matrix[i][1] = y

        return matrix

    def __calc_points(self, m):
        points = []
        for i in range(int(len(self.points) / 2)):
            x = m[i][0]
            y = m[i][1]
            points.append(x)
            points.append(y)

        return points

    def __init__(self, canvas: tk.Canvas, points: List[float]):
        self.canvas = canvas
        if len(points) % 2 != 0:
            raise Exception("Not equal amount of x and y")
        self.points = points
        self.matrix = self.__calc_matrix(points)
        self.tags = str(uuid.uuid4())

    def draw(self, *args, **kwargs):
        self.canvas.create_polygon(self.points, tags=self.tags, fill=self.color, *args, **kwargs)

    def clear(self):
        self.canvas.delete(self.tags)

    def move(self, x: float = 0, y: float = 0):
        move_matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [x, y, 1],
        ])
        return self.update_position(move_matrix)

    def rotate(self, angle: float, center_x: float, center_y: float):
        move_to_center_matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [-center_x, -center_y, 1],
        ])

        rotate_matrix = np.array([
            [math.cos(math.radians(angle)), -math.sin(math.radians(angle)), 0],
            [math.sin(math.radians(angle)), math.cos(math.radians(angle)), 0],
            [0, 0, 1],
        ])

        move_from_center_matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [center_x, center_y, 1],
        ])
        matrix = np.dot(np.dot(move_to_center_matrix, rotate_matrix), move_from_center_matrix)

        return self.update_position(matrix)

    def update_position(self, matrix) -> bool:
        w = self.canvas.winfo_reqwidth()
        h = self.canvas.winfo_reqheight()
        m = np.dot(self.matrix, matrix)
        for i in range(int(len(self.points) / 2)):
            if m[i][0] < 0 or m[i][0] > w:
                return False
            if m[i][1] < 0 or m[i][1] > h:
                return False

        self.matrix = m
        self.points = self.__calc_points(m)
        return True

    def scale(self, x_koef: float = 1, y_koef: float = 1, center_x: float = 1, center_y: float = 1):
        move_to_center_matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [-center_x, -center_y, 1],
        ])

        scale_matrix = np.array([
            [x_koef, 0, 0],
            [0, y_koef, 0],
            [0, 0, 1],
        ])

        move_from_center_matrix = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [center_x, center_y, 1],
        ])

        matrix = np.dot(np.dot(move_to_center_matrix, scale_matrix), move_from_center_matrix)

        return self.update_position(matrix)

    def get_center(self) -> (int, int):
        p_len = int(len(self.points) / 2)
        x_sum = 0
        y_sum = 0
        for i in range(p_len):
            x_sum += self.points[i * 2]
            y_sum += self.points[1 + i * 2]

        return x_sum / p_len, y_sum / p_len


class Rectangle(TkinterShape):
    def __init__(self, canvas: tk.Canvas, x: float, y: float, width: float, height: float, ):
        points = [x, y, x + width, y, x + width, y + height, x, y + height]
        super().__init__(canvas, points)
        self.__is_rectangle()

    @classmethod
    def square(cls, canvas: tk.Canvas, x: float, y: float, width: float):
        return cls(canvas, x, y, width, width)

    def __is_rectangle(self):
        p = self.points
        if len(p) != 8:
            raise Exception("Not rectangle")
        x1 = p[0]
        x2 = p[2]
        x3 = p[4]
        x4 = p[6]
        y1 = p[1]
        y2 = p[3]
        y3 = p[5]
        y4 = p[7]

        cx = (x1 + x2 + x3 + x4) / 4
        cy = (y1 + y2 + y3 + y4) / 4

        dd1 = math.pow(cx - x1, 2) + math.pow(cy - y1, 2)
        dd2 = math.pow(cx - x2, 2) + math.pow(cy - y2, 2)
        dd3 = math.pow(cx - x3, 2) + math.pow(cy - y3, 2)
        dd4 = math.pow(cx - x4, 2) + math.pow(cy - y4, 2)
        return dd1 == dd2 and dd1 == dd3 and dd1 == dd4
