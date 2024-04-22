import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import material
import utils


# Для формування модельного Dataset з метою навчання нейромережі для розпізнавання
# заданих об’єктів за технологіями Computer Vision створити динамічну модель руху легкових
# автомобілів.


@dataclass
class Drawable(ABC):
    x: float
    y: float
    z: float

    w: float
    h: float
    l: float

    hitbox_color: Union[None, tuple[int, int, int]]

    @abstractmethod
    def display(self):
        raise NotImplementedError()

    def display_hit_box(self):
        if self.hitbox_color is None:
            return

        vertices = utils.get_box_vertices(self.x, self.y, self.z, self.h, self.w, self.l)

        glBegin(GL_LINES)
        glColor(*self.hitbox_color)
        for edge in utils.box_edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()


class Updatable(ABC):
    @abstractmethod
    def update(self, _val):
        raise NotImplementedError()


class Box(Drawable):
    cube_color: Union[None, tuple[int, int, int]]

    def __init__(self, x, y, z, w, h, l, hitbox_color, cube_color) -> None:
        super().__init__(x, y, z, w, h, l, hitbox_color)
        self.cube_color = cube_color

    def display(self):
        if self.cube_color is None:
            return

        vertices = utils.get_box_vertices(self.x, self.y, self.z, self.h, self.w, self.l)

        glBegin(GL_QUADS)
        glColor(self.cube_color)
        for face in utils.box_faces:
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()


class Car(Drawable, Updatable):
    speed: int
    wheel_radius: int = 0.02
    wheel_height: float = 0.02
    wheel_color: tuple[float, float, float]

    glass_color: tuple[float, float, float]
    edge_color: tuple[float, float, float]
    body_color: tuple[float, float, float]

    def __init__(self, x, y, z, w, h, l, speed, hitbox_color, inverse=False) -> None:
        super().__init__(x, y, z, w, h, l, hitbox_color)
        self.speed = speed
        self.inverse = inverse
        self.edge_color = utils.random_color()
        self.body_color = utils.random_color()
        self.wheel_color = (0.5, 0.5, 0.5)
        self.glass_color = (0.137, 0.675, 0.769)

    def update(self, _val):
        self.y += self.speed

    def draw_wheel(self):
        glTranslatef(0, 0, self.wheel_radius)
        glRotatef(90, 0, 1, 0)
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluQuadricNormals(quadric, GLU_SMOOTH)

        gluCylinder(quadric, self.wheel_radius, self.wheel_radius, self.wheel_height, 32, 32)

        gluQuadricOrientation(quadric, GLU_INSIDE)

        gluDisk(quadric, self.wheel_radius / 2, self.wheel_radius, 32, 1)
        glTranslatef(0, 0, self.wheel_height)
        gluDisk(quadric, self.wheel_radius / 2, self.wheel_radius, 32, 1)

        gluDeleteQuadric(quadric)
        glTranslatef(0, 0, -self.wheel_height)
        glRotatef(-90, 0, 1, 0)
        glTranslatef(0, 0, -self.wheel_radius)

    def draw_wheels(self):
        glColor(*self.wheel_color)
        glTranslatef(self.w * 0.5 / 5, self.h * 1 / 4, 0)
        self.draw_wheel()

        glTranslatef(0, self.h * 2 / 4, 0)
        self.draw_wheel()

        glTranslatef(self.w * 3.5 / 5, 0, 0)
        self.draw_wheel()

        glTranslatef(0, -self.h * 2 / 4, 0)
        self.draw_wheel()

        glTranslatef(-self.w * 4 / 5, -self.h / 4, 0)

    def draw_glass(self):
        vertices = (
            (0, 0, 0),
            (0, self.h * 2 / 4, 0),
            (self.w * 7.3 / 10, self.h * 2 / 4, 0),
            (self.w * 7.3 / 10, 0, 0),

            (0, self.h * 0.5 / 4, 2 * self.wheel_radius),
            (0, self.h * 1.5 / 4, 2 * self.wheel_radius),
            (self.w * 7.3 / 10, self.h * 1.5 / 4, 2 * self.wheel_radius),
            (self.w * 7.3 / 10, self.h * 0.5 / 4, 2 * self.wheel_radius),
        )

        glTranslate(self.w * 1.2 / 10, self.h * 0.7 / 4, 2 * self.wheel_radius)

        glColor(self.edge_color)
        glBegin(GL_LINES)
        for edge in utils.box_edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for i, face in enumerate(utils.box_faces):
            if i == 1:
                glColor(*self.body_color)
            else:
                glColor(*self.glass_color)
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

        glTranslate(-self.w * 2 / 10, -self.h * 1 / 4, -2 * self.wheel_radius)

    def draw_body(self):
        glTranslatef(0, 0, 1.5 * self.wheel_radius)

        box = Box(
            self.w * 1.2 / 10, self.h * 1 / 10, 0,
            self.w * 7.3 / 10, self.h * 8 / 10, 2 * self.wheel_radius,
            self.edge_color, self.body_color
        )
        box.display()
        box.display_hit_box()

        self.draw_glass()

        glTranslate(0, 0, -1.5 * self.wheel_radius)

    def display(self):
        if self.inverse:
            glTranslate(-self.x, -self.y, 0)
            glRotatef(180, 0, 0, 1)

        glTranslatef(self.x, self.y, 0.1)
        self.draw_wheels()
        self.draw_body()

        glTranslatef(-self.x, -self.y, -0.1)

        if self.inverse:
            glRotatef(-180, 0, 0, 1)
            glTranslate(self.x, self.y, 0)

    def display_hit_box(self):
        if self.inverse:
            glTranslate(-self.x, -self.y, 0)
            glRotatef(180, 0, 0, 1)

        super().display_hit_box()
        if self.inverse:
            glRotatef(-180, 0, 0, 1)
            glTranslate(self.x, self.y, 0)


