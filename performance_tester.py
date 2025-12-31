
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# SCRIPT DE PRUEBA DE CARGA HTTP ASÍNCRONO
#
# Propósito:
# Este script está diseñado para enviar un gran número de solicitudes HTTP GET
# a una URL específica de la forma más rápida posible utilizando programación
# asíncrona. Es una herramienta para realizar pruebas de carga y medir el
# rendimiento de un servidor web.
#
# Cómo funciona:
# Utiliza las librerías `asyncio` y `aiohttp`. A diferencia de un script
# secuencial que envía una solicitud y espera la respuesta antes de enviar la
# siguiente, este script puede lanzar miles de solicitudes "a la vez"
# (de forma concurrente). Esto le permite saturar la conexión de red y
# poner a prueba la capacidad del servidor para manejar múltiples peticiones
# simultáneas.
#
# -----------------------------------------------------------------------------
# ADVERTENCIA DE USO RESPONSABLE:
# Este script es una herramienta poderosa. Su uso indebido puede causar
# problemas en el servidor de destino y puede ser considerado un ataque de
# Denegación de Servicio (DoS).
#
# ==> NO LO UTILICES en sitios web o servicios sobre los que no tengas
#     permiso explícito para realizar pruebas. <==
#
# El autor de este script no se hace responsable del mal uso del mismo.
# -----------------------------------------------------------------------------

import asyncio
import aiohttp
import time

# --- CONFIGURACIÓN PRINCIPAL ---
#
# URL_A_PROBAR:
# El enlace completo del servidor o endpoint que quieres probar.
# Asegúrate de que sea una URL válida y de tener permiso para probarla.
URL_A_PROBAR = "https://www.google.com"

# NUMERO_DE_SOLICITUDES:
# La cantidad total de solicitudes GET que se enviarán a la URL.
# Un número mayor ejercerá más presión sobre el servidor.
NUMERO_DE_SOLICITUDES = 1000

# ---------------------------------

async def fetch(session, url):
    """
    Función asíncrona que realiza una única solicitud HTTP GET.

    :param session: La sesión de cliente aiohttp. Reutilizar la sesión es clave
                    para el rendimiento, ya que gestiona un pool de conexiones.
    :param url: La URL de destino para esta solicitud.
    :return: True si la solicitud devuelve un código de estado 200 (OK),
             False en cualquier otro caso (otro código o un error).
    """
    try:
        # 'async with' gestiona el ciclo de vida de la solicitud de forma asíncrona.
        # Se establece un timeout de 10 segundos. Si el servidor no responde en
        # ese tiempo, la solicitud se considerará fallida.
        async with session.get(url, timeout=10) as response:
            # Para una prueba de carga, a menudo solo nos importa si el servidor
            # responde correctamente (código 200), no el contenido de la respuesta.
            # Esto ahorra ancho de banda y tiempo de procesamiento.
            return response.status == 200
    except Exception:
        # Captura cualquier tipo de excepción (ej. timeouts, errores de DNS,
        # problemas de conexión) y la marca como una solicitud fallida.
        return False

async def main():
    """
    Función principal asíncrona que orquesta toda la prueba de carga.
    """
    print("--- Iniciando prueba de carga HTTP asíncrona ---")
    print(f"URL de destino: {URL_A_PROBAR}")
    print(f"Número de solicitudes a enviar: {NUMERO_DE_SOLICITUDES}")
    print("-------------------------------------------------")

    # time.monotonic() es ideal para medir intervalos de tiempo.
    tiempo_inicio = time.monotonic()

    # Usamos aiohttp.ClientSession() para crear una sesión que será reutilizada
    # por todas nuestras solicitudes. Esto es fundamental para el rendimiento.
    async with aiohttp.ClientSession() as session:
        # Aquí creamos la lista de "tareas". Cada tarea es una llamada a la
        # función `fetch`. En este punto, las tareas aún no se han ejecutado.
        # Son solo objetos "coroutine" listos para ser programados.
        tareas = [fetch(session, URL_A_PROBAR) for _ in range(NUMERO_DE_SOLICITUDES)]

        # asyncio.gather() es la magia. Le pasamos la lista de tareas y él se
        # encarga de ejecutarlas todas de la forma más concurrente posible.
        # `await` pausa la ejecución de `main` hasta que TODAS las tareas hayan finalizado.
        resultados = await asyncio.gather(*tareas)

    # El tiempo se detiene justo después de que la última solicitud ha terminado.
    tiempo_fin = time.monotonic()

    # Procesamos los resultados obtenidos.
    exitosas = resultados.count(True)
    fallidas = resultados.count(False)

    # Calculamos las métricas de rendimiento.
    duracion_total = tiempo_fin - tiempo_inicio

    # Solicitudes Por Segundo (RPS) o "throughput". Es una métrica clave
    # que indica cuántas peticiones puede manejar el servidor por segundo.
    solicitudes_por_segundo = exitosas / duracion_total if duracion_total > 0 else 0

    # Imprimimos un resumen claro y útil.
    print("\n--- Resultados de la prueba ---")
    print(f"Tiempo total de ejecución: {duracion_total:.2f} segundos")
    print(f"Solicitudes exitosas (código 200): {exitosas}")
    print(f"Solicitudes fallidas (error o código != 200): {fallidas}")
    print(f"Rendimiento (RPS): {solicitudes_por_segundo:.2f} solicitudes por segundo")
    print("-------------------------------")


# Este es el punto de entrada del script.
if __name__ == "__main__":
    # asyncio.run() inicia el bucle de eventos de asyncio, ejecuta la
    # corutina `main()` que le pasamos y cierra el bucle al finalizar.
    asyncio.run(main())
