"""Persistencia y consulta de estadisticas agregadas."""


def cargar_estadisticas():
    """Carga las estadisticas acumuladas desde el archivo JSON."""
    return {}


def guardar_estadisticas(estadisticas):
    """Persiste las estadisticas en el archivo JSON."""
    pass


def actualizar_por_ingreso(estadisticas, fecha):
    """Incrementa ingresos del dia al registrar un ingreso."""
    pass


def actualizar_por_egreso(estadisticas, fecha, horas):
    """Actualiza egresos y horas por fecha, mes y dia de semana."""
    pass


def calcular_porcentaje_ocupacion(ocupacion, espacios):
    """Calcula el porcentaje de espacios ocupados sobre el total."""
    total = len(espacios)
    if total == 0:
        return 0.0
    ocupados = len(ocupacion)
    return ocupados * 100 / total


def calcular_promedio(total_horas, cantidad_egresos):
    """Calcula el tiempo promedio de permanencia."""
    if cantidad_egresos == 0:
        return None
    return total_horas / cantidad_egresos
