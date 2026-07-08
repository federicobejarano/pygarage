"""Gestion de clientes registrados."""

from src.archivos import leer_json, guardar_json
from src.contratos import RUTA_CLIENTES


def cargar_clientes():
    """Carga el diccionario de clientes desde el archivo JSON."""
    return leer_json(RUTA_CLIENTES)


def guardar_clientes(clientes):
    """Persiste el diccionario de clientes en el archivo JSON."""
    guardar_json(RUTA_CLIENTES, clientes)


def buscar_cliente(clientes, dni):
    """Busca un cliente registrado por DNI."""
    return clientes.get(dni)


def registrar_cliente(clientes, dni, nombre):
    """Registra un cliente nuevo con total_horas en cero."""
    if dni in clientes:
        return False
    clientes[dni] = {"nombre": nombre, "total_horas": 0}
    guardar_clientes(clientes)
    return True


def actualizar_horas(clientes, dni, horas):
    """Suma horas al total acumulado de un cliente registrado."""
    if dni in clientes:
        clientes[dni]["total_horas"] += horas
        guardar_clientes(clientes)