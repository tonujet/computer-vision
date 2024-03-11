import numpy as np


def calc_points_with_lagrange_interpolation(points, point_num):
    first_x, last_x = points[0, 0], points[-1, 0]
    first_z, last_z = points[0, 2], points[-1, 2]
    diff_x, diff_z = last_x - first_x, last_z - first_z

    if diff_x == 0:
        return lagrange_interpolation_fix(points, point_num)

    res_points = np.ones((point_num, 4))

    step_x = diff_x / (point_num - 1)
    step_z = diff_z / (point_num - 1)

    for num in range(0, point_num):
        x = first_x + num * step_x
        y = lagrange_interpolation(x, points)
        z = first_z + num * step_z
        res_points[num, 0] = x
        res_points[num, 1] = y
        res_points[num, 2] = z

    return res_points


def lagrange_interpolation(x, points):
    res = 0
    for index, point in enumerate(points):
        point_x = point[0]
        point_y = point[1]
        pol = point_y
        for curr_index, curr_point in enumerate(points):
            if index == curr_index:
                continue
            curr_x = curr_point[0]

            try:
                pol *= (x - curr_x) / (point_x - curr_x)
            except:
                continue
        res += pol
    return res


# Interpolation fix for the points with the same x.
# In such cases lagrange interpolation doesn't work
def lagrange_interpolation_fix(points, point_num):
    first_y, last_y = points[0, 1], points[-1, 1]
    first_z, last_z = points[0, 2], points[-1, 2]
    diff_y, diff_z = last_y - first_y, last_z - first_z

    step_y = diff_y / (point_num - 1)
    step_z = diff_z / (point_num - 1)

    res_points = np.ones((point_num, 4))

    for num in range(0, point_num):
        y = first_y + num * step_y
        z = first_z + num * step_z
        res_points[num, 1] = y
        res_points[num, 0] = points[0, 0]
        res_points[num, 2] = z

    return res_points
