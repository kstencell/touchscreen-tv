import cv2
import numpy as np
from process_image_library import RedMaskAndBinary

# Load image
image = cv2.imread('200_test_with_points.jpg')

### DELETE EVERYTHING THAT'S NOT RED IN ORIGINAL IMAGE AND CONVERT TO BLACK/WHITE
image_copy = image.copy()
only_red_binary = RedMaskAndBinary(image_copy)
cv2.imshow("Only Red Binary", only_red_binary)

params = cv2.SimpleBlobDetector_Params()
params.filterByColor = True
params.blobColor = 255
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(only_red_binary)

# for point in keypoints:
#     print("x: ", point.pt[0])
#     print("y: ", point.pt[1])

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(image, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)