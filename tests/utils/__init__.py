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

def pdf_normal(x, mean, var, normed=False):
    norm = 1 / np.sqrt(2 * np.pi) / var if normed else 1
    shape = np.exp(0.5 * ((mean - x) / var) ** 2)
    return norm * shape
