import pyautogui
import time
import numpy as np
import win32api
import win32con
import keyboard
import random
pyautogui.FAILSAFE = False


def wait(timer):
    m = 0
    while m < timer:
        print(timer - m)
        time.sleep(1)
        m += 1


def left_click(timer=0.1, rand_sleep=False):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(timer) if not rand_sleep else time.sleep(np.random.uniform(timer, timer*3))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def nade(nade_key, timer=0.1):
    pyautogui.keyDown(nade_key)
    time.sleep(timer)
    pyautogui.keyUp(nade_key)


def press(key, timer=0.1, rand_sleep=False):
    pyautogui.keyDown(key)
    time.sleep(timer) if not rand_sleep else time.sleep(np.random.uniform(timer, timer*3))
    pyautogui.keyUp(key)


def click_img(img):
    target = pyautogui.locateOnScreen(img, confidence=0.9)
    if target:
        pyautogui.click(target)


def holds(*keys, timer=0.1, rand_sleep=False):
    for key in keys:
        pyautogui.keyDown(key)
    time.sleep(timer) if not rand_sleep else time.sleep(np.random.uniform(timer, timer*3))
    for key in keys:
        pyautogui.keyUp(key)

while True:
    choice = input('> ')
    if choice == 's':
        wait(3)
        while not keyboard.is_pressed('q'):
            click_img(r"C:\Users\HT\Desktop\folder\Python\PI\BM\img\ok.jpg")
            left_click(rand_sleep=True)
            press(random.choice(['a', 'w', 's', 'd', 'space']), rand_sleep=True)
    elif choice == 'q':
        break
