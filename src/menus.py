"""Presentacion por consola y flujos de operaciones."""

from src.estadisticas import calcular_porcentaje_ocupacion, calcular_promedio

from src.validaciones import validar_opcion_menu

from src.calculos import estado_descuento


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
    print(f"Cliente{nombre} registrado con exito.")


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

    print(f"DNI:{dni}")
    print(f"Nombre:{cliente['nombre']}")
    print(f"Horas acumuladas:{cliente['total_horas']}")
    print(estado_descuento(cliente["total_horas"], UMBRAL_HORAS_DESCUENTO))

def mostrar_menu_estadisticas():
    """Muestra el submenu de estadisticas con 4 opciones."""
    print()
    print("=== ESTADISTICAS ===")
    print("1. Porcentaje de ocupacion actual")
    print("2. Cantidad de vehiculos atendidos hoy")
    print("3. Tiempo promedio de permanencia")
    print("4. Volver al menu principal")


def flujo_consultar_estadisticas(estadisticas, espacios, ocupacion):
    """Flujo completo del submenu de estadisticas."""
    opcion = 0
    while opcion != 4:
        mostrar_menu_estadisticas()
        opcion = leer_opcion("Elija una opcion: ", 1, 4)

        if opcion == 1:
            porcentaje = calcular_porcentaje_ocupacion(ocupacion, espacios)
            print(f"Porcentaje de ocupacion actual:{porcentaje:.2f}%")
            pausar_para_continuar()

        elif opcion == 2:
            hoy = datetime.now().strftime(FORMATO_FECHA)
            datos_hoy = estadisticas["por_fecha"].get(hoy, {})
            atendidos = datos_hoy.get("ingresos", 0)
            print(f"Vehiculos atendidos hoy:{atendidos}")
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
                        print(f"{clave}: Sin datos suficientes")
                    else:
                        print(f"{clave}:{promedio:.2f} horas")
            pausar_para_continuar()

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
    lineas.append("Libres: " + str(libres) + " | Ocupados: " + str(ocupados) + " | Total: " + str(total))
    return "\n".join(lineas)


def pausar_para_continuar():
    """Muestra pausa para volver al menu principal."""
    input("Presione Enter para volver al menu...")
