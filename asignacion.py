# -*- coding: utf-8 -*-
"""
asignacion.py
ALGORITMO 1: Mochila 0/1 (programacion dinamica).
Para cada vehiculo elige el conjunto de paquetes que maximiza la CANTIDAD
de paquetes sin pasar la capacidad de peso.
"""

import math


def mochila_01(paquetes, capacidad_peso):
    """
    paquetes: lista de Paquete candidatos.
    Devuelve los indices (de esa lista) de los paquetes elegidos.

    dp[w] = maximo numero de paquetes que caben en un peso w.
    Pesos en decimas de kg (enteros) para poder usar la tabla.
    """
    n = len(paquetes)
    cap = int(capacidad_peso * 10)                         # decimas de kg
    pesos = [math.ceil(p.peso * 10) for p in paquetes]     # redondeo hacia arriba

    dp = [0] * (cap + 1)
    # tomado[i][w] = True si en el item i se mejoro dp[w] tomando el paquete i
    tomado = [bytearray(cap + 1) for _ in range(n)]

    for i in range(n):
        w_i = pesos[i]
        for w in range(cap, w_i - 1, -1):                  # de derecha a izquierda (0/1)
            if dp[w - w_i] + 1 > dp[w]:
                dp[w] = dp[w - w_i] + 1
                tomado[i][w] = 1

    # Reconstruir: recorremos los items de atras hacia adelante
    elegidos = []
    w = cap
    for i in range(n - 1, -1, -1):
        if tomado[i][w]:
            elegidos.append(i)
            w -= pesos[i]
    return elegidos


def asignar_paquetes(paquetes, vehiculos):
    """
    Recorre los vehiculos; a cada uno le aplica la mochila con los paquetes
    que aun no se han repartido y que le caben.
    Devuelve la lista de paquetes sobrantes.
    """
    pendientes = list(paquetes)

    for v in vehiculos:
        candidatos = [p for p in pendientes if v.cabe_el_paquete(p)]
        if not candidatos:
            continue

        elegidos = mochila_01(candidatos, v.peso_libre())

        for i in elegidos:
            p = candidatos[i]
            # agregar_paquete ademas revisa volumen y medidas.
            # Solo lo sacamos de pendientes si de verdad entro.
            if v.agregar_paquete(p):
                pendientes.remove(p)

    return pendientes