class Road(Box):

    def __init__(self, x, y, z, w, h, l, hitbox_color, cube_color) -> None:
        super().__init__(x, y, z, w, h, l, hitbox_color, cube_color)
        self.line_vertices = (
            (0, y, z + l + 0.01),
            (0, y + h, z + l + 0.01)
        )

    def draw_road_line(self):
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, 0xFF00)
        glLineWidth(4)
        glBegin(GL_LINES)
        glColor3f(1, 1, 1)
        for vert in self.line_vertices:
            glVertex3fv(vert)
        glEnd()
        glLineWidth(1)
        glDisable(GL_LINE_STIPPLE)

    def display(self):
        # Draw road
        super().display()

        # Draw road line
        self.draw_road_line()


class Grass(Drawable):

    def __init__(self, x=-1, y=-1, z=0, w=2, h=2, l=0) -> None:
        super().__init__(x, y, z, w, h, l, None)

    def display(self):
        material_id = material.get("grass.jpg")
        glBindTexture(GL_TEXTURE_2D, material_id)

        glBegin(GL_QUADS)
        glTexCoord2f(self.x, self.y)
        glVertex3f(self.x, self.y, self.z)
        glTexCoord2f(self.x + self.w, self.y)
        glVertex3f(self.x + self.w, self.y, self.z)
        glTexCoord2f(self.x + self.w, self.y + self.h)
        glVertex3f(self.x + self.w, self.y + self.h, self.z)
        glTexCoord2f(self.x, self.y + self.h)
        glVertex3f(self.x, self.y + self.h, self.z)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)


class Simulation(Drawable):
    items: list[Drawable]
    update_time: int
    window_name: str
    width: int
    height: int
    hitboxes: bool
    update_counter: int = 0

    def __init__(
            self,
            width,
            height,
            hitboxes=False,
            update_time=1000,
            window_name="Window"
    ):
        self.update_time = update_time
        self.window_name = window_name
        self.width = width
        self.height = height
        self.hitboxes = hitboxes

        road = Road(-0.6, -20, 0, 1.2, 40, 0.1, (1, 0, 0), (0, 0, 0))
        grass = Grass(-5, -5, 0, 10, 10, 0)

        self.items = [road, grass]

    def add_drawable(self, drawable: Drawable):
        self.items.append(drawable)

    def spawn_random_car(self, left=False, right=False):
        if left and right or not left and not right:
            raise NotImplementedError()

        if left:
            speed = random.uniform(0.02, 0.023)
            x = random.uniform(-0.55, -0.25)
            y = random.uniform(-1.6, -1.3)
            car = Car(x, y, 0.1, 0.2, 0.3, 0.1, speed, hitbox_color=(1, 0, 0))
        else:
            speed = random.uniform(0.01, 0.011)
            x = random.uniform(-0.25, -0.15)
            y = random.uniform(-1.8, -1.6)
            car = Car(x, y, 0.1, 0.2, 0.3, 0.1, speed, hitbox_color=(1, 0, 0), inverse=True)
        return car

    def manage_drawables(self):
        if self.update_counter % 50 == 0:
            left_car = self.spawn_random_car(left=True)
            right_car = self.spawn_random_car(right=True)
            self.add_drawable(left_car)
            self.add_drawable(right_car)

        if self.update_counter % 100 == 0 and len(self.items) > 3 and self.update_counter > 200:
            self.items = self.items[:2] + self.items[6:]

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0.6, -1.1, 1.4, 0, 0, 0, 0, 0, 1)
        # gluLookAt(1.5, -1.0, 0.7, 0, 0, 0, 0, 0, 1)
        # gluLookAt(1, -2, 5, 0, 0, 0, 0, 0, 1)
        # gluLookAt(0, 1, 5, 0, 0, 0, 0, 0, 1)

        for item in self.items:
            if self.hitboxes:
                item.display_hit_box()
            item.display()

        glutSwapBuffers()

    def update(self, _val):
        self.manage_drawables()
        updatable = [i for i in self.items if isinstance(i, Updatable)]
        for item in updatable:
            item.update(_val)

        glutPostRedisplay()
        self.update_counter += 1
        glutTimerFunc(self.update_time, self.update, 0)

    def start(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(self.window_name)
        self.init()
        glutDisplayFunc(self.display)
        glutTimerFunc(self.width, self.update, 0)
        glutReshapeFunc(self.reshape)
        glutMainLoop()

    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, self.width / self.height, 1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def init(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)


sim = Simulation(width=600, height=600, update_time=1, hitboxes=False)
sim.start()
