import pyautogui
import time
import keyboard
names = {}
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
pyr_txt = [['/', 'space', '\\'],
           ['/', '(', '0', ')', '\\'],
           ['/', 'space', 'space', 'space', 'space', 'space', '\\'],
           ['/', '_', '_', '_', '_', '_', '_', '_', '\\']]
pyr_space = [3, 2, 1, 0]
bun_txt = [['(', '\\', '_', '_', '/', ')'],
           ['(', '.', 'space', 'space', '.', ')'],
           ['(', '"', ')', '[', 'A', 'F', 'K', '.', ']', '(', '"', ')']]
bun_space = [3, 3, 0]
fis_txt = [['~', '~', '~', '~', '~', '~'],
           ['<', '*', ')', ')', ')', '<'],
           ['~', '~', '~', '~', '~', '~']]
fis_space = [0, 1, 2]


def wait(sec):
    m = 0
    while m < sec:
        print(sec - m)
        time.sleep(1)
        m += 1


def run(name='it'):
    if name not in names:
        names[name] = 1
    elif name in names:
        names[name] += 1
    print(f"{name} run {names[name]}")


class symbol:
    def __init__(self, fr_space, words, ending=True, skip_line=50):
        self.fr_space = fr_space
        self.words = words
        self.ending = ending
        self.skip_line = skip_line

    def typ(self, obj=None):  # depends on API
        pyautogui.press('t')
        time.sleep(0.1)
        for num, item in zip(self.fr_space, self.words):
            symbol.row(self, num, item)
        pyautogui.press('enter')
        run(obj)
        wait(60)

    def row(self, space, txt, x=0, y=0, z=0):
        i = int(space)
        while i > x:
            pyautogui.press('space')
            x += 1
        for word in txt:
            pyautogui.press(word)
            y += 1
        if self.ending:
            n = self.skip_line - y - x
            while n > z:
                pyautogui.press('space')
                z += 1

    @staticmethod
    def blank():
        while True:
            pyautogui.press('t')
            wait(0.1)       
            pyautogui.press('enter')
            print('pressed')
            wait(60)

    @staticmethod
    def sym():
        pyr = symbol(pyr_space, pyr_txt)
        bun = symbol(bun_space, bun_txt)
        fis = symbol(fis_space, fis_txt)
        while True:
            pyr.typ('pyr')
            bun.typ('bun')
            fis.typ('fis')


wait(10)
# symbol.sym()
while not keyboard.is_pressed('ctrl'):
    wait(60)
    pyautogui.keyDown('tab')
    time.sleep(.1)
    pyautogui.keyUp('tab')
