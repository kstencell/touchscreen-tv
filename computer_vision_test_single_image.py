import cv2
import time
from process_image_library import *
import globals
import glob
import os

# Load image
image = cv2.imread('200_test_with_arm_and_pointer.jpg')
# image = cv2.imread('./images/testing_images/camera2/img008.jpg')
# image = cv2.imread('./images/testing_images/{}/img.jpg'.format(name))
# image = cv2.imread(latest_file)
image_copy = image.copy()

# cv2.imshow("Original: thread {}".format(thread_num), image)

### DELETE EVERYTHING THAT'S NOT RED IN ORIGINAL IMAGE AND CONVERT TO BLACK/WHITE
only_red_binary = RedMaskAndBinary(image_copy)
cv2.imshow("Only Red Binary", only_red_binary)

#### GET AVERAGE LINE ON ALL FOUR SIDES ####
lines = GetAverageLines(only_red_binary)

# #### CALCULATE INTERSECTIONS OF LINES #####
intersections = GetIntersections(lines)

# # #### SHOW WHAT COMPUTER SEES ####
canvas = DrawOnCanvas(intersections, lines)
cv2.imshow("Computer Vision", canvas)

# ### FIND LARGEST CONTOUR (SHOULD BE TV OUTLINE) USED FOR DETERMINING IF DOTS ARE ON SCREEN OR OFF SCREEN
contour = GetLargestContour(only_red_binary)

# ### APPROXIMATE CONVEX HULL FROM BROKEN QUADRILATERAL CONTOUR
hull = cv2.convexHull(contour)

# ### DETECT ALL WHITE DOTS IN IMAGE
all_dots = DotDetector(only_red_binary)

# ### GET ONLY POINTS THAT ARE INSIDE SCREEN CONTOUR (CENTER OF DOTS SPECIFICALLY)
points_on_screen = GetPointsInsideContour(all_dots, hull)

VisualizePointsOnScreen(points_on_screen, image.copy())

# ### TRANSFORM QUADRILATERAL PLANE TO RECTANGLE (TV) AND USE TRANSFORM ON POINTS
transformed_point = TransformToRectangle(intersections, points_on_screen)[0]

# # globals.points_from_cameras[index] = transformed_point

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()