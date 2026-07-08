"""Presentacion por consola y flujos de operaciones."""

from datetime import datetime

from src.calculos import (
    aplicar_descuento,
    calcular_importe,
    calcular_permanencia_horas,
    estado_descuento,
)
from src.clientes import actualizar_horas, buscar_cliente, registrar_cliente
from src.contratos import (
    ACCION_EGRESO,
    ACCION_INGRESO,
    FORMATO_FECHA,
    FORMATO_FECHA_HORA,
    PORCENTAJE_DESCUENTO,
    TARIFA_POR_HORA,
    UMBRAL_HORAS_DESCUENTO,
)
from src.espacios import listar_disponibles, sugerir_espacio
from src.estadisticas import (
    actualizar_por_egreso,
    actualizar_por_ingreso,
    calcular_porcentaje_ocupacion,
    calcular_promedio,
)
from src.movimientos import obtener_ingreso_activo, registrar_movimiento
from src.validaciones import (
    validar_codigo_espacio,
    validar_dni,
    validar_nombre,
    validar_opcion_menu,
)


def mostrar_menu_principal():
    """Muestra el menu principal numerado con 7 opciones."""
    print()
    print("=== ESTACIONAMIENTO ===")
    print("1. Registrar ingreso")
    print("2. Registrar egreso")
    print("3. Registrar cliente")
    print("4. Consultar cliente")
    print("5. Consultar espacios disponibles")
    print("6. Consultar estadisticas")
    print("7. Finalizar programa")


def mostrar_menu_estadisticas():
    """Muestra el submenu de estadisticas con 4 opciones."""
    print()
    print("=== ESTADISTICAS ===")
    print("1. Porcentaje de ocupacion actual")
    print("2. Cantidad de vehiculos atendidos hoy")
    print("3. Tiempo promedio de permanencia")
    print("4. Volver al menu principal")


def leer_opcion(mensaje, minimo, maximo):
    """Lee y valida una opcion numerica del usuario con reintento."""
    while True:
        opcion = input(mensaje)
        if validar_opcion_menu(opcion, minimo, maximo):
            return int(opcion)
        print("Opcion invalida. Ingrese un numero del menu.")


def formatear_espacios_disponibles(disponibles_por_piso, libres, ocupados, total):
    """Formatea el listado de espacios disponibles agrupados por piso."""
    lineas = []
    lineas.append("Espacios disponibles")
    lineas.append("")

    for piso in sorted(disponibles_por_piso):
        codigos = disponibles_por_piso[piso]
        if codigos:
            lineas.append("Piso " + str(piso) + ": " + ", ".join(codigos))
        else:
            lineas.append("Piso " + str(piso) + ": sin espacios disponibles")

    lineas.append("")
    lineas.append(
        "Libres: "
        + str(libres)
        + " | Ocupados: "
        + str(ocupados)
        + " | Total: "
        + str(total)
    )
    return "\n".join(lineas)


def pausar_para_continuar():
    """Muestra pausa para volver al menu principal."""
    input("Presione Enter para volver al menu...")


def finalizar_programa():
    """Muestra mensaje de cierre del programa."""
    print("Cerrando sistema...")


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
        print(f"Bienvenido/a {cliente['nombre']}.")
    else:
        respuesta = input(
            "El cliente no esta registrado. Desea registrarlo? (s/n): "
        ).strip().lower()
        if respuesta == "s":
            nombre = input("Ingrese el nombre del cliente: ").strip()
            while not validar_nombre(nombre):
                print("El nombre no puede estar vacio.")
                nombre = input("Ingrese el nombre del cliente: ").strip()
            registrar_cliente(clientes, dni, nombre)
            print(f"Cliente {nombre} registrado con exito.")
        else:
            print("El ingreso continuara como cliente no registrado.")

    sugerido = sugerir_espacio(espacios, ocupacion)
    if sugerido is None:
        print("No hay espacios disponibles en este momento.")
        return ocupacion

    print(f"Espacio sugerido: {sugerido['codigo']}")
    respuesta = input("Acepta el espacio sugerido? (s/n): ").strip().lower()
    if respuesta == "s":
        codigo = sugerido["codigo"]
    else:
        disponibles = listar_disponibles(espacios, ocupacion)
        for piso in sorted(disponibles):
            print(f"Piso {piso}: {', '.join(disponibles[piso])}")

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

    print(f"Ingreso registrado con exito. Espacio asignado: {codigo}")
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
            info_cliente = (
                f"{cliente['nombre']}: se aplico {PORCENTAJE_DESCUENTO}% de descuento."
            )
        elif total_actualizado >= UMBRAL_HORAS_DESCUENTO:
            info_cliente = (
                f"{cliente['nombre']}: tendra descuento disponible en su proxima visita."
            )
        else:
            faltan = UMBRAL_HORAS_DESCUENTO - total_actualizado
            info_cliente = f"{cliente['nombre']}: le faltan {faltan} horas para el descuento."

    registrar_movimiento(fecha_hora_egreso, codigo, dni, ACCION_EGRESO)
    del ocupacion[codigo]
    actualizar_por_egreso(estadisticas, fecha, horas)

    print("----- Resumen del egreso -----")
    print(f"Espacio: {codigo}")
    print(f"DNI: {dni}")
    print(f"Ingreso: {fecha_hora_ingreso}")
    print(f"Egreso: {fecha_hora_egreso}")
    print(f"Permanencia: {horas} hora(s)")
    print(f"Importe a pagar: ${importe}")
    print(info_cliente)
    return ocupacion


