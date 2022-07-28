from ffmpy import FFmpeg
import os

def FFmpegImageCapture(name, ip):

    print("Thread: {} is starting".format(name))

    # ff = FFmpeg(
    #         inputs={'http://{}/video'.format(ip): ['-f', 'mjpeg']},
    #         outputs={'img.jpg': ['-vf', 'fps=60']}
    #     )

    # os.system(ff.cmd)

    while(True):
        pass