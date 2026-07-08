from datetime import datetime

from src.contratos import (
    ACCION_INGRESO,
    FORMATO_FECHA_HORA,
    FORMATO_FECHA,
)
from src.validaciones import validar_dni, validar_nombre, validar_codigo_espacio
from src.espacios import listar_disponibles, sugerir_espacio
from src.clientes import buscar_cliente, registrar_cliente
from src.movimientos import registrar_movimiento
from src.estadisticas import actualizar_por_ingreso

"""Presentacion por consola y flujos de operaciones."""


def mostrar_menu_principal():
    """Muestra el menu principal numerado con 7 opciones."""
    pass


def mostrar_menu_estadisticas():
    """Muestra el submenu de estadisticas con 4 opciones."""
    pass


def leer_opcion(mensaje, minimo, maximo):
    """Lee y valida una opcion numerica del usuario con reintento."""
    return 0


def formatear_espacios_disponibles(disponibles_por_piso, libres, ocupados, total):
    """Formatea el listado de espacios disponibles agrupados por piso."""
    return ""


def pausar_para_continuar():
    """Muestra pausa para volver al menu principal."""
    pass


def finalizar_programa():
    """Muestra mensaje de cierre y termina la ejecucion."""
    pass


def flujo_registrar_cliente(clientes):
    """Flujo completo para registrar un cliente nuevo."""
    pass


def flujo_consultar_cliente(clientes):
    """Flujo completo para consultar un cliente registrado."""
    pass


def flujo_consultar_espacios(espacios, ocupacion):
    """Flujo completo para consultar espacios disponibles."""
    pass


def flujo_consultar_estadisticas(estadisticas, espacios, ocupacion):
    """Flujo completo del submenu de estadisticas."""
    pass


def registrar_ingreso(espacios, clientes, ocupacion, estadisticas):
    """Flujo completo para registrar el ingreso de un vehiculo."""
    return ocupacion


def registrar_egreso(espacios, clientes, ocupacion, estadisticas):
    """Flujo completo para registrar el egreso de un vehiculo."""
    return ocupacion
