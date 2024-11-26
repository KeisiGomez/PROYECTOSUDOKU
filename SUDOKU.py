import time
import matplotlib
matplotlib.use("Agg")  # Usar backend para guardar imágenes
import matplotlib.pyplot as plt
from PIL import Image  # Para crear el GIF

# Lista para almacenar las rutas de las imágenes
cuadros_gif = []

# Función para encontrar celdas vacías en el tablero y ordenar por cantidad de opciones válidas
def encontrar_vacio_menor_opciones(tablero):
    vacios = []
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                opciones = sum(1 for num in range(1, 10) if es_valido(tablero, num, (i, j)))
                vacios.append((opciones, i, j))
    vacios.sort()
    return vacios[0][1:] if vacios else None

# Función para verificar si un número es válido en una posición específica
def es_valido(tablero, num, pos):
    fila, col = pos
    if num in tablero[fila]: return False
    if num in [tablero[i][col] for i in range(9)]: return False
    inicio_fila, inicio_col = (fila // 3) * 3, (col // 3) * 3
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_col, inicio_col + 3):
            if tablero[i][j] == num: return False
    return True

# Función para graficar el tablero y guardar cada paso
def graficar_tablero_y_guardar(tablero, proceso, intento=None, error=False):
    plt.clf()  # Limpia la figura antes de redibujar
    plt.title(f"Proceso {proceso}", fontsize=16, color="green" if not error else "red")
    
    for i in range(10):
        lw = 2 if i % 3 == 0 else 0.5
        plt.plot([i, i], [0, 9], color="black", linewidth=lw)
        plt.plot([0, 9], [i, i], color="black", linewidth=lw)

    for i in range(9):
        for j in range(9):
            if tablero[i][j] != 0:
                color = "black"  # Números originales en negro
                if intento and (i, j) == intento and error:
                    color = "red"  # Marcar intentos erróneos en rojo
                elif intento and (i, j) == intento:
                    color = "blue"  # Números colocados por el algoritmo en azul
                plt.text(j + 0.5, 8.5 - i, str(tablero[i][j]), fontsize=16, ha='center', va='center', color=color)

    plt.axis("off")
    
    # Guardar la imagen del proceso
    filename = f"sudoku_proceso_{proceso}.png"
    plt.savefig(filename)
    cuadros_gif.append(filename)  # Agregar la imagen a la lista

# Algoritmo de backtracking para resolver el Sudoku y graficar cada paso
def resolver_sudoku_paso_a_paso(tablero, proceso=1):
    vacio = encontrar_vacio_menor_opciones(tablero)
    if not vacio:
        graficar_tablero_y_guardar(tablero, proceso)
        return True  # Sudoku resuelto
    fila, col = vacio

    for num in range(1, 10):
        if es_valido(tablero, num, (fila, col)):
            tablero[fila][col] = num
            graficar_tablero_y_guardar(tablero, proceso, intento=(fila, col))  # Mostrar tablero en tiempo real
            if resolver_sudoku_paso_a_paso(tablero, proceso + 1):
                return True
            tablero[fila][col] = 0  # Deshacer asignación
        else:
            # Mostrar intento erróneo
            graficar_tablero_y_guardar(tablero, proceso, intento=(fila, col), error=True)
    return False

# Función para crear el GIF
def crear_gif(cuadros, nombre_gif="sudoku.gif"):
    imagenes = [Image.open(cuadro) for cuadro in cuadros]
    imagenes[0].save(
        nombre_gif,
        save_all=True,
        append_images=imagenes[1:],
        duration=500,  # Duración entre cuadros en milisegundos
        loop=0  # Bucle infinito
    )

# Tablero de ejemplo
tablero = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Configurar visualización interactiva
print("Resolviendo Sudoku paso a paso:")
inicio = time.time()
resolver_sudoku_paso_a_paso(tablero)
fin = time.time()

# Crear el GIF
crear_gif(cuadros_gif)

print(f"\nTiempo de ejecución: {fin - inicio:.4f} segundos")
print("GIF generado: sudoku.gif")

