import numpy as np
import cv2 as cv
import tkinter as tk
import histograma as op
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

# Função para criar um botão
def criar_botao(frame, texto, funcao, linha, coluna):
    botao = ttk.Button(frame, text=texto, command=funcao, width=20)
    botao.grid(row=linha, column=coluna, padx=5, pady=10)

# Função para criar um botão com entrada numerica na frente
def criar_botao_num1(frame, texto, funcao, linha, coluna):
    botao = ttk.Button(frame, text=texto, command=funcao, width=20)
    botao.grid(row=linha, column=coluna, padx=5, pady=10)
    campo = tk.Entry(frame, width=4)
    campo.grid(row=linha, column=coluna+1, padx=10, pady=5)
    return campo

# Função para redimensionar uma imagem
def redimensionar(imagem, nova_largura, nova_altura):
    return cv.resize(imagem, (nova_largura, nova_altura), interpolation=cv.INTER_LINEAR)

# Função para abrir e carregar uma imagem
def selecionar_imagem():
    caminho_imagem = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if caminho_imagem:
        carregar_imagem(caminho_imagem)

# Função para carregar uma imagem
def carregar_imagem(caminho):
    global imagem_cv, imagem_tk, imagem_o
    imagem_o = cv.imread(caminho)
    altura, largura = imagem_o.shape[:2]
    ar = largura / altura
    imagem_cv = redimensionar(imagem_o, int(512*ar), 512)
    imagem_cv = cv.cvtColor(imagem_cv, cv.COLOR_BGR2RGB)  # Converter BGR para RGB
    imagem_pil = Image.fromarray(imagem_cv)
    imagem_tk = ImageTk.PhotoImage(imagem_pil)
    label_imagem_original.config(image=imagem_tk)
    label_imagem_original.image = imagem_tk

def salvar_imagem():
    global imagem_processada, imagem_o, last_op
    caminho = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if caminho is not None:
        cv.imwrite(caminho, last_op(imagem_o))

def invert():
    global imagem_cv, imagem_tk_processada, last_op
    if imagem_cv is not None:
        imagem_processada = op.invert(imagem_cv).astype('uint8')
        last_op = lambda img: op.invert(img)
        imagem_pil = Image.fromarray(imagem_processada)
        imagem_tk_processada = ImageTk.PhotoImage(imagem_pil)
        label_imagem_processada.config(image=imagem_tk_processada)
        label_imagem_processada.image = imagem_tk_processada

def constant():
    global imagem_cv, imagem_tk_processada, last_op
    try:
        c = int(c_campo.get())
        if imagem_cv is not None:
            imagem_processada = op.constante(imagem_cv, c).astype('uint8')
            last_op = lambda img: op.constante(img, c)    
            imagem_pil = Image.fromarray(imagem_processada)
            imagem_tk_processada = ImageTk.PhotoImage(imagem_pil)
            label_imagem_processada.config(image=imagem_tk_processada)
            label_imagem_processada.image = imagem_tk_processada
    except ValueError:
        print("Por favor, insira um número válido.")

def brilho():
    global imagem_cv, imagem_tk_processada, last_op
    try:
        b = int(b_campo.get())
        if imagem_cv is not None:
            imagem_processada = op.brilho(imagem_cv, b).astype('uint8')
            last_op = lambda img: op.brilho(img, b)    
            imagem_pil = Image.fromarray(imagem_processada)
            imagem_tk_processada = ImageTk.PhotoImage(imagem_pil)
            label_imagem_processada.config(image=imagem_tk_processada)
            label_imagem_processada.image = imagem_tk_processada
    except ValueError:
        print("Por favor, insira um número válido.")

