import random
import time

from graphics import *
import tkinter as tk
import numpy as np

points = np.array([
    # base
    [0, 0, 50, 1],
    [0, 100, 50, 1],
    [100, 100, 50, 1],
    [100, 0, 50, 1],
    [0, 0, 50, 1],

    # triangles
    [50, 50, 200, 1],
    [100, 100, 50, 1],
    [100, 100, 50, 1],
    [50, 50, 200, 1],
    [0, 100, 50, 1],
    [50, 50, 200, 1],
    [100, 0, 50, 1],

])


def draw_axes(canvas):
    canvas_width = canvas.winfo_reqwidth()
    canvas_height = canvas.winfo_reqheight()
    center_x = canvas_width // 2
    center_y = canvas_height // 2

    # X-axis
    canvas.create_line(0, center_y, canvas_width, center_y, arrow=tk.LAST, width=2, dash=True)
    canvas.create_text(canvas_width - 5, center_y + 5, text="X", anchor=tk.NE)

    # Y-axis
    canvas.create_line(center_x, canvas_height, center_x, 0, arrow=tk.LAST, width=2, dash=True)
    canvas.create_text(center_x - 10, 5, text="Y", anchor=tk.NE)


root = tk.Tk()
root.title("3d graphics")
root.geometry("805x605")
canvas = tk.Canvas(root, bg="white", bd=0, border=0, width=800, height=600, background="skyblue")
canvas.pack()
canvas.bind("<Configure>", lambda event: draw_axes(canvas))

pyramid1 = Pyramid(canvas, points)
pyramid2 = Pyramid(canvas, points)
pyramid3 = Pyramid(canvas, points)

pyramid1.move(400 - 50, 300 - 50)
pyramid2.move(222, 333)
pyramid3.move(111, 111)

counter = 0
while True:
    time.sleep(0.02)
    counter += 1
    if counter == 50:
        canvas.delete(pyramid1.tags)
        canvas.delete(pyramid2.tags)
        canvas.delete(pyramid3.tags)
        pyramid1.set_random_outline()
        pyramid2.set_random_outline()
        pyramid3.set_random_outline()
        pyramid1.random_scale()
        pyramid2.random_scale()
        pyramid3.random_scale()
        counter = -50
    if counter > 0:
        pyramid1.redraw()
        pyramid2.redraw()
        pyramid3.redraw()

    pyramid1.rotate(1, 10, 5)
    pyramid2.rotate(2, -1, 10)
    pyramid3.rotate(1, -3, -3)

    pyramid1.move(counter, -3, counter / 10)
    pyramid2.move(counter, -1, counter / 10)
    pyramid3.move(counter / 3, counter / 3, counter / 33)
    root.update()
