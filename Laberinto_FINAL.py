import random
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import deque
import time

# Matriz del laberinto aleatoria con ruta asegurada y múltiples caminos

def generar_laberinto(tamano=15):
    laberinto = [[random.choice([0, 1]) for _ in range(tamano)] for _ in range(tamano)]
    # Crear un camino asegurado desde la entrada hasta la salida
    x, y = 0, 0
    laberinto[x][y] = 0
    while (x, y) != (tamano - 1, tamano - 1):
        laberinto[x][y] = 0
        if x < tamano - 1 and (y == tamano - 1 or random.choice([True, False])):
            x += 1
        else:
            y += 1
    laberinto[tamano - 1][tamano - 1] = 2  # Salida
    # Añadir elementos especiales
    teletransporte_count = 0
    while teletransporte_count < 2:
        tx, ty = random.randint(0, tamano - 1), random.randint(0, tamano - 1)
        if laberinto[tx][ty] == 0:
            laberinto[tx][ty] = random.choice([3, 4])
            teletransporte_count += 1
    for _ in range(tamano // 2):
        tx, ty = random.randint(0, tamano - 1), random.randint(0, tamano - 1)
        if laberinto[tx][ty] == 0:
            laberinto[tx][ty] = 111
    return laberinto

laberinto = generar_laberinto()
entrada = (0, 0)
salida = (len(laberinto) - 1, len(laberinto) - 1)
teletransportes = {3: 4, 4: 3}

# Función para resolver el laberinto

def resolver_laberinto():
    camino = buscar_camino_programacion_dinamica()
    if camino:
        mostrar_camino_animado(camino)
    else:
        messagebox.showinfo("Laberinto", "No se encontró un camino hacia la salida. No siempre se puede ganar, ¡inténtalo de nuevo!")

# Función de programación dinámica para buscar el camino

def buscar_camino_programacion_dinamica():
    memo = {}

    def dp(x, y):
        if (x, y) in memo:
            return memo[(x, y)]
        if not es_valido(x, y):
            return None
        if (x, y) == salida:
            return [(x, y)]

        memo[(x, y)] = None  # Marcar como visitado temporalmente
        opciones = [
            (x + dx, y + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if es_valido(x + dx, y + dy)
        ]
        # Priorizar casillas especiales
        opciones.sort(key=lambda pos: laberinto[pos[0]][pos[1]] in teletransportes or laberinto[pos[0]][pos[1]] == 111, reverse=True)

        for nx, ny in opciones:
            if laberinto[x][y] in teletransportes:
                destino = encontrar_teletransporte(x, y)
                result = dp(destino[0], destino[1])
                if result:
                    memo[(x, y)] = [(x, y)] + result
                    break
            result = dp(nx, ny)
            if result:
                memo[(x, y)] = [(x, y)] + result
                break

        return memo[(x, y)]

    return dp(entrada[0], entrada[1])

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

# Acertijo al llegar a celda acertijo

def acertijo():
    preguntas = [
        ("¿Cuál es la capital de Francia?", "paris"),
        ("¿Cuánto es 2 + 2?", "4"),
        ("Cuántos meses tiene un año?", "12"),
        ("¿Qué color se forma cuando se combina el rojo y el amarillo?", "naranja"),
        ("¿Qué idioma se habla en Australia?", "ingles"),
    ]
    pregunta, respuesta_correcta = random.choice(preguntas)
    respuesta = simpledialog.askstring("Acertijo", pregunta)
    return respuesta is not None and respuesta.lower() == respuesta_correcta

# Mostrar el camino animado que se usó

def mostrar_camino_animado(camino):
    if not camino:
        return
    for (x, y) in camino:
        if laberinto[x][y] == 111:
            if not acertijo():
                messagebox.showinfo("Acertijo incorrecto", "No puedes avanzar hasta responder correctamente el acertijo.")
                break
        if laberinto[x][y] in teletransportes:
            x, y = encontrar_teletransporte(x, y)
        canvas.itemconfig(celdas[x][y], fill="yellow")
        ventana_principal.update()
        time.sleep(0.05)  # Pausa para la animación

# GUI para iniciar la solución del laberinto

def iniciar_gui():
    global ventana_principal, celdas, canvas
    ventana_principal = tk.Tk()
    ventana_principal.title("Laberinto Misterioso")
    canvas = tk.Canvas(ventana_principal, width=600, height=600, bg="white")
    canvas.grid(row=0, column=0, columnspan=len(laberinto[0]))

    tamano_celda = 600 // len(laberinto)
    celdas = [[None for _ in range(len(laberinto[0]))] for _ in range(len(laberinto))]

    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            x1, y1 = j * tamano_celda, i * tamano_celda
            x2, y2 = x1 + tamano_celda, y1 + tamano_celda
            if laberinto[i][j] == 1:
                color = "black"  # Pared
            elif laberinto[i][j] == 0:
                color = "white"  # Camino
            elif laberinto[i][j] == 2:
                color = "red"  # Salida
            elif laberinto[i][j] == 3 or laberinto[i][j] == 4:
                color = "blue"  # Teletransporte
            elif laberinto[i][j] == 111:
                color = "orange"  # Acertijo
            celdas[i][j] = canvas.create_polygon(
                x1 + tamano_celda // 2, y1,
                x2, y1 + tamano_celda // 2,
                x1 + tamano_celda // 2, y2,
                x1, y1 + tamano_celda // 2,
                fill=color, outline="black"
            )

    leyenda = tk.Label(ventana_principal, text="Leyenda:\n- Negro: Pared\n- Blanco: Camino\n- Rojo: Salida\n- Azul: Teletransporte\n- Naranja: Acertijo", justify='left')
    leyenda.grid(row=2, column=0, columnspan=len(laberinto[0]), pady=5)

    boton_resolver = tk.Button(ventana_principal, text="Resolver Laberinto", command=lambda: mostrar_camino_animado(buscar_camino_programacion_dinamica()))
    boton_resolver.grid(row=1, column=0, columnspan=len(laberinto[0]), pady=10)
    ventana_principal.mainloop()

# Iniciar la GUI principal
if __name__ == "__main__":
    iniciar_gui()