def flujo_registrar_cliente(clientes):
    """Flujo completo para registrar un cliente nuevo."""
    dni = input("Ingrese DNI o 0 para cancelar: ").strip()
    if dni == "0":
        return

    while not validar_dni(dni):
        print("DNI invalido. Debe ingresar solo numeros (7 u 8 digitos).")
        dni = input("Ingrese DNI o 0 para cancelar: ").strip()
        if dni == "0":
            return

    if buscar_cliente(clientes, dni) is not None:
        print("El cliente ya esta registrado.")
        return

    nombre = input("Ingrese el nombre del cliente: ").strip()
    while not validar_nombre(nombre):
        print("El nombre no puede estar vacio.")
        nombre = input("Ingrese el nombre del cliente: ").strip()

    registrar_cliente(clientes, dni, nombre)
    print(f"Cliente {nombre} registrado con exito.")


def flujo_consultar_cliente(clientes):
    """Flujo completo para consultar un cliente registrado."""
    dni = input("Ingrese DNI o 0 para cancelar: ").strip()
    if dni == "0":
        return

    while not validar_dni(dni):
        print("DNI invalido. Debe ingresar solo numeros (7 u 8 digitos).")
        dni = input("Ingrese DNI o 0 para cancelar: ").strip()
        if dni == "0":
            return

    cliente = buscar_cliente(clientes, dni)
    if cliente is None:
        print("El cliente no esta registrado.")
        respuesta = input("Desea registrarlo? (s/n): ").strip().lower()
        if respuesta == "s":
            flujo_registrar_cliente(clientes)
        return

    print(f"DNI: {dni}")
    print(f"Nombre: {cliente['nombre']}")
    print(f"Horas acumuladas: {cliente['total_horas']}")
    print(estado_descuento(cliente["total_horas"], UMBRAL_HORAS_DESCUENTO))


def flujo_consultar_espacios(espacios, ocupacion):
    """Flujo completo para consultar espacios disponibles."""
    disponibles = listar_disponibles(espacios, ocupacion)
    total = len(espacios)
    ocupados = len(ocupacion)
    libres = total - ocupados
    print(formatear_espacios_disponibles(disponibles, libres, ocupados, total))
    pausar_para_continuar()


def flujo_consultar_estadisticas(estadisticas, espacios, ocupacion):
    """Flujo completo del submenu de estadisticas."""
    opcion = 0
    while opcion != 4:
        mostrar_menu_estadisticas()
        opcion = leer_opcion("Elija una opcion: ", 1, 4)

        if opcion == 1:
            porcentaje = calcular_porcentaje_ocupacion(ocupacion, espacios)
            print(f"Porcentaje de ocupacion actual: {porcentaje:.2f}%")
            pausar_para_continuar()

        elif opcion == 2:
            hoy = datetime.now().strftime(FORMATO_FECHA)
            datos_hoy = estadisticas["por_fecha"].get(hoy, {})
            atendidos = datos_hoy.get("ingresos", 0)
            print(f"Vehiculos atendidos hoy: {atendidos}")
            pausar_para_continuar()

        elif opcion == 3:
            criterio = leer_opcion("Promedio por: 1) Mes  2) Dia de semana: ", 1, 2)
            if criterio == 1:
                grupo = estadisticas["por_mes"]
                titulo = "Tiempo promedio de permanencia por mes"
            else:
                grupo = estadisticas["por_dia_semana"]
                titulo = "Tiempo promedio de permanencia por dia de semana"

            print(titulo)
            if len(grupo) == 0:
                print("Sin datos suficientes")
            else:
                for clave in sorted(grupo):
                    datos = grupo[clave]
                    promedio = calcular_promedio(datos["total_horas"], datos["egresos"])
                    if promedio is None:
                        print(f"  {clave}: Sin datos suficientes")
                    else:
                        print(f"  {clave}: {promedio:.2f} horas")
            pausar_para_continuar()
