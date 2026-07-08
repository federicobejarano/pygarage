from datetime import datetime

from src.archivos import leer_json, guardar_json
from src.contratos import (
    RUTA_ESTADISTICAS,
    FORMATO_FECHA,
    FORMATO_MES,
    DIAS_SEMANA,
)


def cargar_estadisticas():
    """Carga las estadisticas acumuladas desde el archivo JSON."""
    estadisticas = leer_json(RUTA_ESTADISTICAS)
    estadisticas.setdefault("por_fecha", {})
    estadisticas.setdefault("por_mes", {})
    estadisticas.setdefault("por_dia_semana", {})
    return estadisticas


def guardar_estadisticas(estadisticas):
    """Persiste las estadisticas en el archivo JSON."""
    guardar_json(RUTA_ESTADISTICAS, estadisticas)


def actualizar_por_ingreso(estadisticas, fecha):
    """Incrementa ingresos del dia al registrar un ingreso."""
    por_fecha = estadisticas["por_fecha"]
    if fecha not in por_fecha:
        por_fecha[fecha] = {"ingresos": 0, "egresos": 0, "total_horas": 0}
    por_fecha[fecha]["ingresos"] += 1
    guardar_estadisticas(estadisticas)


def actualizar_por_egreso(estadisticas, fecha, horas):
    """Actualiza egresos y horas por fecha, mes y dia de semana."""
    fecha_obj = datetime.strptime(fecha, FORMATO_FECHA)
    mes = fecha_obj.strftime(FORMATO_MES)
    dia_semana = DIAS_SEMANA[fecha_obj.weekday()]

    por_fecha = estadisticas["por_fecha"]
    if fecha not in por_fecha:
        por_fecha[fecha] = {"ingresos": 0, "egresos": 0, "total_horas": 0}
    por_fecha[fecha]["egresos"] += 1
    por_fecha[fecha]["total_horas"] += horas

    por_mes = estadisticas["por_mes"]
    if mes not in por_mes:
        por_mes[mes] = {"egresos": 0, "total_horas": 0}
    por_mes[mes]["egresos"] += 1
    por_mes[mes]["total_horas"] += horas

    por_dia = estadisticas["por_dia_semana"]
    if dia_semana not in por_dia:
        por_dia[dia_semana] = {"egresos": 0, "total_horas": 0}
    por_dia[dia_semana]["egresos"] += 1
    por_dia[dia_semana]["total_horas"] += horas

    guardar_estadisticas(estadisticas)


def calcular_porcentaje_ocupacion(ocupacion, espacios):
    """Calcula el porcentaje de espacios ocupados sobre el total."""
    return 0.0


def calcular_promedio(total_horas, cantidad_egresos):
    """Calcula el tiempo promedio de permanencia."""
    return None
