"""Punto de entrada del sistema de gestion de estacionamiento."""

from src.archivos import asegurar_archivos_iniciales, leer_csv
from src.clientes import cargar_clientes
from src.contratos import RUTA_MOVIMIENTOS
from src.espacios import cargar_espacios
from src.estadisticas import cargar_estadisticas
from src.menus import (
    finalizar_programa,
    flujo_consultar_cliente,
    flujo_consultar_espacios,
    flujo_consultar_estadisticas,
    flujo_registrar_cliente,
    leer_opcion,
    mostrar_menu_principal,
    registrar_egreso,
    registrar_ingreso,
)
from src.movimientos import reconstruir_ocupacion


def cargar_estado_inicial():
    """Carga los datos persistidos y reconstruye el estado en memoria."""
    asegurar_archivos_iniciales()
    espacios = cargar_espacios()
    clientes = cargar_clientes()
    movimientos = leer_csv(RUTA_MOVIMIENTOS)
    ocupacion = reconstruir_ocupacion(espacios, movimientos)
    estadisticas = cargar_estadisticas()
    return espacios, clientes, ocupacion, estadisticas


def despachar_opcion(opcion, espacios, clientes, ocupacion, estadisticas):
    """Ejecuta el flujo correspondiente a la opcion elegida."""
    if opcion == 1:
        return registrar_ingreso(espacios, clientes, ocupacion, estadisticas)
    if opcion == 2:
        return registrar_egreso(espacios, clientes, ocupacion, estadisticas)
    if opcion == 3:
        flujo_registrar_cliente(clientes)
    elif opcion == 4:
        flujo_consultar_cliente(clientes)
    elif opcion == 5:
        flujo_consultar_espacios(espacios, ocupacion)
    elif opcion == 6:
        flujo_consultar_estadisticas(estadisticas, espacios, ocupacion)
    return ocupacion


def main():
    """Inicializa el sistema y ejecuta el menu principal."""
    espacios, clientes, ocupacion, estadisticas = cargar_estado_inicial()

    opcion = 0
    while opcion != 7:
        mostrar_menu_principal()
        opcion = leer_opcion("Elija una opcion: ", 1, 7)

        if opcion == 7:
            finalizar_programa()
        else:
            ocupacion = despachar_opcion(
                opcion,
                espacios,
                clientes,
                ocupacion,
                estadisticas,
            )


if __name__ == "__main__":
    main()
