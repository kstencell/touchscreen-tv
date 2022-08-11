from process_image_line_detection import ProcessTestImages
import cv2

# CAMERA 1 ON LEFT SIDE OF TV
# CAMERA 2 ON RIGHT SIDE OF TV

# ProcessTestImages(directory='test_center', camera_num=1)
# ProcessTestImages(directory='test_center', camera_num=2)

# ProcessTestImages(directory="test_bottom_left", camera_num=1)
ProcessTestImages(directory="test_bottom_left", camera_num=2)

# ProcessTestImages(name='test_bottom_right/camera1')
# ProcessTestImages(name='test_bottom_right/camera2')

# ProcessTestImages(directory='test_top_right', camera_num=1)
# ProcessTestImages(directory='test_top_right', camera_num=2)

# ProcessTestImages(name='test_top_left/camera1')
# ProcessTestImages(name='test_top_left/camera2')

cv2.waitKey(0)
cv2.destroyAllWindows()