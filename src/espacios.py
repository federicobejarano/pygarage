from src.archivos import leer_csv
from src.contratos import RUTA_ESPACIOS


def cargar_espacios():
    """Carga la configuracion de espacios desde el archivo CSV."""
    filas = leer_csv(RUTA_ESPACIOS)
    espacios = []
    codigos_vistos = []

    for fila in filas:
        codigo = fila["codigo"]
        piso = fila["piso"]
        numero = fila["numero"]

        if not piso.isdigit() or not numero.isdigit():
            print(f"Espacio invalido (piso o numero no numerico):{codigo}")
            continue

        if codigo in codigos_vistos:
            print(f"Codigo de espacio duplicado, se ignora:{codigo}")
            continue

        codigos_vistos.append(codigo)
        espacios.append({
            "codigo": codigo,
            "piso": int(piso),
            "numero": int(numero),
        })

    if len(espacios) == 0:
        print("Advertencia: no se cargaron espacios. Revise data/espacios.csv.")

    return espacios


def buscar_espacio(espacios, codigo):
    """Busca un espacio por su codigo en la lista en memoria."""
    codigo = codigo.strip().upper()
    for espacio in espacios:
        if espacio["codigo"] == codigo:
            return espacio
    return None


def listar_disponibles(espacios, ocupacion):
    """Lista espacios disponibles agrupados por piso."""
    disponibles_por_piso = {}
    for espacio in espacios:
        if espacio["codigo"] not in ocupacion:
            piso = espacio["piso"]
            if piso not in disponibles_por_piso:
                disponibles_por_piso[piso] = []
            disponibles_por_piso[piso].append(espacio["codigo"])
    return disponibles_por_piso


def sugerir_espacio(espacios, ocupacion):
    """Sugiere el espacio disponible con menor piso y menor numero."""
    sugerido = None
    for espacio in espacios:
        if espacio["codigo"] not in ocupacion:
            if sugerido is None:
                sugerido = espacio
            elif espacio["piso"] < sugerido["piso"]:
                sugerido = espacio
            elif espacio["piso"] == sugerido["piso"] and espacio["numero"] < sugerido["numero"]:
                sugerido = espacio
    return sugerido