# Importa la biblioteca heapq, que proporciona una implementación de la cola de prioridad.
import heapq


def crear_mapa(filas, columnas):
    # Crea un mapa vacío de dimensiones especificadas por el usuario, con todas las celdas transitables (inicializadas a 0).
    return [[0 for _ in range(columnas)] for _ in range(filas)]


def imprimir_mapa(mapa, ruta=[], inicio=None, fin=None):
    # Imprime el mapa en la consola, con símbolos especiales para el inicio, fin, obstáculos y la ruta encontrada.
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if (i, j) == inicio:
                print("A", end=" ")  # Marca el punto de inicio con 'A'.
            elif (i, j) == fin:
                print("B", end=" ")  # Marca el punto de fin con 'B'.
            elif (i, j) in ruta:
                print("*", end=" ")  # Marca la ruta encontrada con '*'.
            elif mapa[i][j] == 0:
                print(".", end=" ")  # Marca las celdas transitables con '.'.
            elif mapa[i][j] == 1:
                # Marca los obstáculos permanentes con 'X'.
                print("X", end=" ")
            elif mapa[i][j] == 2:
                print("W", end=" ")  # Marca los obstáculos de agua con 'W'.
            elif mapa[i][j] == 3:
                print("T", end=" ")  # Marca los obstáculos temporales con 'T'.
        print()
    print()


def ingresar_coordenadas(mapa):
    # Permite al usuario ingresar coordenadas válidas para el mapa.
    while True:
        x = int(input("Ingrese la coordenada X: "))
        y = int(input("Ingrese la coordenada Y: "))
        # Verifica si las coordenadas son válidas y si el punto es transitable.
        if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]) and mapa[x][y] == 0:
            return x, y
        else:
            print("Coordenadas no válidas o punto no transitable. Intente de nuevo.")


def agregar_obstaculo(mapa, x, y, tipo=1):
    # Agrega un obstáculo de tipo especificado en el mapa.
    if 0 <= x < len(mapa) and 0 <= y < len(mapa[0]):
        mapa[x][y] = tipo


def heuristica(a, b):
    # Calcula la distancia de Manhattan entre dos puntos (a y b).
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def buscar_ruta(mapa, inicio, fin):
    # Implementa el algoritmo A* para encontrar la ruta más corta desde el inicio hasta el fin.
    filas, columnas = len(mapa), len(mapa[0])
    abierta = []  # Cola de prioridad para los nodos por explorar.
    # Agrega el nodo inicial a la cola con prioridad 0.
    heapq.heappush(abierta, (0, inicio))
    came_from = {}  # Diccionario para rastrear el camino desde cada nodo.
    # Diccionario para almacenar el costo de llegar a cada nodo.
    costo_hasta_aqui = {inicio: 0}
    # Diccionario para almacenar el costo estimado total desde cada nodo.
    costo_estimado = {inicio: heuristica(inicio, fin)}

    while abierta:
        # Extrae el nodo con la menor prioridad (costo estimado más bajo).
        _, actual = heapq.heappop(abierta)

        if actual == fin:
            # Si se llega al nodo final, reconstruye la ruta desde el fin hasta el inicio.
            ruta = []
            while actual in came_from:
                ruta.append(actual)
                actual = came_from[actual]
            ruta.append(inicio)
            # Devuelve la ruta en orden correcto (de inicio a fin).
            return ruta[::-1]

        x, y = actual
        # Explora los vecinos (arriba, abajo, izquierda, derecha) del nodo actual.
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            vecino = (x + dx, y + dy)
            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas and mapa[vecino[0]][vecino[1]] == 0:
                # Calcula el nuevo costo para el vecino.
                nuevo_costo = costo_hasta_aqui[actual] + 1
                if vecino not in costo_hasta_aqui or nuevo_costo < costo_hasta_aqui[vecino]:
                    costo_hasta_aqui[vecino] = nuevo_costo
                    # Calcula la prioridad para la cola.
                    prioridad = nuevo_costo + heuristica(vecino, fin)
                    # Agrega el vecino a la cola con la nueva prioridad.
                    heapq.heappush(abierta, (prioridad, vecino))
                    # Actualiza el diccionario de camino.
                    came_from[vecino] = actual

    return None  # Si no se encuentra una ruta, devuelve None.


def main():
    filas = int(input("Ingrese el número de filas del laberinto: "))
    columnas = int(input("Ingrese el número de columnas del laberinto: "))
    # Crea un mapa con las dimensiones especificadas por el usuario.
    mapa = crear_mapa(filas, columnas)
    imprimir_mapa(mapa)

    print("Ingrese las coordenadas del punto de inicio:")
    # Permite al usuario ingresar las coordenadas del punto de inicio.
    inicio = ingresar_coordenadas(mapa)

    print("Ingrese las coordenadas del punto de destino:")
    # Permite al usuario ingresar las coordenadas del punto de destino.
    fin = ingresar_coordenadas(mapa)

    print("Agregar obstáculos:")
    while True:
        # Permite al usuario ingresar las coordenadas para un obstáculo.
        x, y = ingresar_coordenadas(mapa)
        tipo = int(
            input("Ingrese el tipo de obstáculo (1: permanente, 2: agua, 3: temporal): "))
        agregar_obstaculo(mapa, x, y, tipo)  # Agrega el obstáculo al mapa.
        imprimir_mapa(mapa)
        continuar = input("¿Desea agregar otro obstáculo? (s/n): ")
        if continuar.lower() != 's':
            # Sale del bucle si el usuario no desea agregar más obstáculos.
            break

    # Busca la ruta más corta desde el inicio hasta el fin.
    ruta = buscar_ruta(mapa, inicio, fin)
    if ruta:
        print("Ruta más corta encontrada:")
        # Imprime el mapa con la ruta encontrada.
        imprimir_mapa(mapa, ruta, inicio, fin)
    else:
        # Informa si no se encuentra una ruta.
        print("No se encontró una ruta válida.")


if __name__ == "__main__":
    # Ejecuta la función principal si el script se ejecuta directamente.
    main()
