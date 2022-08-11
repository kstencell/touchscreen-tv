import cv2
import time
from process_image_library import *
import globals
import glob
import os
from scipy.spatial import ConvexHull

def ProcessImages(thread_num=0, index=0, directory="null", camera_num="null"):

    while(True):
        try:

            # find most recent file
            list_of_files = glob.glob(f'./images/testing_images/{directory}/*.jpg')
            latest_file = max(list_of_files, key=os.path.getctime)

            # Load image
            # image = cv2.imread('200_test_with_arm_and_pointer.jpg')
            # image = cv2.imread(f'./images/test_center/{name}.jpg')
            # image = cv2.imread('./images/testing_images/{}/img.jpg'.format(name))
            image = cv2.imread(latest_file)
            image_copy = image.copy()

            cv2.imshow("Original: thread {}".format(thread_num), image)

            ### DELETE EVERYTHING THAT'S NOT RED IN ORIGINAL IMAGE AND CONVERT TO BLACK/WHITE
            only_red_binary = RedMaskAndBinary(image_copy)
            cv2.imshow("Only Red Binary", only_red_binary)

            #### GET AVERAGE LINE ON ALL FOUR SIDES ####
            lines = GetAverageLines(only_red_binary)

            #### CALCULATE INTERSECTIONS OF LINES #####
            intersections = GetIntersections(lines)

            #### SHOW WHAT COMPUTER SEES ####
            canvas = DrawOnCanvas(intersections, lines)
            cv2.imshow("Computer Vision", canvas)

            ### FIND LARGEST CONTOUR (SHOULD BE TV OUTLINE) USED FOR DETERMINING IF DOTS ARE ON SCREEN OR OFF SCREEN
            contour = GetLargestContour(only_red_binary)

            ### APPROXIMATE CONVEX HULL FROM BROKEN QUADRILATERAL CONTOUR
            hull = cv2.convexHull(contour)

            ### DETECT ALL WHITE DOTS IN IMAGE
            all_dots = DotDetector(only_red_binary)

            ### GET ONLY POINTS THAT ARE INSIDE SCREEN CONTOUR (CENTER OF DOTS SPECIFICALLY)
            points_on_screen = GetPointsInsideContour(all_dots, hull)

            # VisualizePointsOnScreen(points_on_screen, image.copy())

            ### TRANSFORM QUADRILATERAL PLANE TO RECTANGLE (TV) AND USE TRANSFORM ON POINTS
            transformed_point = TransformToRectangle(intersections, points_on_screen)[0]

            globals.points_from_cameras[index] = transformed_point

            cv2.waitKey(0)
            cv2.destroyAllWindows()

            print("Thread {} processed an image".format(thread_num), flush=True)
        except:
            pass
            # print("error")

def ProcessTestImages(thread_num=0, index=0, directory="null", camera_num="null"):

    # Load image
    # image = cv2.imread('200_test_with_arm_and_pointer.jpg')
    image = cv2.imread(f'./images/{directory}/camera{camera_num}.jpg')
    # cv2.imshow("Original", image)

    # image = cv2.imread('./images/testing_images/{}/img.jpg'.format(name))
    # image = cv2.imread(latest_file)
    image_copy = image.copy()

    ### DELETE EVERYTHING THAT'S NOT RED IN ORIGINAL IMAGE AND CONVERT TO BLACK/WHITE
    only_red_binary = RedMaskAndBinary(image_copy)
    # cv2.imshow("Only Red Binary", only_red_binary)

    #### GET AVERAGE LINE ON ALL FOUR SIDES ####
    lines = GetAverageLines(only_red_binary)

    #### CALCULATE INTERSECTIONS OF LINES #####
    intersections = GetIntersections(lines)
    # print("Intersections: ", intersections)

    #### SHOW WHAT COMPUTER SEES ####
    canvas = DrawOnCanvas(intersections, lines)
    # cv2.imshow("Computer Vision", canvas)

    ### FIND LARGEST CONTOUR (SHOULD BE TV OUTLINE) USED FOR DETERMINING IF DOTS ARE ON SCREEN OR OFF SCREEN
    contour = GetLargestContour(canvas)
    scaled_contour = ScaleContour(contour, 0.95)
    contour_image = cv2.drawContours(image, [scaled_contour], -1, (255, 0, 0), 2)
    # cv2.imshow("Contour", contour_image)

    ### APPROXIMATE CONVEX HULL FROM BROKEN QUADRILATERAL CONTOUR
    # points = np.array([intersections[0][0], intersections[1][0], intersections[2][0], intersections[3][0]])
    # print(points)

    ### DETECT ALL WHITE DOTS IN IMAGE
    all_dots = DotDetector(only_red_binary)

    ### GET ONLY POINTS THAT ARE INSIDE SCREEN CONTOUR (CENTER OF DOTS SPECIFICALLY)
    points_on_screen = GetPointsInsideContour(all_dots, scaled_contour)

    # VisualizePointsOnScreen(points_on_screen, canvas.copy())

    ### TRANSFORM QUADRILATERAL PLANE TO RECTANGLE (TV) AND USE TRANSFORM ON POINTS
    transformed_point = TransformToRectangle(intersections, points_on_screen)[0]

    ### PERCENTAGE CONVERSION OF TRANSFORMED POINT ###
    x = round((transformed_point[0] / 9) * 100, 2)
    y = round((transformed_point[1] / 16) * 100, 2)

    ### FLIP PERCENTAGE FOR CAMERA 2 BECAUSE OF REVERSED P.0.V
    if camera_num == 2:
        x = 100 - x
        y = 100 - y

    x = str(x)
    y = str(y)

    # # globals.points_from_cameras[index] = transformed_point

    try:
        os.mkdir(f"./test_output_points/{directory}")
    except Exception:
        pass

    f = open(f"./test_output_points/{directory}/camera{camera_num}.txt", "w+")
    ### FLIP X AND Y TO ALIGN WITH P.0.V OF USER
    f.write(f"{y}, {x}")
    f.close()

if __name__ == "__main__":
    ProcessImages()