from scipy import ndimage
import cv2 as cv
import numpy as np

KOEF_PIXEL_SQUARE_TO_PANEL = 9.2
area_to_panel = lambda area: int(area * KOEF_PIXEL_SQUARE_TO_PANEL * 0.9)


def Robert(init):
    roberts_cross_v = np.array([
        [1, 0],
        [0, -1]
    ])
    roberts_cross_h = np.array([
        [0, 1],
        [-1, 0]
    ])

    img = init.astype('float64')
    img /= 255.0

    vertical = ndimage.convolve(img, roberts_cross_v)
    horizontal = ndimage.convolve(img, roberts_cross_h)

    edged_img = np.sqrt(np.square(horizontal) + np.square(vertical))
    edged_img *= 255
    return edged_img


def k_means(img, k=10):
    Z = img.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv.kmeans(Z, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    return res.reshape((img.shape))


def adjust_contrast_and_brightness(img, contrast: float = 1.0, brightness: int = 0):
    brightness += int(round(255 * (1 - contrast) / 2))
    return cv.addWeighted(img, contrast, img, 0, brightness)


def is_not_in_mask(x, y):
    return x < 215 and y > 270 or \
        x > 120 and y < 80 or \
        615 < x < 713 and y > 205 or \
        515 < x < 620 and 125 < y < 420 or \
        0 < x < 116 and y > 120 or \
        410 < x < 620 and 140 < y < 310 or \
        210 < x < 420 and y > 480
