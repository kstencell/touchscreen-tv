import cv2
import numpy as np
from skimage.transform import ProjectiveTransform
import matplotlib.pyplot as plt
from process_image_library import *

# Load image
# image = cv2.imread('200_test_with_points.jpg')
image = cv2.imread('200_test_with_arm_and_pointer.jpg')

### DELETE EVERYTHING THAT'S NOT RED IN ORIGINAL IMAGE AND CONVERT TO BLACK/WHITE
image_copy = image.copy()
only_red_binary = RedMaskAndBinary(image_copy)
cv2.imshow("Only Red Binary", only_red_binary)

### FIND LARGEST CONTOUR (SHOULD BE TV OUTLINE)
largest_contour = GetLargestContour(only_red_binary)
# cv2.drawContours(image_copy, largest_contour, -1, (0,255,0), 1)
# cv2.imshow("draw largest contour", image_copy)

scaled_contour = ScaleContour(largest_contour, 0.96)

### APPROXIMATE CONVEX HULL FROM BROKEN QUADRILATERAL CONTOUR
hull = cv2.convexHull(scaled_contour)

VisualizeConvexHull(hull, image.copy())

### DETECT ALL WHITE DOTS IN IMAGE
all_dots = DotDetector(only_red_binary)

### GET ONLY POINTS THAT ARE INSIDE SCREEN CONTOUR (CENTER OF DOTS SPECIFICALLY)
points_on_screen = GetPointsInsideContour(all_dots, hull)

VisualizePointsOnScreen(points_on_screen, image.copy())

### GET CORNERS OF APPROXIMATED QUADRILATERAL FROM CONTOUR
tv_corners = GetCornersOfContour(hull)

VisualizeContourCorners(tv_corners, image.copy())

print(tv_corners)

cv2.imshow('Original', image)

### TRANSFORM QUADRILATERAL PLANE TO RECTANGLE (TV) AND USE TRANSFORM ON POINTS
transformed_points = TransformToRectangle_Contour(tv_corners, points_on_screen)

cv2.waitKey()