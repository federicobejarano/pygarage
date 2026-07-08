"""Bitacora de movimientos y reconstruccion de ocupacion."""

from src.archivos import agregar_linea_csv
from src.contratos import RUTA_MOVIMIENTOS, ACCION_INGRESO, ACCION_EGRESO


def registrar_movimiento(fecha_hora, codigo_espacio, dni, accion):
    """Agrega un movimiento INGRESO o EGRESO a la bitacora CSV."""
    fila = {
        "fecha_hora": fecha_hora,
        "codigo_espacio": codigo_espacio,
        "dni": dni,
        "accion": accion,
    }
    agregar_linea_csv(RUTA_MOVIMIENTOS, fila)


def reconstruir_ocupacion(espacios, movimientos):
    """Reconstruye la ocupacion actual a partir de la bitacora."""
    codigos_validos = []
    for espacio in espacios:
        codigos_validos.append(espacio["codigo"])

    ocupacion = {}
    for movimiento in movimientos:
        codigo = movimiento["codigo_espacio"]

        if codigo not in codigos_validos:
            continue

        if movimiento["accion"] == ACCION_INGRESO:
            ocupacion[codigo] = {
                "dni": movimiento["dni"],
                "fecha_hora_ingreso": movimiento["fecha_hora"],
            }
        elif movimiento["accion"] == ACCION_EGRESO:
            if codigo in ocupacion:
                del ocupacion[codigo]

    return ocupacion


def obtener_ingreso_activo(ocupacion, codigo_espacio):
    """Obtiene el ingreso activo de un espacio ocupado."""
    return ocupacion.get(codigo_espacio)