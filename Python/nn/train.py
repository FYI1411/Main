if __name__ == '__main__':
    from nn import *
    import numpy as np
    import matplotlib.pyplot as plt
    import os
    import time
    import datetime
    import random
    start_time = time.time()
    # data
    batch_size = 3
    point = [[3, 1.5, 1],
             [2, 1, 0],
             [4, 1.5, 1],
             [3, 1, 0],
             [3.5, .5, 1],
             [2, .5, 0],
             [5.5, 1, 1],
             [1, 1, 0]]
    data = np.array([pot[0:2] for pot in point]).T
    targets = np.array([pot[2] for pot in point]).T
    weight = data[0]
    height = data[1]
    rand = random.sample(range(0, 8), batch_size)
    data = np.array([[weight[i], height[i]] for i in rand]).T
    target = np.array([targets[i] for i in rand]).T
    # test run
    activation1 = Activation_Sig()
    activation2 = activation1
    loss1 = Loss_MSE()
    loss2 = loss1
    if loading and save in os.listdir(f"{os.getcwd()}/data"):
        print(f"loaded {save}")
        from data import nnModel
        layer1 = Layer_Dense(2, 1, activation1, 
        weights=np.array(nnModel.ndarray0[0]), biases=np.array(nnModel.ndarray0[1]))
    else:
        layer1 = Layer_Dense(2, 1, activation1)
    # layerList = [layer1, layer2, layer3]
    layerList = [layer1]
    print(data)
    print(target)
    forward(data, layerList)
    lr = 0.1
    layer1.backprop(data, loss1, lr, targets=target)
    # training
    cost_list, index_list = [], []
    gen = 10000
    for index in range(gen + 1):
        rand = random.sample(range(0, 8), batch_size)
        data = np.array([[weight[i], height[i]] for i in rand]).T
        target = np.array([targets[i] for i in rand]).T
        forward(data, layerList)
        layer1.backprop(data, loss1, lr, targets=target)
        if index % 1000 == 0:
            index_list.append(index)
            forward(data, layerList)
            output = loss2.forward(layerList[-1].predicts, target)
            cost_list.append(output)
            print(index, output)
        if index % 100000 == 0 and index > 0:
            save_model(layerList, cost_list)
            print(f"saved {save}")
    for lay in layerList:
        print(lay.weights)
        print(lay.biases)
    print(f"Last cost: {cost_list[-1]}")
    print(f"Minima: {min(cost_list)}")
    print(f"Accuracy: {(100 - min(cost_list) * 100)}%")
    print(f'{os.getcwd()}/data/nnModel.py')
    save_model(layerList, cost_list, save_file=f'Python/nn/data/nnModel.py')
    plt.plot(index_list, cost_list)
    plt.show()
    plt.scatter([p[0] for p in point if p[2] == 0], [p[1] for p in point if p[2] == 0], color='blue')
    plt.scatter([p[0] for p in point if p[2] == 1], [p[1] for p in point if p[2] == 1], color='red')
    test_list = []
    for i, j in zip([0, .25, .5, .75, 1, 1.25, 1.5], range(7)):
        data = np.array([i, j]).T
        forward(data=data, layers=layerList)
        test_list.append(np.average(layerList[-1].predicts, axis=1))
    plt.plot(test_list)
    plt.xlabel("weight")
    plt.ylabel("height")
    plt.show()
    print(f"saved {save}")
    print(f"time: {datetime.timedelta(seconds=time.time() - start_time)}")
    while True:
        try:
            weight = input("weight? ")
            height = input("height? ")
            data = np.array([float(weight), float(height)]).T
            print(data)
            forward(data=data, layers=layerList)
            print(np.average(layerList[-1].predicts, axis=1))
        except Exception as e:
            print(e)
'''
    print("Layer_Conv")
    xarray = np.array([[-1, -1, -1, -1, -1, -1, -1, -1, -1],
                       [-1, 1, -1, -1, -1, -1, -1, 1, -1],
                       [-1, -1, 1, -1, -1, -1, 1, -1, -1],
                       [-1, -1, -1, 1, -1, 1, -1, -1, -1],
                       [-1, -1, -1, -1, 1, -1, -1, -1, -1],
                       [-1, -1, -1, 1, -1, 1, -1, -1, -1],
                       [-1, -1, 1, -1, -1, -1, 1, -1, -1],
                       [-1, 1, -1, -1, -1, -1, -1, 1, -1],
                       [-1, -1, -1, -1, -1, -1, -1, -1, -1]])
    feature = np.array([[1, -1, -1],
                        [-1, 1, -1],
                        [-1, -1, 1]])
    clayer = Layer_Conv(activation=Activation_ReLU)
    clayer.filter(feature, xarray)
    clayer.normalize()
    clayer.normalize()
    clayer.pooling()
    clayer.normalize()
    clayer.pooling()
    print(clayer.conv_ndarray)
'''
