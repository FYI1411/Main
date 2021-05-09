import pyautogui
import threading
import concurrent.futures
from time import sleep
import bs4 as bs
import requests
import numpy as np
from matplotlib import pyplot as plt

print('This is from API!')
names = {}  # for run(name)
friend_url = ''  # for link_friend(url_id)


def link_friend(url_id='fyi1411', m=1):
    x, n = 0, 0
    i = [url_id]
    path = url_id
    print(f'Running {m} time(s).')
    while m > n:
        tries = 0
        print(f'path : {path}')
        print()
        source = requests.get(f'https://steamcommunity.com/id/{url_id}/friends/').text
        soup = bs.BeautifulSoup(source, 'lxml')
        sauce = soup.find_all('a', class_="selectable_overlay")
        if len(sauce) == 0 and tries == 0:  # no custom id = profiles
            tries += 1
            source = requests.get(f'https://steamcommunity.com/profiles/{url_id}/friends/').text
            soup = bs.BeautifulSoup(source, 'lxml')
            sauce = soup.find_all('a', class_="selectable_overlay")
            if len(sauce) == 0:
                print('private or no friends.')
            else:
                print('successful retry')
        if tries == 1:
            print('retried')
        for a in sauce:
            global friend_url
            friend_url = a['href']
            new_friend_url = friend_url.split('/')[-1]
            if new_friend_url not in i:
                i.append(new_friend_url)
            else:
                pass
        for y in i[x:]:
            x += 1
            print(x, y)
            try:
                source = requests.get(f'https://steamcommunity.com/profiles/{y}/friends/').text
                soup = bs.BeautifulSoup(source, 'lxml')
                sauce1 = soup.find('div', class_="friends_header_name")
                sauce1 = str(sauce1).split('>')
                sauce1 = sauce1[2].split('<')
                profile = sauce1[0]
                print(f'name : {profile}')
                keys = 'profiles'
            except IndexError:
                source = requests.get(f'https://steamcommunity.com/id/{y}/friends/').text
                soup = bs.BeautifulSoup(source, 'lxml')
                sauce1 = soup.find('div', class_="friends_header_name")
                sauce1 = str(sauce1).split('>')
                sauce1 = sauce1[2].split('<')
                profile = sauce1[0]
                print(f'name : {profile}')
                keys = 'id'
            print(f'https://steamcommunity.com/{keys}/{y}/friends/')
            print()
        n += 1
        print(str(n) + ' time(s)')
        url_id = i[n]
        if m > n:
            print(f'new_url_id : {url_id}')
            path += '/' + url_id
    else:
        print('Ended')


def pause(num=0):
    pyautogui.PAUSE = num


# pause time between each auto's action


def stop():
    pyautogui.keyDown('ctrl')
    pyautogui.press('f2')


# end run


def run(name='it'):
    if name not in names:
        names[name] = 1
    elif name in names:
        names[name] += 1
    print(f"{name} run {names[name]}")


# count program runs


def wait(time):
    m = 0
    while m < time:
        print(time - m)
        sleep(1)
        m += 1


# wait and print sec


def enemy():
    while True:
        location = str(pyautogui.locateOnScreen('Red.png'))
        if location != "None":
            location1 = location.split('(')[1]
            location2 = location1.split('=')
            location3 = []
            for i in range(1, 4):
                location3.append(location2[i].split(',')[0])
            location3.append(location2[4].split(')')[0])
            print(location3)
        else:
            print("N/A")


# BM enemy detector


point = [[3, 1.5, 1],
         [2, 1, 0],
         [4, 1.5, 1],
         [3, 1, 0],
         [3.5, .5, 1],
         [2, .5, 0],
         [5.5, 1, 1],
         [1, 1, 0]]


def sigmoid(y):
    return 1 / (1 + np.exp(-y))


def sigmoid_p(y):
    return sigmoid(y) * (1 - sigmoid(y))


