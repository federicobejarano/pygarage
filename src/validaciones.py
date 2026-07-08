"""Validaciones de entrada del usuario."""


def validar_opcion_menu(opcion, minimo, maximo):
    """Valida que la opcion de menu sea un numero dentro del rango esperado."""
    opcion = opcion.strip()
    if not opcion.isdigit():
        return False
    numero = int(opcion)
    return minimo <= numero <= maximo


def validar_dni(dni):
    """Valida formato y longitud del DNI (solo digitos, entre 7 y 8)."""
    dni = dni.strip()
    if not dni.isdigit():
        return False
    return 7 <= len(dni) <= 8


def validar_nombre(nombre):
    """Valida que el nombre no este vacio."""
    return nombre.strip() != ""


def validar_codigo_espacio(codigo, espacios):
    """Valida que el codigo de espacio tenga el formato esperado y exista."""
    codigo = codigo.strip().upper()
    partes = codigo.split("-")
    if len(partes) != 2:
        return False
    piso, numero = partes
    if not piso.startswith("P") or not numero.startswith("E"):
        return False
    if not piso[1:].isdigit() or not numero[1:].isdigit():
        return False
    for espacio in espacios:
        if espacio["codigo"] == codigo:
            return True
    return False