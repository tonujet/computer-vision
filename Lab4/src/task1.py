import model
import cv2

img = cv2.imread("example2.png")
cars = model.follow_cars(img)
cv2.imshow("Cars", cars)
cv2.waitKey(0)
cv2.destroyAllWindows()
