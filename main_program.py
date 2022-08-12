import threading
import time
import ctypes
import get_images as gi
import process_image_line_detection as pi
import globals
import move_mouse

try:
    #make variable for user32
    user32 = ctypes.windll.user32

    globals.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print(globals.screensize)
    # real aspect ratio! changed because my laptop is 3:2 not standard tv 16:9
    globals.aspect_ratio = move_mouse.calculate_aspect(globals.screensize[0], globals.screensize[1])
    # aspect_ratio = (16,9)
    print(f"Screen aspect ratio: {globals.aspect_ratio}")


    # left side of tv relative to user
    camera1_thread = threading.Thread(target=gi.FFmpegImageCapture, args=("camera1", "10.193.1.206"), daemon=True)
    camera1_thread.start()

    # right side of tv relative to user
    camera2_thread = threading.Thread(target=gi.FFmpegImageCapture, args=("camera2", "10.193.8.173"), daemon=True)
    camera2_thread.start()

    time.sleep(2)

    image1_thread = threading.Thread(target=pi.ProcessImages, args=(3, 1), daemon=True)
    image1_thread.start()

    image1_thread = threading.Thread(target=pi.ProcessImages, args=(4, 2), daemon=True)
    image1_thread.start()

    move_mouse_thread = threading.Thread(target=move_mouse.MoveMouse, daemon=True)
    move_mouse_thread.start()

except:
    print("Error: unable to start thread", flush=True)

while 1:
    print("Thread count: {}".format(threading.active_count()), flush=True)
    print("Point on screen from camera1: {}".format(globals.points_from_cameras[0]), flush=True)
    print("Point on screen from camera2: {}".format(globals.points_from_cameras[1]), flush=True)
    time.sleep(1)