import numpy as np
from matplotlib import pyplot as plt

point = [[3,   1.5, 1],
         [2,   1,   0],
         [4,   1.5, 1],
         [3,   1,   0],
         [3.5, .5,  1],
         [2,   .5,  0],
         [5.5,  1,  1],
         [1,    1,  0]]


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
    for i in range(10000):
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
                c += (p_pred - p[2])**2
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
    print(f"{round(correct / len(point))*100}%")


test()
