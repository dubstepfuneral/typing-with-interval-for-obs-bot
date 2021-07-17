import pyautogui
import os
import shutil
from time import sleep
from librosa import get_duration

# function for finding coords for finding button
def findCoords(pathh):
    loc = None
    while loc == None:
        loc = pyautogui.locateOnScreen(pathh, grayscale=True, confidence=0.8)
        print("Not there yet!")
    point = pyautogui.center(loc)
    return point

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

# setting the scene
pyautogui.hotkey('alt', 's')
scenePoint = findCoords(sceneLocatePath)
pyautogui.click(scenePoint.x, scenePoint.y)
sleep(1)

# setting the profile
pyautogui.hotkey('alt', 'p')
profilePoint = findCoords(profileLocatePath)
pyautogui.click(profilePoint.x, profilePoint.y)

# starting the recording
pyautogui.click(1261, 597)

# doubleclicking the text shitter in obs
pyautogui.doubleClick(277, 570)

# setting the text
pyautogui.click(479+50, 506)
sleep(0.1)
pyautogui.hotkey('ctrl', 'a')
interv = len(text) / len(text)
pyautogui.typewrite(text, interval=interv)
sleep(interv)

# closing the text editing box
pyautogui.click(990, 644)
# stopping the recording
sleep(0.1)
pyautogui.click(1261, 597)

# closing the text file omegalul
textFile.close()