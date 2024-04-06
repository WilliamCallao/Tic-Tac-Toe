import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Lista de colores reconocibles por Matplotlib
colores_disponibles = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white', 'purple', 'orange', 'gray', 'brown']


# def visualizar_grafo(grafo, coloreo=None):
#     G = nx.Graph()

#     # Añadir nodos y aristas al grafo de NetworkX
#     for nodo, vecinos in grafo.items():
#         G.add_node(nodo)
#         for vecino in vecinos:
#             G.add_edge(nodo, vecino)
    
#     pos = nx.spring_layout(G)  # Generar posiciones de los nodos

#     # Si se proporciona un coloreo, usarlo
#     if coloreo:
#         colores = [coloreo.get(nodo) for nodo in G.nodes()]
#     else:
#         colores = 'lightblue'  # Color por defecto si no se especifica coloreo
    
#     nx.draw(G, pos, with_labels=True, node_color=colores, edge_color='gray')

#     # Mostrar el grafo
#     plt.show()
def visualizar_grafo(grafo, coloreo=None, frame_grafo=None):
    # Crear una figura de Matplotlib
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    G = nx.Graph()
    # Añadir nodos y aristas al grafo de NetworkX
    for nodo, vecinos in grafo.items():
        G.add_node(nodo)
        for vecino in vecinos:
            G.add_edge(nodo, vecino)
    pos = nx.spring_layout(G)  # Generar posiciones de los nodos
    # Si se proporciona un coloreo, usarlo
    if coloreo:
        colores = [coloreo.get(nodo) for nodo in G.nodes()]
    else:
        colores = 'lightblue'  # Color por defecto si no se especifica coloreo
    nx.draw(G, pos, with_labels=True, node_color=colores, edge_color='gray', ax=ax)
    # Si se proporciona un frame, usarlo para embeber el gráfico
    if frame_grafo:
        # Limpiar el frame_grafo antes de añadir otro gráfico
        for widget in frame_grafo.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame_grafo)  # Crear el canvas de Matplotlib en el frame de Tkinter
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                                    
def colorear_grafo(grafo, num_colores):
    coloreo = {}
    # Asegúrate de que no se soliciten más colores de los disponibles
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
    
    # Asegurar que cada nodo tenga al menos una conexión
    for nodo in nodos:
        posible_conexion = nodo
        while posible_conexion == nodo or posible_conexion in grafo[nodo]:
            posible_conexion = random.choice(nodos)
        grafo[nodo].add(posible_conexion)
        grafo[posible_conexion].add(nodo)
    
    # Añadir algunas conexiones adicionales aleatoriamente para hacer el grafo más interesante
    for _ in range(int(num_regiones * 1.5)):  # Número arbitrario de conexiones extra
        nodo = random.choice(nodos)
        posible_conexion = random.choice(nodos)
        
        # Evitar bucles y duplicados
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
        # Lugar para implementar la generación del grafo
        grafo_generado = generar_grafo_aleatorio(num_regiones)
        print("Grafo generado:", grafo_generado)
        coloreo = colorear_grafo(grafo_generado, num_colores)
        # visualizar_grafo(grafo_generado, coloreo)
        visualizar_grafo(grafo_generado, coloreo, frame_grafo)

# Aquí irá la llamada a la función de generación y coloración del grafo
    except ValueError as e:
        messagebox.showerror("Error", f"Por favor, ingrese números válidos. Detalle del error: {e}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Colorear Regiones - Generación Automática")

# Configuración de la ventana
ventana.geometry("800x600")

# Sección de Entrada de Parámetros
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

# Espacio para la visualización del grafo
frame_grafo = ttk.Frame(ventana, padding="10")
frame_grafo.pack(fill=tk.BOTH, expand=True)

# Botones para acciones
frame_acciones = ttk.Frame(ventana, padding="10")
frame_acciones.pack(fill=tk.X)

boton_generar = ttk.Button(frame_acciones, text="Generar Grafo", command=generar_grafo)
boton_generar.pack(side=tk.LEFT, padx=5)

boton_colorear = ttk.Button(frame_acciones, text="Colorear Grafo", command=generar_grafo)

boton_colorear.pack(side=tk.LEFT, padx=5)

ventana.mainloop()
