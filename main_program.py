import threading
import time
import get_images as gi
import process_image_line_detection as pi
import globals
import move_mouse

try:
    camera1_thread = threading.Thread(target=gi.FFmpegImageCapture, args=("Camera1", "10.193.1.119"), daemon=True)
    camera1_thread.start()

    camera2_thread = threading.Thread(target=gi.FFmpegImageCapture, args=("Camera2", "10.193.1.120"), daemon=True)
    camera2_thread.start()
    time.sleep(2)

    image1_thread = threading.Thread(target=pi.ProcessImages, args=(3,0), daemon=True)
    image1_thread.start()

    image1_thread = threading.Thread(target=pi.ProcessImages, args=(4,1), daemon=True)
    image1_thread.start()

    move_mouse_thread = threading.Thread(target=move_mouse.MoveMouse, daemon=True)
    move_mouse_thread.start()

except:
    print("Error: unable to start thread", flush=True)

while 1:
    print("Thread count: {}".format(threading.active_count()), flush=True)
    print("Point on screen from camera1: {}".format(globals.points_from_cameras[0]), flush=True)
    print("Point on screen from camera2: {}".format(globals.points_from_cameras[1]), flush=True)
    time.sleep(5)