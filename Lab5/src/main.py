import cv2 as cv
import example1 as ex1
import example2 as ex2


ex1_img = cv.imread("example1.png")
cv.imshow("Example 1", ex1_img)
ex1_panels, ex1_panels_num = ex1.ident_solar_panels(ex1_img)
cv.imshow("Example 1 panels", ex1_panels)
print(f"On the image approximately {ex1_panels_num} solar panels")

ex2_img = cv.imread("example2.png")
cv.imshow("Example 2", ex2_img)
ex2_panels, ex2_panels_num = ex2.ident_solar_panels(ex2_img)
cv.imshow("Example 2 panels", ex2_panels)
print(f"On the image approximately {ex2_panels_num} solar panels")

cv.waitKey(0)
cv.destroyAllWindows()
