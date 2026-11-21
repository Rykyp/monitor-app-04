"""Monitor de estabilidad semanal para una aplicación móvil."""

import logging
import sys
from typing import Final

# Añadid aquí las importaciones que necesitéis.

# ---------------------------------------------------------------------------
# Datos de la aplicación. Sustituid los del ejemplo APP-00 por los vuestros.
# ---------------------------------------------------------------------------
CODIGO: Final[str] = "APP-04"
NOMBRE: Final[str] = "Agenda Escolar"
# Una posición por semana, de la 1 a la 12. 0 descargas: app retirada.
DESCARGAS: Final = [1_200, 1_350, 1_280, 1_500, 0, 1_720,
                    2_050, 1_810, 1_980, 2_310, 2_200, 2_150]
CAIDAS: Final = [14, 12, 15, 9, 0, 22,
                 31, 8, 6, 9, 5, 4]

# ---------------------------------------------------------------------------
# Datos del programa. Solo hay que cambiar AUTORES.
# ---------------------------------------------------------------------------
VERSION_PROGRAMA: Final[str] = "1.0.0"
AUTORES: Final[str] = "ricardo.palomares.viseras · pablo.morales.gabarron"
PENDIENTE: Final[str] = "  (opción pendiente de implementar)"

# ---------------------------------------------------------------------------
# Constantes comunes.
# ---------------------------------------------------------------------------
ANCHO: Final[int] = 44
POR_MIL: Final[int] = 1_000
UMBRAL_ESTABLE: Final[float] = 5.0       # caídas por cada mil descargas
UMBRAL_ACEPTABLE: Final[float] = 10.0
UMBRAL_REVISAR: Final[float] = 15.0
OPCION_SALIR: Final[int] = 9

# ---------------------------------------------------------------------------
# Constantes de la pareja. Todo valor fijo del programa va aquí, con nombre.
# ---------------------------------------------------------------------------
OPCION_MINIMA: Final[int] = 1
UMBRAL_MINIMO: Final[float] = 0.0
UMBRAL_MAXIMO: Final[float] = 1_000.0
SEPARADOR_MENU: Final[str] = "="
RESPUESTA_SI: Final[str] = "s"

ESTADO_ESTABLE: Final[str] = "Estable"
ESTADO_ACEPTABLE: Final[str] = "Aceptable"
ESTADO_REVISAR: Final[str] = "Revisar"
ESTADO_CRITICA: Final[str] = "Crítica"
ESTADO_MANTENIMIENTO: Final[str] = "Mantenimiento"

SEMANA_MINIMA: Final[int] = 1

OBJETIVO_MAXIMO: Final[int] = 1_000_000
CRECIMIENTO_MINIMO: Final[float] = 0.5
CRECIMIENTO_MAXIMO: Final[float] = 50.0
SEMANAS_PREVISION_MAXIMAS: Final[int] = 104
POR_CIENTO: Final[int] = 100
INCREMENTO_MINIMO_DESCARGAS: Final[int] = 1

# ---------------------------------------------------------------------------
# Excepciones propias de la pareja. Aquí va SemanaNoValida (opción 7).
# ---------------------------------------------------------------------------
class SemanaNoValida(Exception):
    """Error lanzado cuando el número de semana no es válido."""


# ---------------------------------------------------------------------------
# Funciones auxiliares. tasa_caidas viene hecha; el resto, con su docstring,
# las completáis vosotros. No cambiéis sus cabeceras.
# ---------------------------------------------------------------------------
def tasa_caidas(descargas: int, caidas: int) -> float:
    """Devuelve las caídas por cada mil descargas.

    Lanza ZeroDivisionError si la semana no tiene descargas.
    """
    return caidas / descargas * POR_MIL


def estado(descargas: int, caidas: int) -> str:
    """Devuelve el estado de una semana según su tasa de caídas.

    Es uno de estos textos: "Estable", "Aceptable", "Revisar", "Crítica" o
    "Mantenimiento", este último si la semana no tiene descargas.
    """
    try:
        tasa = tasa_caidas(descargas, caidas)
    except ZeroDivisionError:
        return ESTADO_MANTENIMIENTO
    if tasa < UMBRAL_ESTABLE:
        return ESTADO_ESTABLE
    if tasa < UMBRAL_ACEPTABLE:
        return ESTADO_ACEPTABLE
    if tasa < UMBRAL_REVISAR:
        return ESTADO_REVISAR
    return ESTADO_CRITICA


