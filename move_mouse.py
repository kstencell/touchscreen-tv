import pyautogui
import ctypes
import globals
import time
import math

def calculate_aspect(width: int, height: int) -> str:
    temp = 0

    def gcd(a, b):
        """The GCD (greatest common divisor) is the highest number that evenly divides both width and height."""
        return a if b == 0 else gcd(b, a % b)

    if width == height:
        return "1:1"

    if width < height:
        temp = width
        width = height
        height = temp

    divisor = gcd(width, height)

    x = int(width / divisor) if not temp else int(height / divisor)
    y = int(height / divisor) if not temp else int(width / divisor)

    return [x, y]

pyautogui.PAUSE = 0

def MoveMouse():

    pyautogui.FAILSAFE = False
    recentlyClicked = False

    while(True):

        #calculate the x and y position depending on pixels
        xPositionCursor1 = globals.points_from_cameras[0][0] * globals.screensize[0] /100
        yPositionCursor1 = globals.points_from_cameras[0][1] * globals.screensize[1] /100

        xPositionCursor2 = globals.points_from_cameras[1][0] * globals.screensize[0] /100
        yPositionCursor2 = globals.points_from_cameras[1][1] * globals.screensize[1] /100

        #typecast to int 
        xPositionCursor1 = int(xPositionCursor1)
        yPositionCursor1 = int(yPositionCursor1)

        xPositionCursor2 = int(xPositionCursor2)
        yPositionCursor2 = int(yPositionCursor2)

        pointX = (xPositionCursor1 + xPositionCursor2)/2
        pointY = (yPositionCursor1 + yPositionCursor2)/2

        # print(f"Mouse Thread sees: {globals.points_from_cameras}")

        # if ((abs(pointX - pyautogui.position()[0]) > 0.1*globals.screensize[0]) or (abs(pointY - pyautogui.position()[1]) > 0.1*globals.screensize[1])):
        #     continue
        if (globals.points_from_cameras[0][0] != 0 and globals.points_from_cameras[0][1] != 0 and globals.points_from_cameras[1][0] != 0 and globals.points_from_cameras[1][1] != 0):
            pyautogui.moveTo(pointX, pointY, 0.1, pyautogui.easeOutQuad)
            print(f"Moved mouse to ({pointX}, {pointY})", flush=True)
            print(f"Recently Clicked: {recentlyClicked}")
            #### CLICKING functionality ####
            if (abs(xPositionCursor1 - xPositionCursor2) < 0.02*globals.screensize[0] and abs(yPositionCursor1 - yPositionCursor2) < 0.02*globals.screensize[1] and recentlyClicked == False):
                pyautogui.click()
                recentlyClicked = True
                print("Mouse click")
            if (abs(xPositionCursor1 - xPositionCursor2) > 0.02*globals.screensize[0] and abs(yPositionCursor1 - yPositionCursor2) > 0.2*globals.screensize[1] and recentlyClicked == True):
                recentlyClicked = False
        elif (globals.points_from_cameras[0][0] == 0 and globals.points_from_cameras[0][1] == 0 and globals.points_from_cameras[1][0] != 0 and globals.points_from_cameras[1][1] != 0):
            pyautogui.moveTo(xPositionCursor2, yPositionCursor2, 0.2, pyautogui.easeOutQuad)
            print(f"Moved mouse to ({xPositionCursor2}, {yPositionCursor2})", flush=True)
        elif (globals.points_from_cameras[1][0] == 0 and globals.points_from_cameras[1][1] == 0 and globals.points_from_cameras[0][0] != 0 and globals.points_from_cameras[0][1] != 0):
            pyautogui.moveTo(xPositionCursor1, yPositionCursor1, 0.2, pyautogui.easeOutQuad)
            print(f"Moved mouse to ({xPositionCursor1}, {yPositionCursor1})", flush=True)


        time.sleep(0.05)
            

        
    