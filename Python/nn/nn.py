import numpy as np
save = "nnModel.py"
saving, loading = True, False


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
        inputs = np.exp(inputs - np.max(inputs, axis=0, keepdims=True))
        return inputs / np.sum(inputs, axis=0, keepdims=True)


class Loss_MSE:
    @staticmethod
    def forward(inputs, targets):
        loss = np.subtract(inputs, targets)
        return np.average(np.power(loss, 2))

    @staticmethod
    def derivative(inputs, targets):
        loss = np.subtract(inputs, targets)
        return np.average(loss * 2 / loss.shape[1], axis=0)


class Loss_CE:
    @staticmethod
    def forward(inputs, targets):
        softmax = Activation_Softmax.normalize(inputs)
        targets = np.clip(targets, 1e-7, 1-1e-7)
        return -np.log(np.sum(softmax * targets, axis=0, keepdims=True))

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


def save_model(ndarrays, cost_list, save_file=f"{save}"):
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
	array = np.array([[1,2,3],[4,5,6]]).T
	targets = np.array([[1,0,0],[0,1,0]]).T
	print(np.sum(array * targets, axis=0, keepdims=True))
	loss = Loss_CE.forward(array, targets)	
	print(loss)
