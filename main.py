# on mom's laptop without starting obs it takes ~31 seconds, with - ~37
import pyautogui
import os
import shutil
from time import sleep
from librosa import get_duration
import cv2

# function for finding coords for finding button
def findCoords(pathh):
    loc = None
    while loc == None:
        loc = pyautogui.locateOnScreen(pathh, grayscale=True, confidence=0.8)
        print("Not there yet!")
    point = pyautogui.center(loc)
    return point

done = 0
interval = ""
while done == 0:
    interval = input("Do you want a set interval? (y/n): ")
    interval = interval.lower()
    if interval == "y" or interval == "n":
        done = 1
    else:
        print("That's not y/n!")

done = 0
customInterv = 0
while done == 0:
    if interval == "y":
        try:
            customInterv = int(input("Enter the interval: "))
        except ValueError:
            print("That's not a number!")
        finally:
            done = 1

# getting le' paths
scriptPath = os.path.dirname(os.path.abspath(__file__))
with open(scriptPath + "\\obspath.txt", 'r') as file:
    obsPath = file.read()
audioPath = scriptPath + "\\audio.wav"
cmdLocatePath = 'cmd.png'
sceneLocatePath = 'scene.png'
startLocatePath = 'start.png'
textLocatePath = 'text.png'
writingLocatePath = 'write.png'
obsLocatePath = 'obs.png'
denyLocatePath = 'deny.png'
profileLocatePath = 'profile.png'

# deleting everything in the frames folder
folder = scriptPath + '\\frames'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# opening le' files
textFile = open(scriptPath + "\\text.txt", 'r')

# getting the text
text = textFile.read()

# getting audio duration
duration = 0
try:
    duration = get_duration(filename=audioPath)
except FileNotFoundError:
    print("No audio file detected. Exiting the program.")
    exit()
duration = round(duration, 1) # rounding

# checking if obs is open
obsActive = False
for i in pyautogui.getAllTitles():
    if 'OBS' in i:
        obsActive = True
        print("obs is active")

if obsActive == False:
    # opening obs
    pyautogui.hotkey('win', 'r') # open cmd
    pyautogui.write('cmd')
    pyautogui.hotkey('enter')
    sleep(1)
    if "строка" not in pyautogui.getActiveWindowTitle():
        cmdPoint = findCoords(cmdLocatePath)
        pyautogui.click(cmdPoint.x, cmdPoint.y)
    pyautogui.write(obsPath) # writing the path
    pyautogui.hotkey('enter')
    sleep(8)
    os.system("taskkill /f /im cmd.exe") # killing the cmd process
elif obsActive == True:
    obsPoint = findCoords(obsLocatePath)
    pyautogui.click(obsPoint.x, obsPoint.y)
else:
    print("???")
    exit()

# waiting until obs opens
if obsActive == False:
    check = 0
    while check == 0:
        for i in pyautogui.getAllTitles():
            print(i)
            if "OBS" in i:
                check = 1
                break
        sleep(0.5)


# checking if obs is active and if it's not - active
if "OBS" not in pyautogui.getActiveWindowTitle():
    obsPoint = findCoords(obsLocatePath)
    pyautogui.click(obsPoint.x, obsPoint.y)

# setting the scene
pyautogui.hotkey('alt', 's')
scenePoint = findCoords(sceneLocatePath)
pyautogui.click(scenePoint.x, scenePoint.y)

# setting the profile
pyautogui.hotkey('alt', 'p')
profilePoint = findCoords(profileLocatePath)
pyautogui.click(profilePoint.x, profilePoint.y)

# starting the recording
recPoint = findCoords(startLocatePath)
pyautogui.click(recPoint.x, recPoint.y)

# doubleclicking the text shitter in obs
textPoint = findCoords(textLocatePath)
pyautogui.doubleClick(textPoint.x, textPoint.y)

# setting the text
writePoint = findCoords(writingLocatePath)
pyautogui.click(writePoint.x+50, writePoint.y)
sleep(0.1)
pyautogui.hotkey('ctrl', 'a')
if interval == "n": # deciding the interval and stuff
    interv = customInterv
else:
    interv = duration / len(text)
pyautogui.typewrite(text, interval=interv)

# closing the text editing box
denyPoint = findCoords(denyLocatePath)
pyautogui.click(denyPoint.x, denyPoint.y)
# stopping the recording
pyautogui.click(recPoint.x, recPoint.y)

# closing the text file omegalul
textFile.close()

# getting all frames from the video (useful in editing PogChamp)
sleep(1)
video = cv2.VideoCapture('video.mp4')
success,image = video.read()
count = 0
while success:
    cv2.imwrite("frames\\frame%d.jpg" % count, image)     # save frame as JPEG file
    success,image = video.read()
    print('Read a new frame: ', success)
    count += 1