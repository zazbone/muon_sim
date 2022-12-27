import numpy as np


def cst(x, C):
    x = np.array(x)
    return np.full(x.shape, C)

def linear(x, a, b):
    return a * x + b

def poly(x, coef, power):
    x = np.array(x)
    y = np.zeros(x.shape)
    for c, p in zip(coef, power):
        y += c * np.power(x, p)
    return y