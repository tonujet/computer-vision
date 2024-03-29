import cv2 as cv
import utils


def prepare_image(initial):
    bil_blured = cv.bilateralFilter(initial, 9, 75, 75)
    # cv.imshow("Bilateral blur", bil_blured)

    gray = cv.cvtColor(bil_blured, cv.COLOR_BGR2GRAY)
    # cv.imshow("Gray", gray)

    gauss_blured = cv.GaussianBlur(gray, (3, 3), cv.BORDER_DEFAULT)
    # cv.imshow("Gaussian blur", gauss_blured)

    gauss_thresh = cv.adaptiveThreshold(gauss_blured, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 9, 1)
    # cv.imshow("Gaussian Thresh", gauss_thresh)

    median_blured = cv.medianBlur(gauss_thresh, 5)
    # cv.imshow("Median blur", median_blured)

    dilated = cv.dilate(median_blured, (3, 3), iterations=2)
    # cv.imshow("Dilated", dilated)
    return dilated


def ident_solar_panels(initial):
    # cv.imshow("Initial example1", initial)

    prepared = prepare_image(initial)
    contours, hierarchies = cv.findContours(prepared, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contoured = initial.copy()
    solar_panel_area = 0

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        area = cv.contourArea(contour)
        perimeter = cv.arcLength(contour, True)
        rect_area = w * h

        if w > 55 or h > 55 or w < 10 or h < 10:
            continue

        if area > 2500 or area < 150:
            continue

        if perimeter > 220 or perimeter < 40:
            continue

        if h < w / 3 or w < h / 3:
            continue

        if utils.is_not_in_mask(x, y):
            continue

        cv.rectangle(contoured, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)
        solar_panel_area += rect_area

    panels_number = utils.area_to_panel(solar_panel_area)
    return contoured, panels_number