def pedir_entero(mensaje: str, minimo: int, maximo: int) -> int:
    """Pide un entero entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un entero o está fuera de rango, avisa y
    lo vuelve a pedir.
    """
    while True:
        entrada = input(mensaje)
        try:
            valor = int(entrada)
        except ValueError:
            print(f"«{entrada}» no es un número entero.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"El valor debe estar entre {minimo} y {maximo}.")


def pedir_real(mensaje: str, minimo: float, maximo: float) -> float:
    """Pide un número real entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un número o está fuera de rango, avisa y
    lo vuelve a pedir.
    """
    while True:
        entrada = input(mensaje)
        try:
            valor = float(entrada)
        except ValueError:
            print(f"«{entrada}» no es un número válido.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"El valor debe estar entre {minimo} y {maximo}.")


def semana_valida(texto: str) -> int:
    """Convierte el texto en un número de semana de los datos.

    Lanza SemanaNoValida si no es un entero o está fuera de rango.
    """
    try:
        semana = int(texto)
    except ValueError:
        raise SemanaNoValida(
            f"«{texto}» no es un número de semana"
        ) from None

    ultima_semana = len(DESCARGAS)
    if not SEMANA_MINIMA <= semana <= ultima_semana:
        raise SemanaNoValida(
            f"la semana {semana} no existe: "
            f"hay de {SEMANA_MINIMA} a {ultima_semana}"
        )

    return semana


def comprobar_datos() -> int:
    """Revisa los datos semanales y devuelve el número de errores.

    Registra cada error con logging.error y cada semana de mantenimiento
    con logging.warning.
    """
    errores = 0

    if len(DESCARGAS) != len(CAIDAS):
        logging.error(
            "las listas de descargas y caídas tienen distinta longitud"
        )
        errores += 1

    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas < 0:
            logging.error("semana %s: descargas negativas", semana)
            errores += 1

        if caidas < 0:
            logging.error("semana %s: caídas negativas", semana)
            errores += 1

        if caidas > descargas:
            logging.error("semana %s: más caídas que descargas", semana)
            errores += 1

        if descargas == 0:
            logging.warning(
                "semana %s: sin descargas (mantenimiento)", semana
            )

    return errores


# ---------------------------------------------------------------------------
# Menú y opciones. La opción 1 viene hecha y la 2 tiene dos errores.
# ---------------------------------------------------------------------------
def mostrar_menu() -> None:
    """Muestra la cabecera de la aplicación y las opciones del menú."""
    linea = SEPARADOR_MENU * ANCHO
    titulo = f"MONITOR DE {CODIGO} · {NOMBRE}"
    print(linea)
    print(titulo.center(ANCHO))
    print(linea)
    print("1. Listado semanal")
    print("2. Resumen")
    print("3. Estabilidad por semana")
    print("4. Primera semana que alcanza un umbral")
    print("5. Mejor racha sin problemas")
    print("6. Previsión de crecimiento")
    print("7. Consultar una semana")
    print("8. Comprobar los datos")
    print("9. Salir")


def opcion_1_listado() -> None:
    """Muestra las descargas, las caídas y la tasa de cada semana."""
    print(f"{'Semana':>6}{'Descargas':>11}{'Caídas':>8}{'Tasa ‰':>9}")
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        try:
            tasa = f"{tasa_caidas(descargas, caidas):.1f}"
        except ZeroDivisionError:
            tasa = "—"
        print(f"{semana:>6}{descargas:>11}{caidas:>8}{tasa:>9}")


def opcion_2_resumen() -> None:
    """Muestra los totales, la media y las semanas extremas."""
    total_descargas = 0
    total_caidas = 0
    activas = 0
    mas = 0
    semana_mas = 0
    menos = 0
    semana_menos = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        activas += 1
        total_descargas += descargas
        total_caidas += caidas
        if descargas > mas:
            mas = descargas
            semana_mas = semana
        if activas == 1 or descargas < menos:
            menos = descargas
            semana_menos = semana
    media = total_descargas / activas
    tasa = tasa_caidas(total_descargas, total_caidas)
    print(f"Semanas activas:     {activas} de {len(DESCARGAS)}")
    print(f"Total de descargas:  {total_descargas}")
    print(f"Media semanal:       {media:.1f}")
    print(f"Más descargas:       semana {semana_mas} ({mas})")
    print(f"Menos descargas:     semana {semana_menos} ({menos})")
    print(f"Total de caídas:     {total_caidas}")
    print(f"Tasa global:         {tasa:.1f} ‰")


def opcion_3_estabilidad() -> None:
    """Muestra el estado de cada semana y cuántas hay de cada tipo."""
    estables = 0
    aceptables = 0
    revisar = 0
    criticas = 0
    mantenimiento = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        estado_semana = estado(descargas, caidas)
        print(f"Semana {semana:>2}: {estado_semana}")
        match estado_semana:
            case "Estable":
                estables += 1
            case "Aceptable":
                aceptables += 1
            case "Revisar":
                revisar += 1
            case "Crítica":
                criticas += 1
            case "Mantenimiento":
                mantenimiento += 1
    print(f"Estables:      {estables}")
    print(f"Aceptables:    {aceptables}")
    print(f"Revisar:       {revisar}")
    print(f"Críticas:      {criticas}")
    print(f"Mantenimiento: {mantenimiento}")


def opcion_4_umbral() -> None:
    """Busca la primera semana que alcanza o supera un umbral de caídas."""
    umbral = pedir_real(
        "Umbral en caídas por mil: ",
        UMBRAL_MINIMO,
        UMBRAL_MAXIMO,
    )
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        tasa = tasa_caidas(descargas, caidas)
        if tasa >= umbral:
            print(f"Primera semana: {semana} ({tasa:.1f} ‰)")
            break
    else:
        print(f"Ninguna semana alcanza {umbral:.1f} ‰")


def opcion_5_racha() -> None:
    """Busca la racha más larga de semanas seguidas estables o aceptables."""
    racha_actual = 0
    inicio_actual = 0
    mejor_racha = 0
    mejor_inicio = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        estado_semana = estado(descargas, caidas)
        if estado_semana == ESTADO_MANTENIMIENTO:
            continue
        if estado_semana in (ESTADO_ESTABLE, ESTADO_ACEPTABLE):
            if racha_actual == 0:
                inicio_actual = semana
            racha_actual += 1
            if racha_actual > mejor_racha:
                mejor_racha = racha_actual
                mejor_inicio = inicio_actual
        else:
            racha_actual = 0
    if mejor_racha == 0:
        print("No hay ninguna racha sin problemas.")
    else:
        print(
            f"Mejor racha: {mejor_racha} semanas, "
            f"desde la semana {mejor_inicio}"
        )


def opcion_6_prevision() -> None:
    """Calcula las semanas necesarias para alcanzar un objetivo de descargas."""
    ultimas_descargas = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        ultimas_descargas = descargas

    print(f"Descargas de la última semana activa: {ultimas_descargas}")

    objetivo_minimo = ultimas_descargas + INCREMENTO_MINIMO_DESCARGAS
    objetivo = pedir_entero(
        "Objetivo semanal de descargas: ",
        objetivo_minimo,
        OBJETIVO_MAXIMO,
    )
    crecimiento = pedir_real(
        "Crecimiento semanal en %: ",
        CRECIMIENTO_MINIMO,
        CRECIMIENTO_MAXIMO,
    )

    proporcion_crecimiento = crecimiento / POR_CIENTO
    descargas_previstas = float(ultimas_descargas)
    semanas = 0

    while descargas_previstas < objetivo:
        if semanas >= SEMANAS_PREVISION_MAXIMAS:
            break
        aumento = descargas_previstas * proporcion_crecimiento
        descargas_previstas += aumento
        semanas += 1

    if descargas_previstas >= objetivo:
        print(
            f"Se alcanza en {semanas} semanas "
            f"({descargas_previstas:.0f} descargas)"
        )
    else:
        print(
            f"No se alcanza el objetivo en "
            f"{SEMANAS_PREVISION_MAXIMAS} semanas."
        )


def opcion_7_consulta() -> None:
    """Consulta los datos, el estado y la acción recomendada de una semana."""
    entrada = input("Número de semana: ")
    try:
        semana = semana_valida(entrada)
    except SemanaNoValida as error:
        print(f"No se puede consultar: {error}")
        return

    for numero_semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if numero_semana != semana:
            continue
        estado_semana = estado(descargas, caidas)
        match estado_semana:
            case "Estable":
                accion = "Sin acciones"
            case "Aceptable":
                accion = "Vigilar en la próxima versión"
            case "Revisar":
                accion = "Revisar los informes de errores"
            case "Crítica":
                accion = "Publicar una versión correctora urgente"
            case "Mantenimiento":
                accion = "La app no estuvo publicada esa semana"

        print(f"Semana {semana}:")
        print(f"  Descargas: {descargas}")
        print(f"  Caídas:    {caidas}")
        print(f"  Estado:    {estado_semana}")
        print(f"  Acción:    {accion}")
        break


def opcion_8_comprobar() -> None:
    """Comprueba los datos y muestra cuántos errores se han encontrado."""
    errores = comprobar_datos()
    if errores == 0:
        print(f"Datos correctos: {len(DESCARGAS)} semanas")
    else:
        print(f"Los datos tienen errores: {errores}")


def main() -> None:
    """Arranca el programa, comprueba los datos y ejecuta el menú."""
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s",
    )
    errores = comprobar_datos()
    if errores > 0:
        sys.exit("Los datos tienen errores: corrígelos antes de continuar.")

    print(f"Monitor de estabilidad {VERSION_PROGRAMA} · {AUTORES}")

    try:
        while True:
            mostrar_menu()
            entrada = input("Opción: ")
            try:
                opcion = int(entrada)
            except ValueError:
                print(f"«{entrada}» no es una opción.")
                continue

            match opcion:
                case 1:
                    opcion_1_listado()
                case 2:
                    opcion_2_resumen()
                case 3:
                    opcion_3_estabilidad()
                case 4:
                    opcion_4_umbral()
                case 5:
                    opcion_5_racha()
                case 6:
                    opcion_6_prevision()
                case 7:
                    opcion_7_consulta()
                case 8:
                    opcion_8_comprobar()
                case _ if opcion == OPCION_SALIR:
                    confirmar = input("¿Salir del programa? (s/n): ")
                    if confirmar.strip().lower() == RESPUESTA_SI:
                        break
                case _:
                    print(
                        f"Elige una opción entre {OPCION_MINIMA} y "
                        f"{OPCION_SALIR}."
                    )
    except KeyboardInterrupt:
        print("\nPrograma interrumpido.")

    print(f"Fin del monitor de {CODIGO}.")


if __name__ == "__main__":
    main()