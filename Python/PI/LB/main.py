import pyautogui
import os
import cv2
import time
import keyboard
base_conf = .95


def check(pic, confidence=base_conf):
    return pyautogui.locateCenterOnScreen(cv2.imread(f'img/{pic}', 0), grayscale=True, confidence=confidence)


def check_all(pic, confidence=base_conf):
    result = list(pyautogui.locateAllOnScreen(cv2.imread(f'img/{pic}', 0), grayscale=True, confidence=confidence))
    return None if not result else pyautogui.center(result[-1])


if __name__ == '__main__':
    os.chdir('C:/Users/HT/Desktop/folder/python/PI/LB')
    print(os.getcwd())
    pyautogui.PAUSE = 0
    pyautogui.FAILSAFE = False
    pyautogui.alert(text='Running', title='Last Bullet', button='OK')
    img_files = ['play.jpg', 'redo.jpg', 'ok2.jpg', 'skip.jpg', 'start1.jpg', 'start2.jpg', 'leave.jpg', 'replay.jpg']
    check_all_img = []
    print(img_files)
    try:
        while True:
            while not keyboard.is_pressed('q'):
                img_list = set([check(img) if img not in check_all_img else check_all(img) for img in img_files])
                for img in img_list:
                    if img is not None:
                        x, y = img
                        print(x, y)
                        pyautogui.click(x, y)
                        time.sleep(.5)
                        break
                    else:
                        print('not found.')
                time.sleep(.5)
            pyautogui.prompt('stop?')
    except Exception as e:
        print(e)
    i = input()
