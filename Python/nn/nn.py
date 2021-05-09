import numpy as np
save = "nnModel.py"
saving, loading = True, False


# used in Layer_Conv.pooling()
def rrange(start, stop=None, step=1):
    for i in range(start, stop, step):
        yield i
    if stop is not None and (stop + 1) % step != 0:
        yield stop - step + 1 + (stop + 1) % step


class Activation_Linear:
    @staticmethod
    def forward(inputs):
        return inputs

    @staticmethod
    def derivative(inputs):
        return (inputs > 0) + (inputs <= 0)


class Activation_Sig:
    @staticmethod
    def forward(inputs):
        return 1 / (1 + np.exp(-inputs))

    @staticmethod
    def derivative(inputs):
        return 1 / (1 + np.exp(-inputs)) * (1 - 1 / (1 + np.exp(-inputs)))


class Activation_ReLU:
    @staticmethod
    def forward(inputs):
        return inputs * (inputs > 0)

    @staticmethod
    def derivative(inputs):
        return 1 * (inputs > 0)


class Activation_Leaky_ReLU:
    @staticmethod
    def forward(inputs):
        return ((inputs > 0) * inputs) + ((inputs <= 0) * inputs * 0.01)

    @staticmethod
    def derivative(inputs):
        return ((inputs > 0) * 1) + ((inputs <= 0) * 0.01)


class Activation_Softmax:
    @staticmethod
    def normalize(inputs):
        inputs = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        return inputs / np.sum(inputs, axis=1, keepdims=True)


class Loss_MSE:
    @staticmethod
    def forward(inputs, targets):
        loss = np.subtract(inputs, targets)
        return np.average(np.power(loss, 2))

    @staticmethod
    def derivative(inputs, targets):
        loss = np.subtract(inputs, targets)
        return loss * 2 / loss.shape[1]


class Loss_CE:
    @staticmethod
    def forward(inputs, targets):
        inputs = np.exp(inputs)
        softmax = inputs / np.sum(inputs, axis=1)[:, None]
        return np.sum(-np.log(softmax) * targets)

    @staticmethod
    def derivative(inputs, targets):
        inputs = np.exp(inputs)
        softmax = inputs / np.sum(inputs, axis=1)[:, None]
        targets = np.argmax(targets, axis=1)
        return np.array([np.sum([softmax[i][j] - 1 if targets[i] == j
                        else softmax[i][j] for i in range(len(softmax))]) for j in range(len(targets))])


class Layer_Dense:
    def __init__(self, n_inputs, n_neurons, activation, weights=None, biases=None):
        self.weights = np.array(weights) if weights is not None else 0.1 * np.random.randn(n_inputs, n_neurons)
        self.biases = np.array(biases) if biases is not None else np.zeros((n_neurons, 1))
        self.activation = activation
        self.outputs, self.predicts, self.input_derivative = None, None, None

    def forward(self, inputs):
        self.outputs = np.dot(self.weights.T, inputs) + self.biases
        self.predicts = self.activation.forward(self.outputs)

    def backprop(self, inputs, loss, learning_rate, input_derivative=None, targets=None):
        bias_derivative = np.multiply(
            input_derivative if input_derivative is not None
            else loss.derivative(self.predicts, targets),
            self.activation.derivative(self.outputs))
        weight_derivative = np.dot(inputs, bias_derivative.T)
        self.weights = np.subtract(self.weights, learning_rate * weight_derivative / self.weights.shape[1])
        self.biases = np.subtract(self.biases, learning_rate * np.average(bias_derivative, axis=0))
        self.input_derivative = np.dot(self.weights, bias_derivative)


