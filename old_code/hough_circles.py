import numpy as np
import cv2 as cv
from process_image_library import RedMaskAndBinary

src_img = cv.imread('200_test_with_points.jpg')
image_copy = src_img.copy()

only_red_binary = RedMaskAndBinary(image_copy)
cv.imshow("Only Red Binary", only_red_binary)

circles_img = cv.HoughCircles(only_red_binary, cv.HOUGH_GRADIENT, 1, 10, 100, 50, 1, 100)
circles_img = np.uint16(np.around(circles_img))

for i in circles_img[0,:]:
    cv.circle(image_copy,(i[0],i[1]),i[2],(0,255,0),2)
    cv.circle(image_copy,(i[0],i[1]),2,(0,0,255),3)

cv.imshow('Original Image',src_img)
cv.imshow('Detected Circles',image_copy)
cv.waitKey(0)
cv.destroyAllWindows()