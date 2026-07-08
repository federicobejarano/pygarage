"""Capa generica de acceso a archivos CSV y JSON."""

import csv
import json
import os

from src.contratos import (
    RUTA_MOVIMIENTOS,
    RUTA_CLIENTES,
    RUTA_ESTADISTICAS,
    CAMPOS_MOVIMIENTO,
)



def leer_csv(ruta):
    """Lee un archivo CSV y devuelve una lista de diccionarios."""
    filas = []
    try:
        with open(ruta, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                filas.append(fila)
    except FileNotFoundError:
        print(f"Error: no se encontro el archivo{ruta}.")
    return filas


def agregar_linea_csv(ruta, fila):
    """Agrega una linea al final de un archivo CSV."""
    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(fila.keys()))
        escritor.writerow(fila)


def leer_json(ruta):
    """Lee un archivo JSON y devuelve un diccionario."""
    try:
        with open(ruta, encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print(f"Error: el archivo{ruta} esta danado o tiene un formato invalido.")
        return {}


def guardar_json(ruta, datos):
    """Guarda un diccionario en un archivo JSON."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)


def asegurar_archivos_iniciales():
    """Crea archivos de datos faltantes con estructura inicial valida."""
    if not os.path.exists(RUTA_CLIENTES):
        guardar_json(RUTA_CLIENTES, {})

    if not os.path.exists(RUTA_ESTADISTICAS):
        estadisticas_vacias = {
            "por_fecha": {},
            "por_mes": {},
            "por_dia_semana": {},
        }
        guardar_json(RUTA_ESTADISTICAS, estadisticas_vacias)

    if not os.path.exists(RUTA_MOVIMIENTOS):
        with open(RUTA_MOVIMIENTOS, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_MOVIMIENTO)
            escritor.writeheader()
