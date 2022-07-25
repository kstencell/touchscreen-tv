from ffmpy import FFmpeg
import os

ff = FFmpeg(
        inputs={'http://10.193.1.119:5002/video': ['-f', 'mjpeg']},
        outputs={'img.jpg': ['-vf', 'fps=60']}
    )

os.system(ff.cmd)