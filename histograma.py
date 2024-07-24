import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

k = 255

def histogram(img):
    vet_256 = np.zeros(256, dtype=int)
    count_vet = np.bincount(img.flatten())
    vet_256[:len(count_vet)] = count_vet
    return vet_256

def func_constante(x, c):
    return c

def func_invert(x):
    return k - x

def func_dim_brilho(x, b):
    return max(0, x - b)

def func_aum_brilho(x, b):
    return min(k, x + b)

def func_dim_contraste(x, c1):
    c2 = k - c1
    result = int((((c2-c1)*x)/k)+c1)
    return min(255, max(0, result))

def func_aum_contraste(x, minf):
    maxf = k - minf 
    result = int(((x-minf)/(maxf-minf))*k) 
    return min(255, max(0, result))

def func_limiar(x, t):
    if x > t: return k
    else: return 0

def func_normalizar(x, maxi):
    return (x/maxi)*k
        
def gama(img, gama):
    result = np.power(img.astype(np.uint64), gama)
    normalizar = np.vectorize(func_normalizar)
    return normalizar(result, result.max())


# carregar imagem
img = cv.imread('Lenna.png')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

# converter para escala de cinza
# gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# funcoes vetorizadas
constante = np.vectorize(func_constante)
invert = np.vectorize(func_invert)
dim_brilho = np.vectorize(func_dim_brilho)
aum_brilho = np.vectorize(func_aum_brilho)
dim_contraste = np.vectorize(func_dim_contraste)
aum_contraste = np.vectorize(func_aum_contraste)
limiar = np.vectorize(func_limiar)

# plot
figure, axis = plt.subplots(2, 2)
figure.set_size_inches(20,10)

modified_img = gama(img, 2).astype(np.uint8)
h1 = histogram(img)
h2 = histogram(modified_img)
arange = np.arange(256)
axis[0,0].bar(arange, h1)
axis[0,1].bar(arange, h2)
axis[1,0].imshow(img)
axis[1,0].axis('off')
axis[1,1].imshow(modified_img)
axis[1,1].axis('off')
plt.show()

# cv.imshow('original', gray)
# cv.imshow('modified', gama(gray, 0.5).astype(np.uint8))
# cv.moveWindow('original', 0, 0)
# cv.moveWindow('modified', 512, 0)
# cv.waitKey(0)
# cv.destroyAllWindows()