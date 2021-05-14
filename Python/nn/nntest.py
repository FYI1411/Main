import numpy as np
import matplotlib.pyplot as plt
import random
point = [[3,   1.5, 1],
         [2,   1,   0],
         [4,   1.5, 1],
         [3,   1,   0],
         [3.5, .5,  1],
         [2,   .5,  0],
         [5.5,  1,  1],
         [1,    1,  0]]
# 4.5, 1 = 1
data = np.array([pot[0:2] for pot in point]).T
targets = np.array([pot[2] for pot in point]).T
weight = data[0]
height = data[1]
rand = random.sample(range(0, 8), 3)
print(np.array([[weight[i], height[i]]for i in rand]).T)
print(np.array([targets[i] for i in rand]))
print(data, '\n', targets)
plt.scatter([p[0] for p in point if p[2] == 0], [p[1] for p in point if p[2] == 0], color='blue')
plt.scatter([p[0] for p in point if p[2] == 1], [p[1] for p in point if p[2] == 1], color='red')
plt.show()
