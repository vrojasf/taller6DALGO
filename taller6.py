# input() lee la primera línea
# .split() separa los valores de la primera lpinea (son dos)
# map(int, ...) convierte esos textos en números enteros
#n, m = guarda el primer número en n y el segundo en m
n, m = map(int, input().split())

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


#el parámetro opcional "orden" permite recorrer a los amigos
# en otro orden (se usará en la Parte 2.3 con RANDOMIZE-IN-PLACE).
# Si no se pasa, se recorren 1, 2, ..., n como en el pseudocódigo.
def voraz_reuniones(grafo, orden=None):

    # Número de amigos
    n = len(grafo) - 1

    # NUEVO: orden por defecto 1..n
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


#  COSTO
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


#PROGRAMA PRINCIPAL

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