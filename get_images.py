from ffmpy import FFmpeg
import os
import time

def FFmpegImageCapture(name, ip):

    print("Thread: {} is starting".format(name))

    dir = f'./images/testing_images/{name}/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    os.system(f"ffmpeg -f mjpeg -i http://{ip}:5000/video -vf fps=30 ./images/testing_images/{name}/img%003d.jpg")

    while(True):
        time.sleep(60000)
        pass


if __name__ == "__main__":
    FFmpegImageCapture("camera1", "10.193.8.209:5000")