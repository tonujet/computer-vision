import cv2
import numpy as np
import histogram

Y_CROP_OFFSET = 350
X_CROP_OFFSET = 200
MAX_CAR_WIDTH = 150
MIN_CAR_WIDTH = 20
MAX_DISTANT = 310


# use black mask to unused areas
def mask_image(img):
    img = histogram.hist_correction(img)
    h, w, *_ = img.shape
    mask = np.zeros((h, w), dtype=np.uint8)
    points = np.array([[[0, 0], [0, h], [90, h], [440, 295], [600, 295], [1140, h], [w, h], [w, 0], [0, 0]]])
    cv2.fillPoly(mask, points, (255))
    img[mask > 0] = 255
    return img


# Change contrast and brightness
def adjust_contrast_brightness(img, contrast: float = 1.0, brightness: int = 0):
    brightness += int(round(255 * (1 - contrast) / 2))
    return cv2.addWeighted(img, contrast, img, 0, brightness)


# Cars identification
def image_ident(init_img, processed_img, additional_contours=False):
    img_h, img_w, *_ = init_img.shape
    contours = cv2.findContours(processed_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    ident_image = init_img.copy()

    relative_koef = MIN_CAR_WIDTH * (img_h - MAX_CAR_WIDTH) / (MAX_CAR_WIDTH * MAX_DISTANT)
    lower_bound = MAX_CAR_WIDTH - MIN_CAR_WIDTH
    upper_bound = MAX_CAR_WIDTH * 1 / relative_koef
    is_in_bound = lambda x: lower_bound < x < upper_bound

    counter = 1
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if additional_contours:
            cv2.drawContours(ident_image, [contour], -1, (0, 255, 0), 2)
            cv2.rectangle(ident_image, (x, y), (x + w - 1, y + h - 1), (255, 255, 255), 2)

        if w < MIN_CAR_WIDTH or h < MIN_CAR_WIDTH:
            continue

        projection = lambda x: (x * (img_h - MAX_CAR_WIDTH)) / (relative_koef * y)
        w_proj = projection(w)
        h_proj = projection(h)

        if not (is_in_bound(w_proj) and is_in_bound(h_proj)):
            continue

        cv2.rectangle(ident_image, (x, y), (x + w - 1, y + h - 1), 255, 2)
        cv2.putText(ident_image, f'Car #{counter}', (x, y - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,
                    (0, 0, 255), 1, cv2.LINE_AA)
        counter += 1
    return ident_image


# Process image
def image_procession(img):
    # color correction
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # cv2.imshow("RGB image", rgb_image)

    # filtering
    noise_consumed_image = cv2.blur(rgb_image, (6, 6))
    # cv2.imshow("Noise consumed image", noise_consumed_image)

    sharpen_kernel = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]
    ])
    sharpen_img = cv2.filter2D(noise_consumed_image, -1, kernel=sharpen_kernel)
    # cv2.imshow("Sharpen image", sharpen_img)

    adjusted_img = adjust_contrast_brightness(sharpen_img, 1.5, 20)
    # cv2.imshow("Brighten kernel", adjusted_img)

    greyscape = cv2.cvtColor(adjusted_img, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(greyscape, (5, 5), 0)
    # cv2.imshow("Blurred greyscape", blurred_img)

    # vectorization
    edged = cv2.Canny(blurred_img, 1, 200)
    # cv2.imshow("Edged image", edged)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    transformed_image = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("Morphological transformation", transformed_image)
    return transformed_image


# Final api function that allows track cars
def follow_cars(img):
    masked_image = mask_image(img)
    processed_image = image_procession(masked_image)
    return image_ident(img, processed_image, additional_contours=False)
