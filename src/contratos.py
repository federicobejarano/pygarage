"""Contratos de datos y constantes globales del sistema."""

# Estructura esperada para cada espacio:
# {"codigo": "P1-E01", "piso": 1, "numero": 1}
# La lista completa de espacios se guarda en memoria como:
# espacios = [espacio_1, espacio_2, ...]

# Estructura esperada para clientes registrados:
# clientes = {
#     "12345678": {"nombre": "Juan Perez", "total_horas": 15}
# }

# Estructura esperada para la ocupacion actual:
# ocupacion = {
#     "P1-E01": {"dni": "12345678", "fecha_hora_ingreso": "2026-07-08 09:15:00"}
# }
# Si un codigo de espacio no aparece en ocupacion, se considera disponible.

# Estructura esperada para una fila de movimiento:
# {
#     "fecha_hora": "2026-07-08 09:15:00",
#     "codigo_espacio": "P1-E01",
#     "dni": "12345678",
#     "accion": "INGRESO",
# }

TARIFA_POR_HORA = 1000
UMBRAL_HORAS_DESCUENTO = 10
PORCENTAJE_DESCUENTO = 10

FORMATO_FECHA_HORA = "%Y-%m-%d %H:%M:%S"
FORMATO_FECHA = "%Y-%m-%d"
FORMATO_MES = "%Y-%m"

RUTA_ESPACIOS = "data/espacios.csv"
RUTA_MOVIMIENTOS = "data/movimientos.csv"
RUTA_CLIENTES = "data/clientes.json"
RUTA_ESTADISTICAS = "data/estadisticas.json"

ACCION_INGRESO = "INGRESO"
ACCION_EGRESO = "EGRESO"

CAMPOS_ESPACIO = ["codigo", "piso", "numero"]
CAMPOS_MOVIMIENTO = ["fecha_hora", "codigo_espacio", "dni", "accion"]
CAMPOS_CLIENTE = ["nombre", "total_horas"]

DIAS_SEMANA = {
    0: "lunes",
    1: "martes",
    2: "miercoles",
    3: "jueves",
    4: "viernes",
    5: "sabado",
    6: "domingo",
}
