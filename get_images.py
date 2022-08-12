from ffmpy import FFmpeg
import os

def FFmpegImageCapture(name, ip):

    print("Thread: {} is starting".format(name))

    # ff = FFmpeg(
    #         inputs={'http://{}/video'.format(ip): ['-f', 'mjpeg', 'y']},
    #         # outputs={'img.jpg': []}
    #         outputs={'./images/testing_images/{}/img.jpg'.format(name): ['-y', '-vf', 'fps=60', '-update', '1']}
    #     )

    # os.system(ff.cmd)
    # print(ff.cmd)

    # updates the same image file but runs into LOTS of collisions/corrupted files
    # os.system(f"ffmpeg -y -f mjpeg -i http://{ip}/video -vf fps=5 -update 1 ./images/testing_images/{name}/img.jpg")

    dir = f'./images/testing_images/{name}/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    os.system(f"ffmpeg -f mjpeg -i http://{ip}:5000/video -vf fps=5 ./images/testing_images/{name}/img%003d.jpg")

    while(True):
        pass

if __name__ == "__main__":
    FFmpegImageCapture("camera1", "10.193.8.209:5000")