def train():
    w1 = np.random.randn()
    w2 = np.random.randn()
    b = np.random.randn()
    learning_rate = 0.1
    cost = []
    iteration = []
    for i in range(100000):
        index = np.random.randint(len(point))
        a = point[index]
        z = w1 * a[0] + w2 * a[1] + b
        pred = sigmoid(z)
        dcost_dpred = 2 * (pred - a[2])
        dpred_dz = sigmoid_p(z)
        dz_dw1 = a[0]
        dz_dw2 = a[1]
        dz_db = 1
        dcost_dz = dcost_dpred * dpred_dz
        dcost_dw1 = dcost_dz * dz_dw1
        dcost_dw2 = dcost_dz * dz_dw2
        dcost_db = dcost_dz * dz_db
        w1 = w1 - learning_rate * dcost_dw1
        w2 = w2 - learning_rate * dcost_dw2
        b = b - learning_rate * dcost_db
        if i % 1000 == 0:
            c = 0
            for j in range(len(point)):
                p = point[j]
                p_pred = sigmoid(w1 * p[0] + w2 * p[1] + b)
                c += (p_pred - p[2]) ** 2
            cost.append(c)
            iteration.append(i)
    plt.plot(iteration, cost)
    plt.show()
    return cost, w1, w2, b


def test():
    cost, w1, w2, b = train()
    print(cost)
    print(w1, w2, b)
    correct = 0
    for d in point:
        a1 = d[0]
        a2 = d[1]
        target = d[2]
        pred = sigmoid(w1 * a1 + w2 * a2 + b)
        if abs(pred - target) <= 0.5:
            correct += 1
        else:
            print(d)
    print(f"{round(len(point) / correct) * 100}%")


def crit(crit_rate, crit_dmg, dmg=1, nor_dmg=1):
    nor_rate = 1 - crit_rate
    dmg = dmg * nor_rate * nor_dmg + dmg * crit_rate * crit_dmg
    return dmg


def morse_code(text, code='quack'):
    morse = {'a': [0, 1],
             'b': [1, 0, 0, 0],
             'c': [1, 0, 1, 0],
             'd': [1, 0, 0],
             'e': [0],
             'f': [0, 0, 1, 0],
             'g': [1, 1, 0],
             'h': [0, 0, 0, 0],
             'i': [0, 0],
             'j': [0, 1, 1, 1],
             'k': [1, 0, 1],
             'l': [0, 1, 1, 1],
             'm': [1, 1],
             'n': [1, 0],
             'o': [1, 1, 1],
             'p': [0, 1, 1, 0],
             'q': [1, 1, 0, 1],
             'r': [0, 1, 0],
             's': [0, 0, 0],
             't': [1],
             'u': [0, 0, 1],
             'v': [0, 0, 0, 1],
             'w': [0, 1, 1],
             'x': [1, 0, 0, 1],
             'y': [1, 0, 1, 1],
             'z': [1, 1, 0, 0],
             '1': [0, 1, 1, 1, 1],
             '2': [0, 0, 1, 1, 1],
             '3': [0, 0, 0, 1, 1],
             '4': [0, 0, 0, 0, 1],
             '5': [0, 0, 0, 0, 0],
             '6': [1, 0, 0, 0, 0],
             '7': [1, 1, 0, 0, 0],
             '8': [1, 1, 1, 0, 0],
             '9': [1, 1, 1, 1, 0],
             '0': [1, 1, 1, 1, 1]}
    code = list(code)
    encode = ''
    for word in list(text.split(' ')):
        for char in word:
            if char in morse:
                for i, num in enumerate(morse[char]):
                    if num:
                        encode += code[i].upper()
                    else:
                        encode += code[i]
                encode += ' '
            else:
                encode += char
        encode += '    '
    return encode


'''
sent = ''
while 1 and sent != 'exit':
    sent = input('> ')
    print(morse_code(sent))
'''


def sth(sec=1):
    print(f'sleep {sec} sec')
    sleep(sec)
    print('done sleeping')


def sth_thread(thread_range=10):
    threads = []
    for _ in range(thread_range):
        t = threading.Thread(target=sth, args=[1.5])
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()


def sth_future(*args):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        secs = [*args]
        results = [executor.submit(sth, sec) for sec in secs]
        for f in concurrent.futures.as_completed(results):
            print(f.result())
