import random

box_faces = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
    (0, 3, 7, 4),
    (1, 2, 6, 5),
)

box_edges = (
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
)


def get_box_vertices(x, y, z, h, w, l):
    return (
        (x + w, y, z + l),
        (x + w, y + h, z + l),
        (x, y + h, z + l),
        (x, y, z + l),
        (x + w, y, z),
        (x + w, y + h, z),
        (x, y + h, z),
        (x, y, z),
    )


def random_color() -> tuple[float, float, float]:
    color = lambda: random.uniform(0, 1)
    return color(), color(), color()
