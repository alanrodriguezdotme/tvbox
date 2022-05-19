import os
import RPi.GPIO as GPIO
import random
import time
from subprocess import PIPE, Popen, STDOUT

directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'videos')
videos = []
currentVideo = 0
playProcess = None
isPlaying = False

button1 = 31
button2 = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def getVideos():
    global videos
    videos = []
    for file in os.listdir(directory):
        if file.lower().endswith('.mp4'):
            videos.append(os.path.join(directory, file))


def stopVideo():
    global isPlaying
    global playProcess
    if isPlaying and (playProcess != None):
        print('Attempting to stop video...' + str(playProcess.pid))
        playProcess.terminate()
        playProcess = None
        isPlaying = False


def playVideos():
    global videos
    global isPlaying
    global playProcess

    if len(videos) == 0:
        getVideos()
        time.sleep(5)
        random.shuffle(videos)
        return

    print('Playing video...')
    print(currentVideo)
    playProcess = Popen(['omxplayer', '--no-osd', '--aspect-mode', 'fill', videos[currentVideo]])
    isPlaying = True
    playProcess.wait()

def changeVideo(value):
    global videos
    global currentVideo
    global isPlaying
    global playProcess
    print('Changing video...' + str(value))

    stopVideo()

    if currentVideo >= len(videos) - 1:
        currentVideo = 0
    elif currentVideo == 0:
        currentVideo = 0
    else:
        currentVideo += value
    playVideos()


while (True):
    input1 = GPIO.input(button1)
    input2 = GPIO.input(button2)

    if input1 == False:
        changeVideo(-1)
    if input2 == False:
        changeVideo(1)

    playVideos()
