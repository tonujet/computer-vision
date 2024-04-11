import cv2 as cv
import numpy as np
import utils
import lab5.example1 as l51
import lab5.example2 as l52


def orb_match(img1, img2, roi=False):
    if roi:
        img1 = utils.select_roi(img1)

    orb = cv.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

    matches = bf.match(des1, des2)

    img3 = cv.drawMatches(img1, kp1, img2, kp2, matches, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    return img3


def sift_match(img1, img2, roi=False):
    if roi:
        img1 = utils.select_roi(img1)

    sift = cv.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    img3 = cv.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    return img3


def flann_match(img1, img2, mask1=None, mask2=None, roi=False):
    img1_init = img1
    img2_init = img2
    if mask1 is not None:
        img1 = cv.bitwise_and(img1, mask1)
        cv.imshow("Img 1 masked", img1)
    if mask2 is not None:
        img2 = cv.bitwise_and(img2, mask2)
        cv.imshow("Img 2 masked", img2)

    if roi:
        img1 = utils.select_roi(img1)

    sift = cv.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Need to draw only good matches, so create a mask and fill it
    match_counter = 0
    matchesMask = [[0, 0] for i in range(len(matches))]
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            match_counter += 1
            matchesMask[i] = [1, 0]
    ident_ratio = match_counter / len(des1)

    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=cv.DrawMatchesFlags_DEFAULT)

    img3 = cv.drawMatchesKnn(img1_init, kp1, img2_init, kp2, matches, None, **draw_params)
    return img3, ident_ratio


img1 = cv.imread("example1.png")
img2 = cv.imread("example2.png")
# cv.imshow("Img 1", img1)
# cv.imshow("Img 2", img2)

mask1 = l51.ident_solar_panels(img1)[-1]
mask2 = l52.ident_solar_panels(img2)[-1]
# cv.imshow("Mask 1", mask1)
# cv.imshow("Mask 2", mask2)

res, ident_ratio = flann_match(img1, img2, mask1=mask1, mask2=mask2, roi=False)
cv.imshow("Flann", res)
print("Identification ratio: ", ident_ratio)

# res2 = sift_match(img1, img2, roi=False)
# cv.imshow("Sift", res2)
#
# res3 = orb_match(img1, img2, roi=False)
# cv.imshow("Orb", res3)


cv.waitKey(0)
cv.destroyAllWindows()
