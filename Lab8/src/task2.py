import task1
import cv2 as cv


def rescale_frame(frame, scale: float = 1.0):
    h, w = frame.shape[:2]
    new_width = int(w * scale)
    new_height = int(h * scale)

    return cv.resize(frame, (new_width, new_height), interpolation=cv.INTER_AREA)


def get_frame(cap, cap_name, scale):
    if not cap.isOpened():
        raise IOError()

    ret, frame = cap.read()
    scaled = rescale_frame(frame, scale=scale)
    cv.imshow(cap_name, scaled)

    if not ret:
        raise IOError()

    return scaled


if __name__ == "__main__":
    cap1 = cv.VideoCapture("1_1.mp4")
    cap2 = cv.VideoCapture("2_1.mp4")
    task1.start_loop(
        lambda: get_frame(cap1, "video1", scale=0.6),
        lambda: get_frame(cap2, "video2", scale=0.6)
    )
