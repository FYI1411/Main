from nn import Layer_Dense, np, Activation_Leaky_ReLU, Cost_SSR, forward, test
import timeit

print(timeit.timeit("test()", number=10000, setup="from nn import Layer_Dense, np, Activation_Leaky_ReLU, Cost_SSR, forward, test"))
