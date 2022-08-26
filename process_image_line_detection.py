import cv2
import time
from process_image_library import *
import globals
import glob
import os
import traceback

def ProcessImages(thread_num=0, camera_num="null"):

    while(True):
        time.sleep(0.01)
        try:

            # find most recent file
            list_of_files = glob.glob(f'./images/testing_images/camera{camera_num}/*.jpg')
            sorted_files = sorted(list_of_files, key=os.path.getctime)
            latest_file = sorted_files[-2]

            # Load image
            image = cv2.imread(latest_file)
            image_copy = image.copy()

            # cv2.imshow("Original: thread {}".format(thread_num), image)

            ### DELETE EVERYTHING THAT'S NOT RED IN ORIGINAL IMAGE AND CONVERT TO BLACK/WHITE
            only_red_binary = RedMaskAndBinary(image_copy)
            # cv2.imshow("Only Red Binary", only_red_binary)

            #### GET AVERAGE LINE ON ALL FOUR SIDES ####
            lines = GetAverageLines(only_red_binary)

            #### CALCULATE INTERSECTIONS OF LINES #####
            intersections = GetIntersections(lines)

            #### SHOW WHAT COMPUTER SEES ####
            canvas = DrawOnCanvas(intersections, lines)
            # cv2.imshow("Computer Vision", canvas)

            ### FIND LARGEST CONTOUR (SHOULD BE TV OUTLINE) USED FOR DETERMINING IF DOTS ARE ON SCREEN OR OFF SCREEN
            contour = GetLargestContour(canvas)
            scaled_contour = ScaleContour(contour, 0.95)

            ### APPROXIMATE CONVEX HULL FROM BROKEN QUADRILATERAL CONTOUR
            # hull = cv2.convexHull(contour)

            ### DETECT ALL WHITE DOTS IN IMAGE
            all_dots = DotDetector(only_red_binary)

            ### GET ONLY POINTS THAT ARE INSIDE SCREEN CONTOUR (CENTER OF DOTS SPECIFICALLY)
            points_on_screen = GetPointsInsideContour(all_dots, scaled_contour)

            if (len(points_on_screen) != 1):
                globals.points_from_cameras[camera_num-1][0] = 0
                globals.points_from_cameras[camera_num-1][1] = 0
                # print(f"Thread {thread_num} did not detect only one blob {latest_file}", flush=True)
                continue

            VisualizePointsOnScreen(points_on_screen, image.copy())

            ### TRANSFORM QUADRILATERAL PLANE TO RECTANGLE (TV) AND USE TRANSFORM ON POINTS
            transformed_point = TransformToRectangle(intersections, points_on_screen)[0]

            ### PERCENTAGE CONVERSION OF TRANSFORMED POINT ###

            x = round((transformed_point[0] / globals.aspect_ratio[1]) * 100, 2)
            y = round((transformed_point[1] / globals.aspect_ratio[0]) * 100, 2)

            ### FLIP PERCENTAGE FOR CAMERA 2 BECAUSE OF REVERSED P.0.V
            if camera_num == 1:
                x = 100 - x
                y = 100 - y

            # print(f'Camera{camera_num} coordinates: {y}, {x}\n')

            globals.points_from_cameras[camera_num-1][0] = y
            globals.points_from_cameras[camera_num-1][1] = x

            # print(f'Global variable coordinates: {globals.points_from_cameras[camera_num][0]}, {globals.points_from_cameras[camera_num][1]}\n')

            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # print(f"Thread {thread_num} processed an image", flush=True)
        except Exception:
            # traceback.print_exc()
            pass
            # print("error")

def ProcessTestImages(thread_num=0, index=0, directory="null", camera_num="null"):

    # Load image
    # image = cv2.imread('200_test_with_arm_and_pointer.jpg')
    # image = cv2.imread(f'./images/{directory}/camera{camera_num}.jpg')
    image = cv2.imread(f'./images/{directory}.jpg')
    cv2.imshow("Original", image)

    # image = cv2.imread('./images/testing_images/{}/img.jpg'.format(name))
    # image = cv2.imread(latest_file)
    image_copy = image.copy()

    ### DELETE EVERYTHING THAT'S NOT RED IN ORIGINAL IMAGE AND CONVERT TO BLACK/WHITE
    only_red_binary = RedMaskAndBinary(image_copy)
    cv2.imshow("Only Red Binary", only_red_binary)

    #### GET AVERAGE LINE ON ALL FOUR SIDES ####
    lines = GetAverageLines(only_red_binary)

    #### CALCULATE INTERSECTIONS OF LINES #####
    intersections = GetIntersections(lines)
    # print("Intersections: ", intersections)

    #### SHOW WHAT COMPUTER SEES ####
    canvas = DrawOnCanvas(intersections, lines)
    cv2.imshow("Computer Vision", canvas)

    ### FIND LARGEST CONTOUR (SHOULD BE TV OUTLINE) USED FOR DETERMINING IF DOTS ARE ON SCREEN OR OFF SCREEN
    contour = GetLargestContour(canvas)
    scaled_contour = ScaleContour(contour, 0.95)
    contour_image = cv2.drawContours(image, [scaled_contour], -1, (255, 0, 0), 2)
    cv2.imshow("Contour", contour_image)

    ### APPROXIMATE CONVEX HULL FROM BROKEN QUADRILATERAL CONTOUR
    # points = np.array([intersections[0][0], intersections[1][0], intersections[2][0], intersections[3][0]])
    # print(points)

    ### DETECT ALL WHITE DOTS IN IMAGE
    all_dots = DotDetector(only_red_binary)

    ### GET ONLY POINTS THAT ARE INSIDE SCREEN CONTOUR (CENTER OF DOTS SPECIFICALLY)
    points_on_screen = GetPointsInsideContour(all_dots, scaled_contour)

    print(len(points_on_screen))

    VisualizePointsOnScreen(points_on_screen, canvas.copy())
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    ### TRANSFORM QUADRILATERAL PLANE TO RECTANGLE (TV) AND USE TRANSFORM ON POINTS
    transformed_point = TransformToRectangle(intersections, points_on_screen)[0]

    ### PERCENTAGE CONVERSION OF TRANSFORMED POINT ###
    x = round((transformed_point[0] / 9) * 100, 2)
    y = round((transformed_point[1] / 16) * 100, 2)

    ### FLIP PERCENTAGE FOR CAMERA 2 BECAUSE OF REVERSED P.0.V
    if camera_num == 2:
        x = 100 - x
        y = 100 - y

    # print(f'Camera{camera_num} coordinates: {y}, {x}\n')

    x = str(x)
    y = str(y)

    globals.points_from_cameras[camera_num-1][0] = y
    globals.points_from_cameras[camera_num-1][1] = x

    print("globals.points_from_cameras[camera_num-1][0]: ", globals.points_from_cameras[camera_num-1][0])
    print("globals.points_from_cameras[camera_num-1][1]: ", globals.points_from_cameras[camera_num-1][1])

    # try:
    #     os.mkdir(f"./test_output_points/{directory}")
    # except Exception:
    #     pass

    # f = open(f"./test_output_points/{directory}/camera{camera_num}.txt", "w+")
    ### FLIP X AND Y TO ALIGN WITH P.0.V OF USER
    # f.write(f"{y}, {x}")
    # f.close()

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    ProcessImages()