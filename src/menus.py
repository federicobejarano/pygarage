"""Presentacion por consola y flujos de operaciones."""

from src.validaciones import validar_opcion_menu


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
    lineas.append("Libres: " + str(libres) + " | Ocupados: " + str(ocupados) + " | Total: " + str(total))
    return "\n".join(lineas)


def pausar_para_continuar():
    """Muestra pausa para volver al menu principal."""
    input("Presione Enter para volver al menu...")