def contraste():
    global imagem_cv, imagem_tk_processada, last_op
    try:
        c1 = int(c1_campo.get())
        if imagem_cv is not None:
            if c1 < 0:
                c1 = max(-255//2, c1)
                imagem_processada = op.contraste(imagem_cv, -c1).astype('uint8')
                last_op = lambda img: op.contraste(img, -c1)    
            else:
                c1 = min(255//2, c1)
                imagem_processada = op.normalizar(imagem_cv, c1, 255-c1).astype('uint8')
                last_op = lambda img: op.normalizar(img, c1, 255-c1)    
            imagem_pil = Image.fromarray(imagem_processada)
            imagem_tk_processada = ImageTk.PhotoImage(imagem_pil)
            label_imagem_processada.config(image=imagem_tk_processada)
            label_imagem_processada.image = imagem_tk_processada
    except ValueError:
        print("Por favor, insira um número válido.")
    
def normalizar():
    global imagem_cv, imagem_tk_processada, last_op
    if imagem_cv is not None:
        maxf = np.max(imagem_cv)
        minf = np.min(imagem_cv)
        print(minf, maxf)
        imagem_processada = op.normalizar(imagem_cv, minf, maxf).astype('uint8')
        last_op = lambda img: op.normalizar(img, minf, maxf)    
        imagem_pil = Image.fromarray(imagem_processada)
        imagem_tk_processada = ImageTk.PhotoImage(imagem_pil)
        label_imagem_processada.config(image=imagem_tk_processada)
        label_imagem_processada.image = imagem_tk_processada

def limiar():
    global imagem_cv, imagem_tk_processada, last_op
    try:
        t = int(t_campo.get())
        if imagem_cv is not None:
            imagem_processada = op.limiar(imagem_cv, t).astype('uint8')
            last_op = lambda img: op.limiar(img, t)    
            imagem_pil = Image.fromarray(imagem_processada)
            imagem_tk_processada = ImageTk.PhotoImage(imagem_pil)
            label_imagem_processada.config(image=imagem_tk_processada)
            label_imagem_processada.image = imagem_tk_processada
    except ValueError:
        print("Por favor, insira um número válido.")

def gama():
    global imagem_cv, imagem_tk_processada, last_op
    try:
        g = float(gama_campo.get())
        if imagem_cv is not None:
            imagem_processada = op.gama(imagem_cv, g).astype('uint8')
            last_op = lambda img: op.gama(img, g)    
            imagem_pil = Image.fromarray(imagem_processada)
            imagem_tk_processada = ImageTk.PhotoImage(imagem_pil)
            label_imagem_processada.config(image=imagem_tk_processada)
            label_imagem_processada.image = imagem_tk_processada
    except ValueError:
        print("Por favor, insira um número válido.")

def equalizar():
    global imagem_cv, imagem_tk_processada, last_op
    if imagem_cv is not None:
        imagem_processada = op.equalizar(imagem_cv).astype('uint8')
        # imagem_processada = op.normalizar(imagem_processada, 0, 255).astype('uint8')
        last_op = lambda img: op.equalizar(img)  
        imagem_pil = Image.fromarray(imagem_processada)
        imagem_tk_processada = ImageTk.PhotoImage(imagem_pil)
        label_imagem_processada.config(image=imagem_tk_processada)
        label_imagem_processada.image = imagem_tk_processada
        imagem_pil = Image.fromarray(imagem_cv)
        imagem_tk = ImageTk.PhotoImage(imagem_pil)
        label_imagem_original.config(image=imagem_tk)
        label_imagem_original.image = imagem_tk

# Função para alternar o modo fullscreen
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))
    return "break"

# Função para fechar o programa
def fechar_programa(event=None):
    root.destroy()
    return "break"

# Configuração da janela principal do Tkinter
root = tk.Tk()
root.title("Processamento de Imagens")

# Dimensões da janela
largura_janela = 800
altura_janela = 600

# Dimensões da tela
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

# Posição central
posicao_x = (largura_tela - largura_janela) // 2
posicao_y = (altura_tela - altura_janela) // 2

# Configura a geometria da janela para centralizar
root.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

frame0 = tk.Frame(root)
frame0.pack(pady=10, padx=10)

# Frame para organizar o botão e o campo de entrada
frame = tk.Frame(frame0)
frame.grid(row=0, column=0, pady=10, padx=10)

# Botões
criar_botao(frame, "Selecionar Imagem", selecionar_imagem, 0, 0)

c_campo = criar_botao_num1(frame, "Constant", constant, 1, 0)

criar_botao(frame, "Invert", invert, 2, 0)

b_campo = criar_botao_num1(frame, "Brilho", brilho, 3, 0)

c1_campo = criar_botao_num1(frame, "Contraste", contraste, 4, 0)

criar_botao(frame, "Normalizar", normalizar, 5, 0)

t_campo = criar_botao_num1(frame, "Limiar", limiar, 6, 0)

gama_campo = criar_botao_num1(frame, "Gama", gama, 7, 0)

criar_botao(frame, "Equalizar", equalizar, 8, 0)

# criar_botao(frame0, "Salvar Imagem", salvar_imagem, 1, 0)
criar_botao(frame0, "Salvar Imagem", salvar_imagem, 1, 1)

# Labels para mostrar a imagem original e processada
label_imagem_original = tk.Label(frame0)
label_imagem_original.grid(row=2, column=0, padx=10, pady=10)

label_imagem_processada = tk.Label(frame0)
label_imagem_processada.grid(row=2, column=1, padx=10, pady=10)

# Bindings para alternar, sair do modo fullscreen e fechar o programa
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", fechar_programa)

# Variáveis globais para armazenar as imagens

# Carregar a imagem Lenna.png
carregar_imagem("Lenna.png")
invert()

# Executar a interface gráfica
root.mainloop()