class Layer_Conv:
    def __init__(self, activation, pool_shape=(2, 2)):
        self.pool_shape = pool_shape
        self.activation = activation
        self.conv_ndarray = None

    def filter(self, feature_map, data=None):
        data = data if data is not None else self.conv_ndarray
        j, k = data.shape
        height, width = feature_map.shape
        output = np.array([(np.average(np.multiply([data[i1:i1 + height][i3][i2:i2 + width]
                           for i3 in range(len(data[i1:i1 + height]))], feature_map))) for i2 in range(k - width + 1)
                           for i1 in range(j - height + 1)]).reshape((j - height + 1, k - width + 1))
        self.conv_ndarray = output

    def normalize(self):
        self.conv_ndarray = self.activation.forward(self.conv_ndarray)

    def pooling(self):
        j, k = self.conv_ndarray.shape
        height, width = self.pool_shape
        output = np.array([(np.max([self.conv_ndarray[i1:i1 + height][i3][i2:i2 + width]
                          for i3 in range(len(self.conv_ndarray[i1:i1+height]))])) for i2 in rrange(0, k - width + 1, width)
                          for i1 in rrange(0, j - height + 1, height)]).reshape(-(j // -height), -(k // -width))
        self.conv_ndarray = output


def save_model(ndarrays, save_file=f"data/{save}"):
    if saving:
        with open(save_file, "w+", encoding="utf-8") as f:
            for i, ndarray in enumerate(ndarrays):
                f.write(f"ndarray{i} = [{ndarray.weights.tolist()},\n{ndarray.biases.tolist()}]\n")
            f.write("ndarrayList = [")
            for i in range(len(ndarrays)):
                f.write(f"ndarray{i}" + f"{', ' if i != len(ndarrays) - 1 else ''}")
            f.write(']\n')
            f.write(f"# cost: {cost_list[-1]}\n")
            f.write(f"# minima: {min(cost_list)}\n")


def forward(data, layers):
    inputs = data
    for layer in layers:
        layer.forward(inputs)
        inputs = layer.activation.forward(layer.outputs)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import os
    import time
    import datetime
    start_time = time.time()
    # data
    X = np.array([[1, 2, 3, 2.5],
                  [2.0, 5.0, -1.0, 2.0],
                  [-1.5, 2.7, 3.3, -0.8]]).T
    target1 = np.array([[1, 0, 0], [0, 0, 1], [1, 0, 0]])
    # test run
    activation1 = Activation_Leaky_ReLU()
    activation2 = activation1
    loss1 = Loss_MSE()
    loss2 = loss1
    if loading and save in os.listdir(f"{os.getcwd()}/data"):
        print(f"loaded {save}")
        from Python.nn.data.nnModel import *
        layer1 = Layer_Dense(4, 3, activation1, weights=np.array(ndarray0[0]), biases=np.array(ndarray0[1]))
        layer2 = Layer_Dense(3, 4, activation1, weights=np.array(ndarray1[0]), biases=np.array(ndarray1[1]))
        layer3 = Layer_Dense(4, 3, activation2, weights=np.array(ndarray2[0]), biases=np.array(ndarray2[1]))
    else:
        layer1 = Layer_Dense(4, 3, activation1)
        layer2 = Layer_Dense(3, 4, activation1)
        layer3 = Layer_Dense(4, 3, activation2)
    layerList = [layer1, layer2, layer3]
    forward(X, layerList)
    lr = 0.1
    layer3.backprop(layer2.predicts, loss2, lr, targets=target1)
    layer2.backprop(layer1.predicts, loss1, lr, input_derivative=layer3.input_derivative)
    layer1.backprop(X, loss1, lr, input_derivative=layer2.input_derivative)
    # training
    cost_list, index_list = [], []
    gen = 100000
    for index in range(gen + 1):
        forward(X, layerList)
        layer3.backprop(layer2.predicts, loss2, lr, targets=target1)
        layer2.backprop(layer1.predicts, loss1, lr, input_derivative=layer3.input_derivative)
        layer1.backprop(X, loss1, lr, input_derivative=layer2.input_derivative)
        if index % 1000 == 0:
            index_list.append(index)
            forward(X, layerList)
            cost_list.append(loss2.forward(layer3.predicts, target1))
            print(index, loss2.forward(layer3.predicts, target1))
        if index % 100000 == 0 and index > 0:
            save_model(layerList)
            print(f"saved {save}")
    for lay in layerList:
        print(lay.weights)
        print(lay.biases)
    print(f"Last cost: {cost_list[-1]}")
    print(f"Minima: {min(cost_list)}")
    print(f"Max accuracy: {(100 - min(cost_list) * 100)}%")
    save_model(layerList)
    plt.plot(index_list, cost_list)
    plt.show()
    print(f"saved {save}")
    print(f"time: {datetime.timedelta(seconds=time.time() - start_time)}")
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
