import tkinter as tk
from tkinter import ttk, PhotoImage, Button, messagebox
import random
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path

colores_disponibles = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white', 'purple', 'orange', 'gray', 'brown']

def relative_to_assets(path: str) -> Path:
    current_folder = Path(__file__).parent
    assets_folder = current_folder / "assets"
    return assets_folder / path

def visualizar_grafo(grafo, coloreo=None, frame_grafo=None):
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    G = nx.Graph()
    for nodo, vecinos in grafo.items():
        G.add_node(nodo)
        for vecino in vecinos:
            G.add_edge(nodo, vecino)
    pos = nx.spring_layout(G)
    if coloreo:
        colores = [coloreo.get(nodo) for nodo in G.nodes()]
    else:
        colores = 'lightblue' 
    nx.draw(G, pos, with_labels=True, node_color=colores, edge_color='gray', ax=ax)
    if frame_grafo:
        for widget in frame_grafo.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame_grafo) 
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                                    
def colorear_grafo(grafo, num_colores):
    coloreo = {}
    if num_colores > len(colores_disponibles):
        print("Advertencia: Se solicitaron más colores de los disponibles. Algunos colores se repetirán.")
        num_colores = len(colores_disponibles)
    
    for nodo in grafo:
        colores_disponibles_para_nodo = colores_disponibles[:num_colores]
        for vecino in grafo[nodo]:
            if vecino in coloreo:
                if coloreo[vecino] in colores_disponibles_para_nodo:
                    colores_disponibles_para_nodo.remove(coloreo[vecino])
        coloreo[nodo] = colores_disponibles_para_nodo[0] if colores_disponibles_para_nodo else 'black'
    
    return coloreo

def generar_grafo_aleatorio(num_regiones):
    grafo = {str(i): set() for i in range(num_regiones)}
    nodos = list(grafo.keys())
    for nodo in nodos:
        posible_conexion = nodo
        while posible_conexion == nodo or posible_conexion in grafo[nodo]:
            posible_conexion = random.choice(nodos)
        grafo[nodo].add(posible_conexion)
        grafo[posible_conexion].add(nodo)
    for _ in range(int(num_regiones * 1.5)):
        nodo = random.choice(nodos)
        posible_conexion = random.choice(nodos)
        if nodo != posible_conexion and posible_conexion not in grafo[nodo]:
            grafo[nodo].add(posible_conexion)
            grafo[posible_conexion].add(nodo)
    
    return grafo

def generar_grafo():
    try:
        num_regiones = int(entrada_regiones.get())
        num_colores = int(entrada_colores.get())
        if not entrada_regiones.get() or not entrada_colores.get():
            messagebox.showerror("Error", "Los campos no pueden estar vacíos.")
            return
        if not (16 <= num_regiones <= 30):
            messagebox.showerror("Error", "El número de regiones debe estar entre 16 y 30.")
            return
        if num_colores < 1:
            messagebox.showerror("Error", "Debe haber al menos 1 color.")
            return
        grafo_generado = generar_grafo_aleatorio(num_regiones)
        print("Grafo generado:", grafo_generado)
        coloreo = colorear_grafo(grafo_generado, num_colores)
        visualizar_grafo(grafo_generado, coloreo, frame_grafo)
    except ValueError as e:
        messagebox.showerror("Error", f"Por favor, ingrese números válidos. Detalle del error: {e}")
ventana = tk.Tk()
ventana.title("Colorear Regiones - Generación Automática")
ventana.geometry("800x650")

frame_entrada = ttk.Frame(ventana, padding="10")
frame_entrada.pack(fill=tk.X)
etiqueta_regiones = ttk.Label(frame_entrada, text="Número de Regiones (16-30):")
etiqueta_regiones.pack(side=tk.LEFT)
entrada_regiones = ttk.Entry(frame_entrada)
entrada_regiones.pack(side=tk.LEFT, padx=(0, 20))
etiqueta_colores = ttk.Label(frame_entrada, text="Número de Colores:")
etiqueta_colores.pack(side=tk.LEFT)
entrada_colores = ttk.Entry(frame_entrada)
entrada_colores.pack(side=tk.LEFT)
frame_grafo = ttk.Frame(ventana, padding="10")
frame_grafo.pack(fill=tk.BOTH, expand=True)
frame_acciones = ttk.Frame(ventana, padding="10")
frame_acciones.pack(fill=tk.X)
canvas_textos = tk.Canvas(ventana, height=100) 
canvas_textos.place(relx=0.5, rely=0.95, anchor="center", width=800)

textos = [
    ("IA - UMSS", 37, 20),
    ("Callao Lopez William Humberto", 36, 35),
    ("Fernandez Sandoval Camila Wara", 36, 50),
    ("Vilela Montoya Maria Fernanda", 36, 65),
]

for texto, x, y in textos:
    canvas_textos.create_text(x, y, anchor="nw", text=texto, fill="#A4A4A4", font=("Inter ExtraLight", 10))
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(canvas_textos, image=button_image_1, borderwidth=0, highlightthickness=0, command=generar_grafo, relief="flat")
canvas_textos.create_window(400, 50, window=button_1, width=193, height=38)


ventana.mainloop()
