# -*- coding: utf-8 -*-
"""
recursividad.py
ALGORITMO 2: Backtracking (recursividad).
Intenta meter los paquetes que sobraron de la mochila en los huecos que
quedaron en los vehiculos. Para cada paquete prueba cada vehiculo; si mas
adelante no se puede, deshace (backtrack) y prueba otra opcion.
"""

LIMITE_LLAMADAS = 20000   # evita que el backtracking tarde demasiado


def reasignar_sobrantes(sobrantes, vehiculos):
    """Devuelve la lista de paquetes que NO se lograron colocar."""
    if not sobrantes:
        return []

    # Primero los mas pesados: son los mas dificiles de ubicar
    lista = sorted(sobrantes, key=lambda p: p.peso, reverse=True)
    n = len(lista)

    estado = {"llamadas": 0, "mejor": []}   # mejor = [(paquete, vehiculo), ...]
    actual = []

    def colocar(i):
        estado["llamadas"] += 1
        if estado["llamadas"] > LIMITE_LLAMADAS:
            return
        if len(estado["mejor"]) == n:       # ya se colocaron todos
            return
        # Poda: aunque coloque todos los que faltan no supera al mejor
        if len(actual) + (n - i) <= len(estado["mejor"]):
            return

        if i == n:                          # caso base
            estado["mejor"] = list(actual)
            return

        p = lista[i]
        # Opcion 1: ponerlo en cada vehiculo donde quepa
        for v in vehiculos:
            if v.agregar_paquete(p):
                actual.append((p, v))
                colocar(i + 1)              # llamada recursiva
                actual.pop()                # backtracking: deshacer
                v.quitar_ultimo()
        # Opcion 2: dejar este paquete sin asignar y seguir con los demas
        colocar(i + 1)

    colocar(0)

    # Aplicar la mejor solucion encontrada
    colocados = set()
    for p, v in estado["mejor"]:
        v.agregar_paquete(p)
        colocados.add(p.id_paquete)

    return [p for p in lista if p.id_paquete not in colocados]
