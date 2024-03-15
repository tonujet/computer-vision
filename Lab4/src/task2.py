import cv2
import model

cap = cv2.VideoCapture('example.mp4')
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# print(width, height)
# out = cv2.VideoWriter('modified_example.mp4', -1, 20.0, (int(width), int(height)))
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cars = model.follow_cars(frame)
        # out.write(cars)
        cv2.imshow("Cars", cars)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
# out.release()
cv2.destroyAllWindows()
