from process_image_line_detection import ProcessTestImages
import cv2

# ProcessTestImages(name='test_center/camera1')
# ProcessTestImages(name='200_test_with_arm_and_pointer')
# ProcessTestImages(name='test_center/camera2')

# ProcessTestImages(name='test_bottom_left/camera1')
ProcessTestImages(name='test_bottom_left/camera2')

# ProcessTestImages(name='test_bottom_right/camera1')
# ProcessTestImages(name='test_bottom_right/camera2')

# ProcessTestImages(name='test_top_right/camera1')
# ProcessTestImages(name='test_top_right/camera2')

# ProcessTestImages(name='test_top_left/camera1')
# ProcessTestImages(name='test_top_left/camera2')

cv2.waitKey(0)
cv2.destroyAllWindows()