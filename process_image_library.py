import cv2
import numpy as np
import math
from skimage.transform import ProjectiveTransform
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import globals

def RedMaskAndBinary(image):
    ### TARGET RED BORDER OF TV ####
    image_copy = image.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([5, 255, 255])
    
    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160,100,20])
    upper2 = np.array([179,255,255])
    
    lower_mask = cv2.inRange(image, lower1, upper1)
    upper_mask = cv2.inRange(image, lower2, upper2)
    
    full_mask = lower_mask + upper_mask
    
    # Apply mask to image copy to get rid of anything not red
    only_red = cv2.bitwise_and(image_copy, image_copy, mask=full_mask)

    # Grayscale to make line/dot detection easier
    only_red_grayscale = cv2.cvtColor(only_red, cv2.COLOR_BGR2GRAY)

    # Convert grayscale to binary black/white
    only_red_binary = cv2.threshold(only_red_grayscale, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    return only_red_binary


def GetLargestContour(image):
    ## DETECT CONTOURS
    contours, hierarchy= cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    ## FIND LARGEST CONTOUR (SHOULD BE TV OUTLINE)
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse=True)
    largest_contour = sorted_contours[0]
    return largest_contour

def ScaleContour(cnt, scale):
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    cnt_norm = cnt - [cx, cy]
    cnt_scaled = cnt_norm * scale
    cnt_scaled = cnt_scaled + [cx, cy*0.99]
    cnt_scaled = cnt_scaled.astype(np.int32)

    return cnt_scaled


