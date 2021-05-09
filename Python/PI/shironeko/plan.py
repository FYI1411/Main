import pyautogui
import os
import cv2
import time
os.chdir('C:/Users/HT/Desktop/folder/python/PI/shironeko')
print(os.getcwd())
pyautogui.PAUSE = 0
pyautogui.alert(text='Running', title='Shironeko', button='OK')
dregion = (467, 33, 391, 696)


def check(pic, confidence=.9, region=dregion):
    return pyautogui.locateCenterOnScreen(cv2.imread(f'img/{pic}', 0), grayscale=True, confidence=confidence, region=region)


pyautogui.screenshot('view.png', region=dregion)
i = 0
burst, skill = True, False
x, y = pyautogui.center(dregion)
pyautogui.click(x, y)
while True:
    if check('loading.png') is not None:
        pass
    elif check('rquest.PNG') is not None:
        pyautogui.press('q')
    elif check('mkroom.PNG') is not None:
        pyautogui.press('z')
    elif check('w_ok.PNG') is not None:
        try:
            x1, y1 = check('w_ok.PNG')
            pyautogui.click(x1, y1)
        except Exception as e:
            print(e)
    elif check('ok.PNG', confidence=.8) is not None:
        try:
            x2, y2 = check('ok.PNG', confidence=.8)
            pyautogui.click(x2, y2)
        except Exception as e:
            print(e)
    elif check('check.PNG') is not None:
        pyautogui.press('x')
    elif check('s_ok.PNG') is not None:
        try:
            if check('redo.PNG') is not None:
                pyautogui.press('r')
            else:
                x, y = check('s_ok.PNG')
                pyautogui.click(x, y)
        except Exception as e:
            print(e)
    elif check('go.PNG') is not None:
        try:
            x, y = check('go.PNG')
            pyautogui.click(x, y)
        except Exception as e:
            print(e)
    elif check('battle.PNG') is not None:
        i += 1
        print(f"{i} battles")
        while True:
            if check('battle.PNG') is not None:
                x, y = pyautogui.center(dregion)
                if check('burst.png') is not None and burst:
                    pyautogui.moveTo(x, y)
                    pyautogui.keyDown('space')
                    time.sleep(1)
                    pyautogui.keyUp('space')
                elif check('mpbar.PNG') is not None and skill:
                    pyautogui.moveTo(x, y)
                    pyautogui.mouseDown()
                    time.sleep(.5)
                    pyautogui.moveTo(x=x+60, y=y-60)
                    pyautogui.mouseUp()
                else:
                    pyautogui.press('space')
            else:
                break
    else:
        pyautogui.press('space')
