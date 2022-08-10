import pyautogui
import ctypes
import globals
import time

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
    #make variable for user32
    user32 = ctypes.windll.user32

    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print(screensize)
    # real aspect ratio! changed because my laptop is 3:2 not standard tv 16:9
    # aspect_ratio = calculate_aspect(screensize[0], screensize[1])
    aspect_ratio = (16,9)
    print(f"Screen aspect ratio: {aspect_ratio}")

    while(True):
        getX1 = globals.points_from_cameras[0][0] / aspect_ratio[0]
        getY1 = globals.points_from_cameras[0][1] / aspect_ratio[1]

        getX2 = globals.points_from_cameras[1][0] / aspect_ratio[0]
        getY2 = globals.points_from_cameras[1][1] / aspect_ratio[1]

        #calculate the x and y position depending on pixels
        xPositionCursor1 = getX1 * screensize[0]
        yPositionCursor1 = getY1 * screensize[1]

        xPositionCursor2 = getX2 * screensize[0]
        yPositionCursor2 = getY2 * screensize[1]

        #typecast to int 
        xPositionCursor1 = int(xPositionCursor1)
        yPositionCursor1 = int(yPositionCursor1)

        xPositionCursor2 = int(xPositionCursor2)
        yPositionCursor2 = int(yPositionCursor2)

        # pyautogui.moveTo((xPositionCursor1 + xPositionCursor2)/2, (yPositionCursor1 + yPositionCursor2)/2)

        #set the mouse cursor to that point if within threshold distance from each other
        if (abs(xPositionCursor1 - xPositionCursor2) < 0.1*screensize[0] and abs(yPositionCursor1 - yPositionCursor2) < 0.1*screensize[1]):
            # ctypes.windll.user32.SetCursorPos((xPositionCursor1 + xPositionCursor2)/2, (yPositionCursor1 + yPositionCursor2)/2)
            pointX = (xPositionCursor1 + xPositionCursor2)/2
            pointY = (yPositionCursor1 + yPositionCursor2)/2
            pyautogui.moveTo(pointX, pointY)
            print(f"Moved mouse to ({pointX}, {pointY})")
        
        time.sleep(1)