def DotDetector(image):

    blur = cv2.GaussianBlur(image,(9,9), cv2.BORDER_DEFAULT)
    # cv2.imshow("Blur", blur)

    # retval, threshold = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Create detector with parameters for white dots
    params = cv2.SimpleBlobDetector_Params()

    params.filterByColor = True
    params.blobColor = 255

    # # Filter by Area.
    params.filterByArea = True
    params.minArea = 60
    params.maxArea = 10000

    # # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.7

    # # # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0

    # # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0

    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(blur)

    blobs = cv2.drawKeypoints(blur, keypoints, image, (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # cv2.imshow("Blobs Using Area", blobs)

    return keypoints


def GetPointsInsideContour(keypoints, contour):
    # print("keypoints: ", keypoints)
    points_on_screen = []
    for point in keypoints:
        coords = (round(point.pt[0]), round(point.pt[1]))
        if cv2.pointPolygonTest(contour, coords, False) == 1:
            points_on_screen.append(coords)

    return points_on_screen


def GetCornersOfContour(contour):
    peri = cv2.arcLength(contour, True)
    # Approximate contour as quadrilateral
    # For some reason this function double nests the points like [[[0,0]], [[1,1]]] when we want [[0,0], [1,1]]
    # Gets corners starting in bottom left and going counter-clockwise
    corners = cv2.approxPolyDP(contour, 0.01 * peri, True)
    # cv2.polylines(image_copy, [corners], True, (0,0,255), 1, cv2.LINE_AA)

    condensed_array = []
    for corner in corners:
        condensed_array.append(corner[0])
    
    condensed_array = np.array(condensed_array)
    return condensed_array

#### PROJECTIVE TRANSFORM FROM TRAPEZOID TO RECTANGLE WITH LINE INTERSECTIONS ####
def TransformToRectangle(intersections, points_on_screen):
    t = ProjectiveTransform()
    #                [bottom_left, top_left, top_right, bottom_right])
    src = np.asarray([intersections[1][0], intersections[0][0], intersections[2][0], intersections[3][0]])
    # print(src)
    # print(intersections)
    ## standard 16:9 tv aspect ratio mapping (flipped horizontal because of image pov)
    # dst = np.asarray([[0, 0], [0, 16], [9, 16], [9, 0]])

    # print("points on screen: ", points_on_screen)
    #real aspect ratio of monitor
    temp = [0, globals.aspect_ratio[0]]
    # print(temp)
    dst = np.asarray([[0, 0], [0, globals.aspect_ratio[0]], [globals.aspect_ratio[1], globals.aspect_ratio[0]], [globals.aspect_ratio[1], 0]])
    
    if not t.estimate(src, dst): raise Exception("estimate failed")

    data = np.asarray(points_on_screen)
    data_local = t(data)

    ### UNCOMMENT TO SHOW ORIGINAL POINTS AND TRANSFORMED POINTS COMPARISON
    # ShowTransform(src, dst, data, data_local)

    # plt.figure()
    # plt.plot(src[[0,1,2,3,0], 0], src[[0,1,2,3,0], 1], '-')
    # plt.plot(data.T[0], data.T[1], 'o')
    # plt.gca().invert_yaxis()
    # plt.margins(0)
    # plt.figure()
    # plt.plot(dst.T[0], dst.T[1], '-')
    # plt.plot(data_local.T[0], data_local.T[1], 'o')
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.margins(0)
    # plt.show()

    return data_local

#### PROJECTIVE TRANSFORM FROM TRAPEZOID TO RECTANGLE WITH CORNERS OF CONTOUR #####
def TransformToRectangle_Contour(tv_corners, points_on_screen):
    t = ProjectiveTransform()
    
    #                [bottom_left, top_left, top_right, bottom_right])
    src = np.asarray([tv_corners[0], tv_corners[3], tv_corners[2], tv_corners[1]])

    ## standard 16:9 tv aspect ratio mapping (flipped horizontal because of image pov)
    dst = np.asarray([[0, 0], [0, 16], [9, 16], [9, 0]])

    if not t.estimate(src, dst): raise Exception("estimate failed")

    data = np.asarray(points_on_screen)
    data_local = t(data)

    ### UNCOMMENT TO SHOW ORIGINAL POINTS AND TRANSFORMED POINTS COMPARISON
    # ShowTransform(src, dst, data, data_local)

    return data_local

def ShowTransform(src, dst, data, data_local):
    plt.figure()
    plt.plot(src[[0,1,2,3,0], 0], src[[0,1,2,3,0], 1], '-')
    plt.plot(data.T[0], data.T[1], 'o')
    plt.gca().invert_yaxis()
    plt.margins(0)
    plt.figure()
    plt.plot(dst.T[0], dst.T[1], '-')
    plt.plot(data_local.T[0], data_local.T[1], 'o')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.margins(0)
    plt.show()


def VisualizeContourCorners(corners, image):
    num = 1
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 1
    fontColor              = (255,0,0)
    thickness              = 3
    lineType               = 2
    for corner in corners:
        cv2.putText(image, str(num), 
            (corner[0], corner[1]), 
            font, 
            fontScale,
            fontColor,
            thickness,
            lineType)    
        num += 1
        image = cv2.circle(image, (corner[0], corner[1]), radius=1, color=(0, 255, 0), thickness=-1)
    # cv2.imshow('Corners', image)

def VisualizePointsOnScreen(points_on_screen, image):
    for point in points_on_screen:
        image = cv2.circle(image, (point[0], point[1]), radius=5, color=(255, 0, 0), thickness=-1)
    # cv2.imshow("Points on screen", image)


def VisualizeConvexHull(hull, image):
    cv2.drawContours(image, [hull], 0, (255,0,0), 3)
    cv2.imshow("Convex Hull", image)

def intersection(line1, line2):
    """Finds the intersection of two lines given in Hesse normal form.

    Returns closest integer pixel locations.
    See https://stackoverflow.com/a/383527/5087436
    """

    rho1, theta1 = line1[0]
    rho2, theta2 = line2[0]
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return [[x0, y0]]

def segmented_intersections(lines):
    """Finds the intersections between groups of lines."""

    intersections = []
    for k, x in enumerate(lines):
        for y in lines[k+1:]:
            intersections.append(intersection(x, y))

    return intersections

def GetAverageLines(image):
    ### GET LINES FROM IMAGE ###
    edges = cv2.Canny(image, 100, 100)
    # lines = cv2.HoughLines(edges, 1.5, np.pi / 180, 150, None, 0, 0)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 50, None, 0, 0)

    #### Categorize lines by sides ####
    lineCollections = CategorizeLines(lines)

    #### GET AVERAGE LINE ON ALL FOUR SIDES ####
    final_four_lines = []
    for lineCollection in lineCollections:
        final_four_lines.append(np.mean(lineCollection, axis=0))
    
    return final_four_lines

def CategorizeLines(lines):
    #### Categorize lines by sides ####
    left_lines = []
    right_lines = []
    top_lines = []
    bottom_lines = []

    for line in lines:
        rho_l, theta_l = line[0]

        if (0 <= theta_l <= 1):
            left_lines.append(line)
        elif (2 <= theta_l <= 3):
            right_lines.append(line)
        elif (rho_l > 300):
            bottom_lines.append(line)
        elif (rho_l < 100):
            top_lines.append(line)

    #### Put line lists into a single array to make the following for loop easier ####
    lineCollections = []
    lineCollections.append(left_lines)
    lineCollections.append(right_lines)
    lineCollections.append(top_lines)
    lineCollections.append(bottom_lines)

    return lineCollections

def GetIntersections(lines):
    #### CALCULATE INTERSECTIONS OF LINES #####
    intersections = segmented_intersections(lines)

    #### REMOVE INTERSECTION POINTS THAT DON'T MATTER
    largest_x_point = intersections[0]
    largest_x_index = 0
    smallest_y_point = intersections[0]
    smallest_y_index = 0
    for k, point in enumerate(intersections):
        if (abs(point[0][0]) > abs(largest_x_point[0][0])):
            largest_x_point = point
            largest_x_index = k
        if (point[0][1] < 0):
            smallest_y_point = point
            smallest_y_index = k
        # elif (abs(point[0][1]) < abs(smallest_y_point[0][1])):
        #     smallest_y_point = point
        #     smallest_y_index = k

    intersections.pop(largest_x_index)
    intersections.pop(smallest_y_index)

    return intersections

def DrawOnCanvas(intersections, lines):
    #### BLANK CANVAS TO DRAW RESULTS ON ####
    canvas =  np.zeros((480, 720, 3), dtype=np.uint8)

    #### DRAW INTERSECTION POINTS ONTO CANVAS
    # for point in intersections:
    #     cv2.circle(canvas, point[0], radius=10, color=(0, 0, 255), thickness=-1)

    #### DRAW LINES BETWEEN INTERSECTION POINTS #####
    simplified_intersections = [intersections[0][0], intersections[2][0], intersections[3][0], intersections[1][0]]
    simplified_intersections = np.array(simplified_intersections)
    cv2.drawContours(canvas, [simplified_intersections], 0, (255,255,255), 2)

    #### DRAW LINES ON BLACK CANVAS ####
    # for line in lines:
    #     rho_l, theta_l = line[0]
    #     a_l = math.cos(theta_l)
    #     b_l = math.sin(theta_l)
    #     x0_l = a_l * rho_l
    #     y0_l = b_l * rho_l
    #     pt1_l = (int(x0_l + 1000*(-b_l)), int(y0_l + 1000*(a_l)))
    #     pt2_l = (int(x0_l - 1000*(-b_l)), int(y0_l - 1000*(a_l)))
    #     cv2.line(canvas, pt1_l, pt2_l, (255,255,255), 1, cv2.LINE_AA)

    canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    return canvas
