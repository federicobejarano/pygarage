from datetime import datetime

from src.contratos import (
    ACCION_INGRESO,
    FORMATO_FECHA_HORA,
    FORMATO_FECHA,
    ACCION_EGRESO,
    TARIFA_POR_HORA,
    UMBRAL_HORAS_DESCUENTO,
    PORCENTAJE_DESCUENTO,
)
from src.calculos import (
    calcular_permanencia_horas,
    calcular_importe,
    aplicar_descuento,
)
from src.validaciones import validar_dni, validar_nombre, validar_codigo_espacio
from src.espacios import listar_disponibles, sugerir_espacio
from src.clientes import buscar_cliente, registrar_cliente, actualizar_horas
from src.movimientos import registrar_movimiento, obtener_ingreso_activo
from src.estadisticas import actualizar_por_ingreso, actualizar_por_egreso

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
    dni = input("Ingrese DNI del cliente o 0 para cancelar: ").strip()
    if dni == "0":
        return ocupacion
    while not validar_dni(dni):
        print("DNI invalido. Debe ingresar solo numeros (7 u 8 digitos).")
        dni = input("Ingrese DNI del cliente o 0 para cancelar: ").strip()
        if dni == "0":
            return ocupacion

    cliente = buscar_cliente(clientes, dni)
    if cliente is not None:
        print(f"Bienvenido/a{cliente['nombre']}.")
    else:
        respuesta = input("El cliente no esta registrado. Desea registrarlo? (s/n): ").strip().lower()
        if respuesta == "s":
            nombre = input("Ingrese el nombre del cliente: ").strip()
            while not validar_nombre(nombre):
                print("El nombre no puede estar vacio.")
                nombre = input("Ingrese el nombre del cliente: ").strip()
            registrar_cliente(clientes, dni, nombre)
            print(f"Cliente{nombre} registrado con exito.")
        else:
            print("El ingreso continuara como cliente no registrado.")

    sugerido = sugerir_espacio(espacios, ocupacion)
    if sugerido is None:
        print("No hay espacios disponibles en este momento.")
        return ocupacion

    print(f"Espacio sugerido:{sugerido}")
    respuesta = input("Acepta el espacio sugerido? (s/n): ").strip().lower()
    if respuesta == "s":
        codigo = sugerido
    else:
        disponibles = listar_disponibles(espacios, ocupacion)
        for piso in sorted(disponibles):
            print(f"Piso{piso}:{', '.join(disponibles[piso])}")
        codigo = input("Ingrese el codigo del espacio o 0 para cancelar: ").strip().upper()
        if codigo == "0":
            return ocupacion
        while not validar_codigo_espacio(codigo, espacios) or codigo in ocupacion:
            print("El espacio no existe o ya esta ocupado.")
            codigo = input("Ingrese el codigo del espacio o 0 para cancelar: ").strip().upper()
            if codigo == "0":
                return ocupacion

    ahora = datetime.now()
    fecha_hora = ahora.strftime(FORMATO_FECHA_HORA)
    fecha = ahora.strftime(FORMATO_FECHA)

    registrar_movimiento(fecha_hora, codigo, dni, ACCION_INGRESO)
    ocupacion[codigo] = {"dni": dni, "fecha_hora_ingreso": fecha_hora}
    actualizar_por_ingreso(estadisticas, fecha)

    print(f"Ingreso registrado con exito. Espacio asignado:{codigo}")
    return ocupacion


def registrar_egreso(espacios, clientes, ocupacion, estadisticas):
    """Flujo completo para registrar el egreso de un vehiculo."""
    codigo = input("Ingrese el codigo del espacio ocupado o 0 para cancelar: ").strip().upper()
    if codigo == "0":
        return ocupacion
    while not validar_codigo_espacio(codigo, espacios):
        print("El espacio ingresado no existe.")
        codigo = input("Ingrese el codigo del espacio ocupado o 0 para cancelar: ").strip().upper()
        if codigo == "0":
            return ocupacion

    ingreso = obtener_ingreso_activo(ocupacion, codigo)
    if ingreso is None:
        print("No se puede registrar el egreso porque el espacio esta libre.")
        return ocupacion

    dni = ingreso["dni"]
    fecha_hora_ingreso = ingreso["fecha_hora_ingreso"]
    ahora = datetime.now()
    fecha_hora_egreso = ahora.strftime(FORMATO_FECHA_HORA)
    fecha = ahora.strftime(FORMATO_FECHA)

    horas = calcular_permanencia_horas(fecha_hora_ingreso, fecha_hora_egreso)
    importe = calcular_importe(horas, TARIFA_POR_HORA)

    cliente = buscar_cliente(clientes, dni)
    info_cliente = "Cliente no registrado."
    if cliente is not None:
        tenia_descuento = cliente["total_horas"] >= UMBRAL_HORAS_DESCUENTO
        if tenia_descuento:
            importe = aplicar_descuento(importe, PORCENTAJE_DESCUENTO)
        actualizar_horas(clientes, dni, horas)
        total_actualizado = clientes[dni]["total_horas"]
        if tenia_descuento:
            info_cliente = f"{cliente['nombre']}: se aplico{PORCENTAJE_DESCUENTO}% de descuento."
        elif total_actualizado >= UMBRAL_HORAS_DESCUENTO:
            info_cliente = f"{cliente['nombre']}: tendra descuento disponible en su proxima visita."
        else:
            faltan = UMBRAL_HORAS_DESCUENTO - total_actualizado
            info_cliente = f"{cliente['nombre']}: le faltan{faltan} horas para el descuento."

    registrar_movimiento(fecha_hora_egreso, codigo, dni, ACCION_EGRESO)
    del ocupacion[codigo]
    actualizar_por_egreso(estadisticas, fecha, horas)

    print("----- Resumen del egreso -----")
    print(f"Espacio:{codigo}")
    print(f"DNI:{dni}")
    print(f"Ingreso:{fecha_hora_ingreso}")
    print(f"Egreso:{fecha_hora_egreso}")
    print(f"Permanencia:{horas} hora(s)")
    print(f"Importe a pagar: ${importe}")
    print(info_cliente)
    return ocupacion
