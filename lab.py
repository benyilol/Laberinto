import random
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import deque

# Matriz del laberinto aleatorea

def generar_laberinto(tamano=6):
    laberinto = [[random.choice([0, 1, 3, 4, 111]) for _ in range(tamano)] for _ in range(tamano)]
    laberinto[0][0] = 0  # Entrada
    laberinto[tamano - 1][tamano - 1] = 2  # Salida
    return laberinto

laberinto = generar_laberinto()
entrada = (0, 0)
salida = (len(laberinto) - 1, len(laberinto) - 1)
teletransportes = {3: 4, 4: 3}

# Función para resolver el laberinto
def resolver_laberinto():
    camino = buscar_camino_bfs()
    if camino:
        mostrar_camino(camino)
    else:
        messagebox.showinfo("Laberinto", "No se encontró un camino hacia la salida. No siempre se puede ganar, ¡inténtalo de nuevo!")

# Función BFS para buscar el camino
def buscar_camino_bfs():
    queue = deque([(entrada[0], entrada[1], [])])
    visitado = set()

    while queue:
        x, y, camino = queue.popleft()
        if (x, y) == salida:
            camino.append((x, y))
            return camino
        if (x, y) in visitado or not es_valido(x, y):
            continue
        if laberinto[x][y] == 111 and not acertijo():
            continue
        visitado.add((x, y))
        camino.append((x, y))
        valor_actual = laberinto[x][y]
        if valor_actual in teletransportes:
            destino = encontrar_teletransporte(x, y)
            queue.append((destino[0], destino[1], camino.copy()))
        else:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                queue.append((x + dx, y + dy, camino.copy()))
    return None

def es_valido(x, y):
    return 0 <= x < len(laberinto) and 0 <= y < len(laberinto[0]) and laberinto[x][y] in (0, 2, 3, 4, 111)

# Teletransporte entre celdas
def encontrar_teletransporte(x, y):
    valor = laberinto[x][y]
    nuevo_valor = teletransportes[valor]
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if laberinto[i][j] == nuevo_valor:
                return (i, j)
    return (x, y)  # Si no encuentra, se queda en el lugar

# Acertijo al llegar a celda acerjito
def acertijo():
    pregunta = "¿Cuál es la capital de Francia?"
    respuesta_correcta = "paris"
    respuesta = simpledialog.askstring("Acertijo", pregunta)
    return respuesta is not None and respuesta.lower() == respuesta_correcta

# Mostrar el camino que se uso
def mostrar_camino(camino):
    ventana = tk.Tk()
    ventana.title("Laberinto Resuelto")
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if (i, j) == entrada:
                color = "green"
            elif (i, j) == salida:
                color = "red"
            elif (i, j) in camino:
                color = "yellow"
            elif laberinto[i][j] == 1:
                color = "black"
            else:
                color = "white"
            celda = tk.Label(ventana, bg=color, width=4, height=2, borderwidth=1, relief="solid")
            celda.grid(row=i, column=j)
    ventana.mainloop()

# GUI para iniciar la solución del laberinto
def iniciar_gui():
    ventana_principal = tk.Tk()
    ventana_principal.title("Laberinto Misterioso")
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            if laberinto[i][j] == 1:
                color = "black"
            elif laberinto[i][j] == 0:
                color = "white"
            elif laberinto[i][j] == 2:
                color = "red"
            elif laberinto[i][j] == 3 or laberinto[i][j] == 4:
                color = "blue"
            elif laberinto[i][j] == 111:
                color = "orange"
            celda = tk.Label(ventana_principal, bg=color, width=4, height=2, borderwidth=1, relief="solid")
            celda.grid(row=i, column=j)
    boton_resolver = tk.Button(ventana_principal, text="Resolver Laberinto", command=resolver_laberinto)
    boton_resolver.grid(row=len(laberinto), column=0, columnspan=len(laberinto[0]))
    ventana_principal.mainloop()

# Iniciar la GUI principal
if __name__ == "__main__":
    iniciar_gui()
