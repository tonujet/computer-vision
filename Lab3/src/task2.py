import tkinter
from graphics import *
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
    [100, 0, 50, 1],
    [0, 0, 50, 1],

    [50, 50, 200, 1],
    [0, 100, 50, 1],
    [0, 0, 50, 1],

    [50, 50, 200, 1],
    [100, 100, 50, 1],
    [0, 100, 50, 1],

    [50, 50, 200, 1],
    [100, 0, 50, 1],
    [100, 100, 50, 1],

    # return to center
    [0, 100, 50, 1],
    [0, 0, 50, 1],

])

root = tkinter.Tk()
root.title("3d graphics")
root.geometry("1200x600")
canvas = tkinter.Canvas(root, bg="white", bd=0, border=0, width=1200, height=600, background="white")
canvas.pack()

# === Task 1 === #
pyramid1 = Pyramid(canvas, points)
pyramid1.set_color(3, "red")
pyramid1.move(100, 300)
pyramid1.rotate(angle_x=0, angle_y=55, angle_z=90)
pyramid1.draw_using_lagrange_interpolation(point_num=170)

pyramid2 = Pyramid(canvas, points)
pyramid2.set_color(3, "green")
pyramid2.move(250, 300)
pyramid2.rotate(angle_x=0, angle_y=55, angle_z=90)
pyramid2.draw()

# === Task 2 === #
colors = ["red", "grey", "green", "#FF8C00", "purple"]

# pyramid3 = Pyramid(canvas, points)
# pyramid3.move(500, 400)
# pyramid3.rotate(angle_x=0, angle_y=55, angle_z=90)
# pyramid3.draw_using_lagrange_interpolation_and_z_buffer(point_num=170, colors=colors)
#
# pyramid4 = Pyramid(canvas, points)
# pyramid4.move(700, 400)
# pyramid4.rotate(angle_x=-45, angle_y=-45, angle_z=45)
# pyramid4.draw_using_lagrange_interpolation_and_z_buffer(point_num=170, colors=colors)
#
# pyramid7 = Pyramid(canvas, points)
# pyramid7.move(900, 400)
# pyramid7.rotate(angle_z=-30, angle_x=110, angle_y=-30)
# pyramid7.draw_using_lagrange_interpolation_and_z_buffer(point_num=170, colors=colors)

pyramid5 = Pyramid(canvas, points)
pyramid5.move(500, 100)
pyramid5.draw_using_lagrange_interpolation_and_z_buffer(point_num=170, colors=colors)

pyramid6 = Pyramid(canvas, points)
pyramid6.move(700, 100)
pyramid6.rotate(angle_z=45, angle_x=180)
pyramid6.draw_using_lagrange_interpolation_and_z_buffer(point_num=170, colors=colors)

pyramid8 = Pyramid(canvas, points)
pyramid8.move(900, 100)
pyramid8.rotate(angle_z=30, angle_x=33, angle_y=-60)
pyramid8.draw_using_lagrange_interpolation_and_z_buffer(point_num=170, colors=colors)

root.mainloop()
