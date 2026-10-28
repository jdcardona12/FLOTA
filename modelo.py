# -*- coding: utf-8 -*-
"""
modelo.py
Clases base: Paquete, Vehiculo y Bodega.
"""


class Paquete:
    def __init__(self, id_paquete, tipo, peso, alto, ancho, profundidad,
                 direccion, barrio, latitud, longitud):
        self.id_paquete = id_paquete
        self.tipo = tipo
        self.peso = peso                      # kg
        self.alto = alto                      # cm
        self.ancho = ancho
        self.profundidad = profundidad
        self.direccion = direccion
        self.barrio = barrio
        self.latitud = latitud
        self.longitud = longitud

        # Volumen en litros (cm3 / 1000)
        self.volumen = (alto * ancho * profundidad) / 1000.0
        # Medidas de menor a mayor: sirven para saber si "cabe" en el vehiculo
        self.medidas_ordenadas = sorted([alto, ancho, profundidad])

    def __repr__(self):
        return f"Paquete({self.id_paquete}, {self.tipo}, {self.peso} kg)"


class Vehiculo:
    # peso en kg, medidas en cm
    CAPACIDADES = {
        "moto":      {"peso": 15,  "largo": 50,  "ancho": 40,  "alto": 30},
        "turbo":     {"peso": 600, "largo": 300, "ancho": 150, "alto": 100},
        "van":       {"peso": 200, "largo": 200, "ancho": 100, "alto": 100},
        "camioneta": {"peso": 350, "largo": 150, "ancho": 100, "alto": 100},
    }

    def __init__(self, tipo, id_vehiculo):
        self.tipo = tipo
        self.id_vehiculo = id_vehiculo
        self.placa = f"{tipo.upper()}-{id_vehiculo:02d}"

        cap = self.CAPACIDADES[tipo]
        self.capacidad_peso = cap["peso"]
        # Solo se usa el 80% del volumen (no hay acomodo 3D)
        self.capacidad_volumen = cap["largo"] * cap["ancho"] * cap["alto"] / 1000.0 * 0.80
        self.medidas_ordenadas = sorted([cap["largo"], cap["ancho"], cap["alto"]])

        self.paquetes = []
        self.peso_actual = 0.0
        self.volumen_actual = 0.0

    def peso_libre(self):
        return self.capacidad_peso - self.peso_actual

    def volumen_libre(self):
        return self.capacidad_volumen - self.volumen_actual

    def cabe_el_paquete(self, p):
        """True si el paquete cabe por peso, volumen y medidas."""
        if p.peso > self.peso_libre() + 1e-9:
            return False
        if p.volumen > self.volumen_libre() + 1e-9:
            return False
        for mp, mv in zip(p.medidas_ordenadas, self.medidas_ordenadas):
            if mp > mv:
                return False
        return True

    def agregar_paquete(self, p):
        if not self.cabe_el_paquete(p):
            return False
        self.paquetes.append(p)
        self.peso_actual += p.peso
        self.volumen_actual += p.volumen
        return True

    def quitar_ultimo(self):
        """Deshace el ultimo agregar_paquete (lo usa el backtracking)."""
        p = self.paquetes.pop()
        self.peso_actual -= p.peso
        self.volumen_actual -= p.volumen
        return p


class Bodega:
    def __init__(self, nombre, direccion, latitud, longitud):
        self.nombre = nombre
        self.direccion = direccion
        self.latitud = latitud
        self.longitud = longitud
