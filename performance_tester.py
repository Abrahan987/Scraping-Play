
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# SCRIPT DE PRUEBA DE CARGA HTTP ASÍNCRONO (VERSIÓN MEJORADA)
#
# Propósito:
# Este script está diseñado para enviar un gran número de solicitudes HTTP GET
# a una URL específica de forma controlada y medible. Es una herramienta
# para realizar pruebas de carga realistas y encontrar el punto de quiebre
# de un servidor web.
#
# Novedades de esta versión:
# Se ha añadido un límite de concurrencia (`MAX_CONCURRENCIA`). En lugar de
# lanzar todas las solicitudes a la vez (lo que puede causar errores masivos),
# el script mantiene un número controlado de solicitudes activas simultáneamente.
# Cuando una termina, se lanza la siguiente, asegurando una presión constante
# y medible sobre el servidor.
#
# -----------------------------------------------------------------------------
# ADVERTENCIA DE USO RESPONSABLE:
# ==> NO LO UTILICES en sitios web o servicios sobre los que no tengas
#     permiso explícito para realizar pruebas. <==
# -----------------------------------------------------------------------------

import asyncio
import aiohttp
import time

# --- CONFIGURACIÓN PRINCIPAL ---
#
# URL_A_PROBAR:
# El enlace completo del servidor o endpoint que quieres probar.
URL_A_PROBAR = "http://185.16.39.160:3046/"

# NUMERO_DE_SOLICITUDES:
# La cantidad total de solicitudes GET que se enviarán a la URL.
NUMERO_DE_SOLICITUDES = 10000

# MAX_CONCURRENCIA:
# ¡Este es el ajuste clave! Limita cuántas solicitudes se ejecutan al mismo tiempo.
# Un valor demasiado alto causará los errores que vistes antes.
# Un buen punto de partida es 100. Puedes subirlo poco a poco para ver
# cuánto aguanta tu servidor antes de empezar a fallar.
MAX_CONCURRENCIA = 100
# ---------------------------------

async def fetch(session, url):
    """
    Función asíncrona que realiza una única solicitud HTTP GET.
    :return: True si la solicitud devuelve un código de estado 200 (OK),
             False en cualquier otro caso (otro código o un error).
    """
    try:
        async with session.get(url, timeout=15) as response:
            return response.status == 200
    except Exception:
        return False

async def fetch_controlado(semaphore, session, url):
    """
    Un "wrapper" para la función fetch que respeta el semáforo.
    La corutina esperará aquí si ya hay demasiadas solicitudes activas.
    """
    async with semaphore:
        return await fetch(session, url)

async def main():
    """
    Función principal asíncrona que orquesta toda la prueba de carga.
    """
    print("--- Iniciando prueba de carga HTTP controlada ---")
    print(f"URL de destino: {URL_A_PROBAR}")
    print(f"Número total de solicitudes: {NUMERO_DE_SOLICITUDES}")
    print(f"Nivel de concurrencia máximo: {MAX_CONCURRENCIA}")
    print("-------------------------------------------------")

    tiempo_inicio = time.monotonic()

    # Creamos un semáforo que no permitirá que más de MAX_CONCURRENCIA
    # corutinas entren en el bloque 'async with' al mismo tiempo.
    semaphore = asyncio.Semaphore(MAX_CONCURRENCIA)

    async with aiohttp.ClientSession() as session:
        # Creamos la lista de tareas, pero esta vez usando nuestra función controlada.
        tareas = [
            fetch_controlado(semaphore, session, URL_A_PROBAR)
            for _ in range(NUMERO_DE_SOLICITUDES)
        ]

        # asyncio.gather sigue siendo la forma de esperar a que todo termine.
        resultados = await asyncio.gather(*tareas)

    tiempo_fin = time.monotonic()

    # Procesamos los resultados.
    exitosas = resultados.count(True)
    fallidas = resultados.count(False)

    # Calculamos las métricas de rendimiento.
    duracion_total = tiempo_fin - tiempo_inicio
    solicitudes_por_segundo = exitosas / duracion_total if duracion_total > 0 else 0

    print("\n--- Resultados de la prueba ---")
    print(f"Tiempo total de ejecución: {duracion_total:.2f} segundos")
    print(f"Solicitudes exitosas (código 200): {exitosas}")
    print(f"Solicitudes fallidas (error o código != 200): {fallidas}")
    print(f"Rendimiento (RPS): {solicitudes_por_segundo:.2f} solicitudes por segundo")
    print("-------------------------------")

if __name__ == "__main__":
    asyncio.run(main())
