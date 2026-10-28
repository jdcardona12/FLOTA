# -*- coding: utf-8 -*-
"""
grafo.py
ALGORITMO 3: Dijkstra sobre un grafo.
Sin mapas ni internet: los nodos son la bodega y los paquetes. Cada nodo se
conecta solo con sus K vecinos mas cercanos (como si fueran las calles).
Dijkstra calcula la distancia minima entre cualquier par de nodos.
"""

import heapq
import math

K_VECINOS = 8


def distancia_recta(a, b):
    """Distancia en metros entre dos (lat, lon) - formula de haversine."""
    R = 6371000
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(h))


def construir_grafo(puntos, k=K_VECINOS):
    """Lista de adyacencia: grafo[i] = [(vecino, peso_metros), ...]"""
    n = len(puntos)
    grafo = [[] for _ in range(n)]
    for i in range(n):
        dists = sorted((distancia_recta(puntos[i], puntos[j]), j)
                       for j in range(n) if j != i)
        for d, j in dists[:k]:
            grafo[i].append((j, d))
            grafo[j].append((i, d))         # las calles van en los dos sentidos
    return grafo


def dijkstra(grafo, origen):
    """Distancia minima desde 'origen' a todos los nodos."""
    dist = [math.inf] * len(grafo)
    dist[origen] = 0.0
    cola = [(0.0, origen)]                  # cola de prioridad (min-heap)
    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:
            continue                        # entrada vieja, se ignora
        for v, w in grafo[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(cola, (dist[v], v))
    return dist


def matriz_distancias(puntos):
    """Matriz n x n con la distancia minima entre todos los pares (Dijkstra)."""
    grafo = construir_grafo(puntos)
    matriz = [dijkstra(grafo, i) for i in range(len(puntos))]
    # Por si el grafo quedara desconectado, se usa la distancia recta
    for i in range(len(puntos)):
        for j in range(len(puntos)):
            if matriz[i][j] == math.inf:
                matriz[i][j] = distancia_recta(puntos[i], puntos[j])
    return matriz
