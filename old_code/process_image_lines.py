import cv2
import numpy as np
import math

##### HoughLines #####

src_img = cv2.imread('./images/640x480_30seconds_100quality/200.jpg')

cv2.imshow('Original Image',src_img)

grayscale = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Grayscale', grayscale)

edges = cv2.Canny(grayscale, 100, 100)

lines = cv2.HoughLines(edges, 0.7, np.pi / 180, 150, None, 0, 0)

for i in range(0, len(lines)):
            rho_l = lines[i][0][0]
            theta_l = lines[i][0][1]
            a_l = math.cos(theta_l)
            b_l = math.sin(theta_l)
            x0_l = a_l * rho_l
            y0_l = b_l * rho_l
            pt1_l = (int(x0_l + 1000*(-b_l)), int(y0_l + 1000*(a_l)))
            pt2_l = (int(x0_l - 1000*(-b_l)), int(y0_l - 1000*(a_l)))
            cv2.line(src_img, pt1_l, pt2_l, (0,0,255), 1, cv2.LINE_AA)

cv2.imshow("Image with lines", src_img)
cv2.waitKey(0)
