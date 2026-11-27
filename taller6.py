# random se usa en la Parte 2 para lanzar la moneda y permutar a los amigos
import random


def crear_grafo(n, m):

    # Creamos la lista principal del grafo
    grafo = []

    # Creamos una lista vacía para cada amigo
    for i in range(n + 1):
        grafo.append([])

    # Leemos los conflictos
    for i in range(m):

        # Leemos los dos amigos que tienen un conflicto
        u, v = map(int, input().split())

        # Agregamos el conflicto en ambos sentidos
        grafo[u].append(v)
        grafo[v].append(u)

    return grafo


# VORAZ-REUNIONES
# Complejidad: O(n + m). Cada amigo se visita una vez y, sumando todos,
# se recorren 2m vecinos (cada arista aparece dos veces en las listas de
# adyacencia), cada uno consultado en O(1) gracias al arreglo reunion.
#
# El parámetro opcional "orden" permite recorrer a los amigos
# en otro orden (se usará en la Parte 2.3 con RANDOMIZE-IN-PLACE).
# Si no se pasa, se recorren 1, 2, ..., n como en el pseudocódigo.
def voraz_reuniones(grafo, orden=None):

    # Número de amigos
    n = len(grafo) - 1

    # Orden por defecto: 1, 2, ..., n
    if orden is None:
        orden = range(1, n + 1)

    # Guardamos los amigos de cada reunión
    A = []
    B = []

    # Guarda la reunión de cada amigo:
    # None significa que todavía no está asignado
    reunion = [None] * (n + 1)

    # Recorremos los amigos en orden
    for v in orden:

        a = 0
        b = 0

        # Revisamos los enemigos del amigo v
        for vecino in grafo[v]:

            # Consultamos directamente dónde está el enemigo
            if reunion[vecino] == 'A':
                a += 1

            elif reunion[vecino] == 'B':
                b += 1

        # Asignamos al amigo a la reunión correspondiente
        if a > b:
            B.append(v)
            reunion[v] = 'B'
        else:
            A.append(v)
            reunion[v] = 'A'

    return A, B


# COSTO
# Calcula c(S): el número de conflictos (aristas) que quedan separados,
# es decir, aristas con un extremo en A y el otro en B.
# Recibe la reunión A; todos los demás amigos están en B.
# Sirve para cualquier algoritmo que devuelva (A, B).
# Complejidad: O(n + m), porque recorre todas las listas de adyacencia.
def costo(grafo, A):

    # Marcamos qué amigos están en A para consultarlo en O(1)
    en_A = [False] * len(grafo)
    for v in A:
        en_A[v] = True

    separados = 0

    # Revisamos cada conflicto (u, v)
    for u in range(1, len(grafo)):
        for v in grafo[u]:

            # La arista queda separada si sus extremos están en reuniones distintas
            if en_A[u] != en_A[v]:
                separados += 1

    # Cada arista aparece dos veces (en grafo[u] y en grafo[v]),
    # así que dividimos entre 2
    return separados // 2


# REUNIONES-AL-AZAR
# Complejidad: O(n). Cada amigo se visita una vez y lanzar la moneda
# y agregarlo a A o a B cuesta O(1). No se revisan los conflictos.
def reuniones_al_azar(grafo):

    # Número de amigos
    n = len(grafo) - 1

    # Guardamos los amigos de cada reunión
    A = []
    B = []

    # Recorremos los amigos en orden
    for v in range(1, n + 1):

        # Lanzamos la moneda: Random(0, 1) devuelve 0 o 1
        moneda = random.randint(0, 1)

        # Asignamos al amigo según el resultado de la moneda
        if moneda == 0:
            A.append(v)
        else:
            B.append(v)

    return A, B


# RANDOMIZE-IN-PLACE
# Permuta los elementos del arreglo en un orden aleatorio.
# Complejidad: O(n). Se recorre el arreglo una vez y cada
# intercambio cuesta O(1).
def randomize_in_place(arreglo):

    # Número de elementos del arreglo
    n = len(arreglo)

    # Recorremos cada posición del arreglo
    for i in range(n):

        # Escogemos una posición al azar entre i y n - 1
        j = random.randint(i, n - 1)

        # Intercambiamos los elementos de las posiciones i y j
        temporal = arreglo[i]
        arreglo[i] = arreglo[j]
        arreglo[j] = temporal


# EXPERIMENTO
# Ejecuta 1000 veces:
# (a) REUNIONES-AL-AZAR
# (b) VORAZ-REUNIONES después de permutar el orden de los amigos
#     con RANDOMIZE-IN-PLACE
# Para cada uno calcula el promedio y el mejor C.
def experimento(grafo, m, repeticiones):

    # Número de amigos
    n = len(grafo) - 1

    # (a) REUNIONES-AL-AZAR

    # Guardamos la suma de los costos y el mejor costo encontrado
    suma_azar = 0
    mejor_azar = 0

    # Repetimos el algoritmo aleatorizado
    for i in range(repeticiones):

        # Ejecutamos el algoritmo y calculamos su costo
        A_azar, B_azar = reuniones_al_azar(grafo)
        C_azar = costo(grafo, A_azar)

        # Sumamos el costo para el promedio
        suma_azar += C_azar

        # Actualizamos el mejor costo si este es mayor
        if C_azar > mejor_azar:
            mejor_azar = C_azar

    # (b) VORAZ-REUNIONES con orden permutado

    # Guardamos la suma de los costos y el mejor costo encontrado
    suma_voraz = 0
    mejor_voraz = 0

    # Repetimos el algoritmo voraz
    for i in range(repeticiones):

        # Creamos la lista de amigos 1, 2, ..., n
        orden = []
        for v in range(1, n + 1):
            orden.append(v)

        # Permutamos el orden de los amigos
        randomize_in_place(orden)

        # Ejecutamos el voraz con el nuevo orden y calculamos su costo
        A_voraz, B_voraz = voraz_reuniones(grafo, orden)
        C_voraz = costo(grafo, A_voraz)

        # Sumamos el costo para el promedio
        suma_voraz += C_voraz

        # Actualizamos el mejor costo si este es mayor
        if C_voraz > mejor_voraz:
            mejor_voraz = C_voraz

    # Calculamos los promedios
    promedio_azar = suma_azar / repeticiones
    promedio_voraz = suma_voraz / repeticiones

    # Valor esperado teórico: E[C] = |E| / 2
    esperado = m / 2

    # Mostramos los resultados
    print()
    print("Experimento con", repeticiones, "ejecuciones")
    print("E[C] teórico:", esperado)
    print("(a) Al azar        - promedio:", promedio_azar, "- mejor:", mejor_azar)
    print("(b) Voraz permutado - promedio:", promedio_voraz, "- mejor:", mejor_voraz)


# PROGRAMA PRINCIPAL

# input() lee la primera línea
# .split() separa los valores de la primera línea (son dos)
# map(int, ...) convierte esos textos en números enteros
# n, m = guarda el primer número en n y el segundo en m
n, m = map(int, input().split())

# Construimos el grafo leyendo los m conflictos
grafo = crear_grafo(n, m)

# Ejecutamos el algoritmo voraz
A, B = voraz_reuniones(grafo)

# Calculamos el número de conflictos separados
C = costo(grafo, A)

# Formato de salida: reunión A, reunión B y conflictos separados
print(*A)
print(*B)
print(C)

# Ejecutamos el experimento de la Parte 2 con 1000 repeticiones
experimento(grafo, m, 1000)
