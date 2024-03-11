import cv2
import numpy as np


def show_image(image):
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_image(image):
    lower_color = np.array([170, 170, 170])
    upper_color = np.array([210, 210, 210])
    mask = cv2.inRange(image, lower_color, upper_color)
    image = image.copy()
    image[mask > 0] = (255, 255, 255)

    lower_color = np.array([60, 60, 60])
    upper_color = np.array([200, 200, 190])
    mask = cv2.inRange(image, lower_color, upper_color)
    image[mask > 0] = (255, 255, 255)
    show_image(image)

    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (1, 1), 0)
    edged = cv2.Canny(blur, 100, 100)
    cv2.imshow("Blur", blur)
    cv2.imshow("Grey", grey)
    show_image(edged)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    show_image(closed)

    return closed


def image_recognition(start_image, processed_image):
    image_cont = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    final_image = start_image.copy()
    cv2.drawContours(final_image, image_cont, -1, (0, 255, 0), 3)
    return final_image


start_image = cv2.imread("example.jpg")
show_image(start_image)
processed_image = process_image(start_image)
final_image = image_recognition(start_image, processed_image)
show_image(final_image)
cv2.imwrite("processed-example.jpg", final_image)
