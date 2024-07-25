import numpy as np
import cv2 as cv

k = 255

def histogram(img):
    vet_256 = np.zeros(256, dtype=int)
    count_vet = np.bincount(img.flatten())
    vet_256[:len(count_vet)] = count_vet
    return vet_256

    
def func_constante(x, c):
    return c
constante = np.vectorize(func_constante)

def func_invert(x):
    return k - x
invert = np.vectorize(func_invert)

def func_brilho(x, b):
    return min(255, max(0, x + b))
brilho = np.vectorize(func_brilho)

def func_contraste(x, c1):
    c2 = k - c1
    result = int((((c2-c1)*x)/k)+c1)
    return min(255, max(0, result))
contraste = np.vectorize(func_contraste)

def func_normalizar(x, minf, maxf):
    result = int(((x-minf)/(maxf-minf))*k) 
    return min(255, max(0, result))
normalizar = np.vectorize(func_normalizar)

def func_limiar(x, t):
    if x > t: return k
    else: return 0
limiar = np.vectorize(func_limiar)
        
def gama(img, gama):
    result = np.power(img.astype(np.uint64), gama)
    return normalizar(result, 0, result.max())

def equalizar(img):
    m, n = img.shape
    hist = histogram(img)
    hacc = np.cumsum(hist)
    aux_func = np.vectorize(lambda x: int((k*hacc[x])/(m*n)))
    return aux_func(img)

