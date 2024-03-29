import cv2 as cv
import utils


def prepare_image(init):
    adjusted = utils.adjust_contrast_and_brightness(init, contrast=3, brightness=50)
    # cv.imshow("Contrast and brightness", adjusted)

    k_means = utils.k_means(adjusted, k=10)
    # cv.imshow("K-means", k_means)

    gray = cv.cvtColor(k_means, cv.COLOR_BGR2GRAY)
    # cv.imshow("Gray", gray)

    bil_blured = cv.bilateralFilter(gray, 7, 50, 50)
    # cv.imshow("Bilateral blured", bil_blured)

    gauss_thresh = cv.adaptiveThreshold(bil_blured, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 9, 5)
    # cv.imshow("Thresh", gauss_thresh)

    opening = cv.morphologyEx(gauss_thresh, cv.MORPH_OPEN, (3, 3))
    # cv.imshow("Opening", opening)

    return opening


def ident_solar_panels(initial):
    # cv.imshow("Initial example 2", initial)

    prepared = prepare_image(initial)
    contours, hierarchies = cv.findContours(prepared, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    contoured = initial.copy()
    solar_panel_area = 0

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        area = cv.contourArea(contour)
        perimeter = cv.arcLength(contour, True)
        rect_area = w * h

        if w > 55 or h > 55 or w < 10 or h < 10:
            continue

        if area > 2500 or area < 100:
            continue

        if perimeter > 400 or perimeter < 40:
            continue

        if utils.is_not_in_mask(x, y):
            continue

        # cv.drawContours(contoured, [contour], -1, (0, 255, 0), thickness=2)
        cv.rectangle(contoured, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)
        solar_panel_area += rect_area

    panels_number = utils.area_to_panel(solar_panel_area)
    return contoured, panels_number
