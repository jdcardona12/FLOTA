# -*- coding: utf-8 -*-
"""
main.py - Sistema de ruteo de entregas (Ibague). Todo por terminal.

Flujo:
  1. Lee el CSV de paquetes
  2. Crea la flota que elija el usuario
  3. Mochila 0/1 -> reparte paquetes entre vehiculos
  4. Backtracking -> intenta colocar los sobrantes
  5. Dijkstra -> matriz de distancias
  6. Vecino mas cercano + 2-opt -> ruta de cada vehiculo
  7. Imprime resultados

Uso:  python main.py            (pregunta cuantos vehiculos)
      python main.py 2 1 1 1    (motos turbos vans camionetas)
"""

import csv
import os
import sys

from modelo import Paquete, Vehiculo, Bodega
from asignacion import asignar_paquetes
from recursividad import reasignar_sobrantes
from grafo import matriz_distancias
from ruta import calcular_ruta

# Ruta al CSV relativa a ESTE archivo: funciona sin importar desde donde se ejecute
CARPETA = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA, "datos", "paquetes.csv")

BODEGA = Bodega("Servientrega Ibague CIL El Salado", "Cra. 8 #122-27",
                4.4670, -75.2220)


def leer_paquetes(ruta_csv):
    paquetes = []
    with open(ruta_csv, "r", encoding="utf-8-sig", newline="") as f:
        for fila in csv.DictReader(f):
            paquetes.append(Paquete(
                int(fila["id_paquete"]), fila["tipo_paquete"],
                float(fila["peso_kg"]), float(fila["alto_cm"]),
                float(fila["ancho_cm"]), float(fila["profundidad_cm"]),
                fila["direccion"], fila["barrio"],
                float(fila["latitud"]), float(fila["longitud"])))
    return paquetes


def crear_flota(cantidades):
    """cantidades: dict {'moto': 2, 'turbo': 1, ...}"""
    flota = []
    for tipo in ("moto", "turbo", "van", "camioneta"):
        for _ in range(cantidades[tipo]):
            flota.append(Vehiculo(tipo, len(flota) + 1))
    return flota


def pedir_flota():
    if len(sys.argv) == 5:
        try:
            m, t, v, c = (int(x) for x in sys.argv[1:5])
            return {"moto": m, "turbo": t, "van": v, "camioneta": c}
        except ValueError:
            pass
    print("Cuantos vehiculos de cada tipo? (Enter = 1)")
    cant = {}
    for tipo in ("moto", "turbo", "van", "camioneta"):
        txt = input(f"  {tipo}: ").strip()
        cant[tipo] = int(txt) if txt.isdigit() else 1
    return cant


def linea(c="=", n=70):
    print(c * n)


def main():
    print("=== SISTEMA DE RUTEO DE FLOTA - IBAGUE ===")
    cant = pedir_flota()
    if sum(cant.values()) == 0:
        print("Necesitas al menos un vehiculo.")
        return

    paquetes = leer_paquetes(RUTA_CSV)
    flota = crear_flota(cant)

    # --- Paso 1: mochila 0/1 ---
    sobrantes = asignar_paquetes(paquetes, flota)
    tras_mochila = len(paquetes) - len(sobrantes)

    # --- Paso 2: backtracking con los sobrantes ---
    sin_asignar = reasignar_sobrantes(sobrantes, flota)
    por_backtracking = len(sobrantes) - len(sin_asignar)

    # --- Paso 3: Dijkstra (indice 0 = bodega) ---
    puntos = [(BODEGA.latitud, BODEGA.longitud)]
    indice = {}                                   # id_paquete -> indice en la matriz
    for v in flota:
        for p in v.paquetes:
            indice[p.id_paquete] = len(puntos)
            puntos.append((p.latitud, p.longitud))
    d = matriz_distancias(puntos)

    # --- Paso 4: rutas ---
    print()
    linea()
    print("RESULTADOS")
    linea()
    print(f"Paquetes totales:             {len(paquetes)}")
    print(f"Asignados por mochila:        {tras_mochila}")
    print(f"Asignados por backtracking:   {por_backtracking}")
    print(f"Sin asignar:                  {len(sin_asignar)}")

    km_total = 0.0
    sin_uso = []
    nombre_bodega = f"BODEGA ({BODEGA.direccion}, Ibague)"
    for v in flota:
        if not v.paquetes:
            sin_uso.append(v.placa)
            continue

        print()
        linea("-")
        print(f"{v.placa}  |  paquetes: {len(v.paquetes)}  |  "
              f"peso: {v.peso_actual:.1f}/{v.capacidad_peso} kg  |  "
              f"volumen: {v.volumen_actual:.0f}/{v.capacidad_volumen:.0f} L")

        por_id = {indice[p.id_paquete]: p for p in v.paquetes}
        ruta, km_nn, km_2opt = calcular_ruta(list(por_id), d)
        km_total += km_2opt
        mejora = (km_nn - km_2opt) / km_nn * 100 if km_nn else 0
        print(f"  Distancia vecino mas cercano: {km_nn:.2f} km")
        print(f"  Distancia con 2-opt:          {km_2opt:.2f} km "
              f"(mejora {mejora:.1f}%)")
        print(f"  Sale de la bodega con {v.peso_actual:.2f} kg de carga")
        print("  Tramos (de -> a | km | peso que entrega | carga a bordo):")

        a_bordo = v.peso_actual
        for k in range(1, len(ruta)):
            ant, sig = ruta[k - 1], ruta[k]
            km = d[ant][sig] / 1000.0
            origen = nombre_bodega if ant == 0 else por_id[ant].direccion
            if sig == 0:
                destino = "BODEGA (regreso)"
                entrega = ""
            else:
                p = por_id[sig]
                destino = f"{p.direccion}, {p.barrio}"
                a_bordo -= p.peso
                entrega = f"entrega {p.peso:5.2f} kg (paq. {p.id_paquete})"
            print(f"   {k:3d}. {origen} -> {destino} | {km:.2f} km"
                  f"{' | ' + entrega if entrega else ''}"
                  f" | a bordo {max(a_bordo, 0):.2f} kg")

    if sin_uso:
        print()
        linea("-")
        print(f"Vehiculos sin paquetes ({len(sin_uso)}): {', '.join(sin_uso)}")

    if sin_asignar:
        print()
        linea("-")
        print("PAQUETES SIN ASIGNAR (no caben en la flota elegida):")
        for p in sin_asignar:
            print(f"  - {p.id_paquete} ({p.tipo}, {p.peso} kg) {p.direccion}, {p.barrio}")

    print()
    linea()
    print(f"DISTANCIA TOTAL DE LA FLOTA: {km_total:.2f} km")
    linea()


if __name__ == "__main__":
    main()
