import requests
import time

i = 0
endTime = time.time() + 30

while (time.time() < endTime):
    # recieve = requests.get("http://10.193.1.119:5002/shot.jpg")
    recieve = requests.get("http://10.193.1.119:5002/video")

    file = "C:\\Users\\Karl\\Desktop\\TouchscreenTV\\images\\{num}.mp3".format(num = i)

    with open(file,'wb') as f:
        f.write(recieve.content)
    
    i += 1



# Capture frames from multipart video stream (much higher fps!)
# ffmpeg -f mjpeg -i http://10.193.1.119:5002/video -vf fps=60 img%03d.jpg