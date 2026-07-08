"""Calculos de negocio: permanencia, importe y descuentos."""

import math
from datetime import datetime

from src.contratos import FORMATO_FECHA_HORA


def calcular_permanencia_horas(fecha_hora_ingreso, fecha_hora_egreso):
    """Calcula horas a cobrar por hora o fraccion entre dos fechas/hora."""
    ingreso = datetime.strptime(fecha_hora_ingreso, FORMATO_FECHA_HORA)
    egreso = datetime.strptime(fecha_hora_egreso, FORMATO_FECHA_HORA)
    diferencia = egreso - ingreso
    minutos_totales = diferencia.total_seconds() / 60
    horas = math.ceil(minutos_totales / 60)
    if horas < 1:
        horas = 1
    return horas


def calcular_importe(horas_a_cobrar, tarifa_por_hora):
    """Calcula el importe multiplicando horas por la tarifa."""
    return horas_a_cobrar * tarifa_por_hora


def estado_descuento(total_horas, umbral_horas):
    """Determina el estado del beneficio de descuento segun horas acumuladas."""
    if total_horas >= umbral_horas:
        return "El cliente tiene descuento disponible."
    faltan = umbral_horas - total_horas
    return f"Al cliente le faltan {faltan} horas para acceder al descuento."


def aplicar_descuento(importe, porcentaje_descuento):
    """Aplica el porcentaje de descuento sobre el importe."""
    descuento = importe * porcentaje_descuento / 100
    return int(importe - descuento)
