import math
import random
import tkinter as tk
import uuid
from abc import ABC, abstractmethod
from typing import List

import numpy as np

import interpolation


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
    color: str = "red"
    z_buffer: np.array

    def __init__(self, canvas: tk.Canvas, matrix):
        self.canvas = canvas
        self.matrix = matrix
        self.tags = str(uuid.uuid4())

    def set_color(self, width: int, color: str):
        self.outline_width = width
        self.color = color

    def set_random_color(self):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        self.color = "#{:02x}{:02x}{:02x}".format(red, green, blue)

    def set_random_outline_width(self):
        self.outline_width = random.randint(2, 10)

    def set_random_outline(self):
        self.set_random_color()
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

    @abstractmethod
    def to_points(self):
        ...

    def draw(self):
        points = self.to_points()
        self.canvas.create_polygon(points, tags=self.tags, fill="", width=self.outline_width,
                                   outline=self.color)

    def draw_using_lagrange_interpolation(self, point_num):
        for i in range(len(self.matrix) - 1):
            curr_point = self.matrix[i]
            next_point = self.matrix[i + 1]
            matrix = np.array([curr_point, next_point])
            points = interpolation.calc_points_with_lagrange_interpolation(matrix, point_num)
            for point in points:
                self._draw_point(point)

    @abstractmethod
    def draw_using_lagrange_interpolation_and_z_buffer(self, z_buffer, point_num):
        ...

    def _draw_point(self, point):
        x, y, *_ = point
        self.canvas.create_oval(x, y, x + 2, y + 2, fill=self.color, outline="")
        # self.canvas.create_line(x, y, x + 1, y, fill=self.color)

    def _draw_points_relative_to_z_buffer(self, points, random_color=False, color=None):
        if not color and random_color:
            self.set_random_color()
        elif color:
            self.color = color

        for point in points:
            self._draw_point_relative_to_z_buffer(point)

    def _fill_z_buffer(self, points):
        for point in points:
            x, y, z, *_ = point
            x, y, z = int(round(x)), int(round(y)), z
            if self.z_buffer[x, y] < z:
                self.z_buffer[x, y] = z

    def _draw_point_relative_to_z_buffer(self, point):
        x, y, z, *_ = point
        r_x, r_y = int(round(x)), int(round(y))
        if self.z_buffer[r_x, r_y] > z:
            return
        # self.canvas.create_oval(x, y, x + 2, y + 2, fill=self.color, outline="")
        self.canvas.create_line(x, y, x + 1, y, fill=self.color)

    def rotate(self, angle_x=0, angle_y=0, angle_z=0):
        self.rotate_x(angle_x)
        self.rotate_y(angle_y)
        self.rotate_z(angle_z)

    def get_shape_center(self):
        center_x = 0
        center_y = 0
        center_z = 0
        l = len(self.matrix)
        for raw in self.matrix:
            x, y, z, *_ = raw
            center_x += x
            center_y += y
            center_z += z

        center_x = center_x / l
        center_y = center_y / l
        center_z = center_z / l

        return center_x, center_y, center_z

    def transition_around_center(self, matrix):
        x, y, z = self.get_shape_center()
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

        transformation_matrix = self.transition_around_center(rotate_matrix)
        self.update_cords(transformation_matrix)

    def rotate_y(self, angle):
        rad = math.radians(angle)
        rotate_matrix = np.array([
            [math.cos(rad), 0, -math.sin(rad), 0],
            [0, 1, 0, 0],
            [math.sin(rad), 0, math.cos(rad), 0],
            [0, 0, 0, 1],
        ])
        transformation_matrix = self.transition_around_center(rotate_matrix)
        self.update_cords(transformation_matrix)

    def rotate_z(self, angle):
        rad = math.radians(angle)
        rotate_matrix = np.array([
            [math.cos(rad), -math.sin(rad), 0, 0],
            [math.sin(rad), math.cos(rad), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])
        transformation_matrix = self.transition_around_center(rotate_matrix)
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

    def draw_using_lagrange_interpolation_and_z_buffer(self, point_num, colors):
        self.z_buffer = np.ones((self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()))
        base = self.fill_base_with_points(point_num)
        triangles = [self.fill_triangle_with_points(point_num, _from=num) for num in [4, 7, 11, 14]]
        shapes = [base] + triangles
        for points in shapes:
            super()._fill_z_buffer(points)

        for points, color in zip(shapes, colors):
            self._draw_points_relative_to_z_buffer(points=points, color=color)

    def fill_base_with_points(self, point_num, _from=0):
        base_outline_points = []
        self.__use_seq_interpolation_to_points(
            _from=_from, to=_from + 5,
            next_point_shift=1,
            points=self.matrix,
            acc_points=base_outline_points,
            point_num=point_num
        )
        # for point in base_outline_points:
        #     print(point[2])

        base_points = []
        self.__use_seq_interpolation_to_points(
            _from=0, to=len(base_outline_points) - point_num,
            next_point_shift=-2 * point_num,
            points=base_outline_points,
            acc_points=base_points,
            point_num=point_num
        )
        return base_points

    def fill_triangle_with_points(self, point_num, _from):
        triangle_outline_points = []
        self.__use_seq_interpolation_to_points(
            _from=_from, to=_from + 3,
            next_point_shift=1,
            points=self.matrix,
            acc_points=triangle_outline_points,
            point_num=point_num
        )

        triangle_points = []
        self.__use_seq_interpolation_to_points(
            _from=0, to=int(1 / 3 * len(triangle_outline_points)),
            next_point_shift=-2 * point_num + 1,
            points=triangle_outline_points,
            acc_points=triangle_points,
            point_num=point_num
        )
        return triangle_points

    def __use_seq_interpolation_to_points(self, _from, to, next_point_shift, points, acc_points, point_num):
        for i in range(_from, to):
            curr_point = points[i]
            next_point = points[abs(i + next_point_shift)]
            self.__use_interpolation_between_two_points(curr_point, next_point, acc_points, point_num)

    def __use_interpolation_between_two_points(self, curr_point, next_point, acc_points, point_num):
        matrix = np.array([curr_point, next_point])
        points = interpolation.calc_points_with_lagrange_interpolation(matrix, point_num)
        for point in points:
            acc_points.append(point)
