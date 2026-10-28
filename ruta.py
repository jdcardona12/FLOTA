# -*- coding: utf-8 -*-
"""
ruta.py
ALGORITMO 4: Vecino mas cercano (voraz / greedy) para armar la ruta.
ALGORITMO 5: 2-opt para mejorarla (busqueda local).
La ruta siempre sale de la bodega (indice 0) y vuelve a ella.
"""


def costo_ruta(ruta, d):
    return sum(d[ruta[i]][ruta[i + 1]] for i in range(len(ruta) - 1))


def vecino_mas_cercano(paradas, d, bodega=0):
    """Desde donde estoy, voy siempre a la parada no visitada mas cercana."""
    por_visitar = set(paradas)
    ruta = [bodega]
    actual = bodega
    while por_visitar:
        sig = min(por_visitar, key=lambda x: d[actual][x])
        ruta.append(sig)
        por_visitar.remove(sig)
        actual = sig
    ruta.append(bodega)
    return ruta


def dos_opt(ruta, d):
    """
    Toma dos aristas (a-b) y (c-e); si invertir el tramo b..c las acorta,
    lo hace. Repite hasta que ya no hay mejoras.
    """
    ruta = list(ruta)
    mejoro = True
    while mejoro:
        mejoro = False
        for i in range(1, len(ruta) - 2):
            for j in range(i + 1, len(ruta) - 1):
                a, b = ruta[i - 1], ruta[i]
                c, e = ruta[j], ruta[j + 1]
                antes = d[a][b] + d[c][e]
                despues = d[a][c] + d[b][e]
                if despues < antes - 1e-9:
                    ruta[i:j + 1] = reversed(ruta[i:j + 1])
                    mejoro = True
    return ruta


def calcular_ruta(paradas, d):
    """Devuelve (ruta_final, km_vecino, km_2opt)."""
    if not paradas:
        return [0, 0], 0.0, 0.0
    inicial = vecino_mas_cercano(paradas, d)
    final = dos_opt(inicial, d)
    return final, costo_ruta(inicial, d) / 1000.0, costo_ruta(final, d) / 1000.0
