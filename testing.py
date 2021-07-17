import pyautogui
from time import sleep

check = 0
while check == 0:
    for i in pyautogui.getAllTitles():
        print(i)
        if "OBS" in i:
            check = 1
            break
    sleep(0.5)