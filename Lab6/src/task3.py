import cv2 as cv
import utils

trackers = {
    'MEANSHIFT': utils.MeanShiftTracker(),
    'CAMSHIFT': utils.CamShiftTracker(),
    'BOOSTING': cv.legacy.TrackerBoosting_create(),
    'MIL': cv.TrackerMIL_create(),
    'KCF': cv.TrackerKCF_create(),
    'TLD': cv.legacy.TrackerTLD_create(),
    'MEDIANFLOW': cv.legacy.TrackerMedianFlow_create(),
    'MOSSE': cv.legacy.TrackerMOSSE_create(),
    'CSRT': cv.TrackerCSRT_create(),
}


cap = cv.VideoCapture('example1.mp4')
# width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
# out = cv.VideoWriter('player2.mp4', -1, 20.0, (int(width), int(height)))

tracker = trackers['CSRT']
ret, frame = cap.read()
bbox = cv.selectROI(frame)
cv.destroyAllWindows()

tracker.init(frame, bbox)

bboxes = []

while cap.isOpened():
    # time.sleep(0.02)
    ret, frame = cap.read()
    if cv.waitKey(1) == ord('q') or not ret:
        break

    ok, bbox = tracker.update(frame)
    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)

    # out.write(frame)
    cv.imshow("Video", frame)
