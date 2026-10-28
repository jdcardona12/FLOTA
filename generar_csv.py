# -*- coding: utf-8 -*-
"""Genera datos/paquetes.csv con 200 paquetes de prueba (semilla fija)."""
import csv
import os
import random

random.seed(42)
CARPETA = os.path.dirname(os.path.abspath(__file__))

barrios = ["Centro", "La Castellana", "El Salado", "San Simon", "Tuerto",
           "Los Arrayanes", "Bosques del Rio", "Villa Restrepo", "La Francia",
           "Primera de Mayo", "Comuna 1", "Comuna 5", "La Toscana", "Alto Bonito"]

LAT, LON = 4.4393, -75.2322   # centro aproximado de Ibague

# tipo: cantidad, rango de peso (kg), medidas (alto, ancho, profundidad) en cm
config = {
    "sobre":   (60, (0.2, 0.5),  (2, 30, 20)),
    "pequeno": (70, (0.5, 2.0),  (10, 20, 15)),
    "mediano": (50, (2.0, 6.0),  (20, 40, 30)),
    "grande":  (20, (6.0, 15.0), (30, 50, 40)),
}

paquetes = []
medianos_largos = 0
for tipo, (cantidad, (pmin, pmax), (alto, ancho, prof)) in config.items():
    for _ in range(cantidad):
        a = ancho
        if tipo == "mediano" and medianos_largos < 20:
            a = 55                      # 20 medianos largos: no caben en moto
            medianos_largos += 1
        paquetes.append([
            0, tipo, round(random.uniform(pmin, pmax), 2), alto, a, prof,
            f"Cra. {random.randint(1, 15)} #{random.randint(1, 140)}-{random.randint(1, 99)}",
            random.choice(barrios),
            round(LAT + random.uniform(-0.015, 0.015), 6),
            round(LON + random.uniform(-0.015, 0.015), 6)])

random.shuffle(paquetes)
for i, p in enumerate(paquetes, 1):
    p[0] = i

with open(os.path.join(CARPETA, "datos", "paquetes.csv"), "w",
          encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id_paquete", "tipo_paquete", "peso_kg", "alto_cm", "ancho_cm",
                "profundidad_cm", "direccion", "barrio", "latitud", "longitud"])
    w.writerows(paquetes)
print(f"CSV generado con {len(paquetes)} paquetes")
