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
            input_derivative if input_derivative is not None else loss.derivative(self.predicts, targets),
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


def save_model(ndarrays, cost_list, save_file=f"data/{save}"):
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
