
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Este script es un ejemplo de cómo interactuar con una base de datos SQLite
# desde Python. SQLite es una base de datos que no requiere un servidor
# separado, ya que almacena todo en un único archivo en el disco.
# Es ideal para prototipos, aplicaciones pequeñas o con fines educativos.
#
# Para adaptar este script a otras bases de datos como MySQL o PostgreSQL:
# 1. Instala el conector adecuado:
#    - Para MySQL: pip install mysql-connector-python
#    - Para PostgreSQL: pip install psycopg2
# 2. Cambia la función `crear_conexion` para usar el conector correspondiente.
#    Por ejemplo, para MySQL, usarías `mysql.connector.connect(...)` con
#    parámetros como host, user, password y database.
# 3. La sintaxis de SQL (como CREATE TABLE, INSERT, SELECT) es muy similar,
#    pero algunos tipos de datos o funciones pueden variar ligeramente.
# -----------------------------------------------------------------------------

import sqlite3

def crear_conexion(db_file):
    """
    Crea una conexión a la base de datos SQLite especificada por db_file.
    :param db_file: ruta al archivo de la base de datos SQLite.
    :return: Objeto de conexión o None si ocurre un error.
    """
    conn = None
    try:
        # sqlite3.connect() abre una conexión a la base de datos.
        # Si el archivo no existe, lo creará automáticamente.
        conn = sqlite3.connect(db_file)
        print(f"Conectado a la base de datos: {db_file}")
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
    return conn

def crear_tabla(conn):
    """
    Crea la tabla 'personas' utilizando la conexión proporcionada.
    La tabla solo se creará si no existe previamente.
    :param conn: Objeto de conexión a la base de datos.
    """
    try:
        # Un cursor es un objeto que te permite ejecutar comandos SQL.
        cursor = conn.cursor()
        # El comando 'CREATE TABLE IF NOT EXISTS' asegura que no haya un error
        # si la tabla ya ha sido creada.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS personas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
        """)
        print("Tabla 'personas' creada o ya existente.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")

def insertar_datos(conn):
    """
    Inserta un conjunto predefinido de personas en la tabla.
    Si una persona con el mismo email ya existe, no se insertará de nuevo
    gracias a la cláusula 'OR IGNORE'.
    :param conn: Objeto de conexión a la base de datos.
    """
    # Lista de tuplas, donde cada tupla representa una fila en la tabla.
    personas = [
        ('Juan', 'Perez', 'juan.perez@example.com'),
        ('Maria', 'Garcia', 'maria.garcia@example.com'),
        ('Pedro', 'Lopez', 'pedro.lopez@example.com'),
        ('Ana', 'Martinez', 'ana.martinez@example.com')
    ]
    try:
        cursor = conn.cursor()
        # 'executemany' es eficiente para insertar múltiples filas a la vez.
        # El '?' es un marcador de posición para prevenir inyección SQL.
        # 'INSERT OR IGNORE' evita errores si intentas insertar un email
        # que ya existe (debido a la restricción UNIQUE en la columna email).
        cursor.executemany("INSERT OR IGNORE INTO personas (nombre, apellido, email) VALUES (?, ?, ?)", personas)
        # conn.commit() guarda los cambios en la base de datos.
        conn.commit()
        print("Datos de ejemplo insertados.")
    except sqlite3.Error as e:
        print(f"Error al insertar datos: {e}")

def buscar_persona_por_apellido(conn, apellido):
    """
    Busca personas en la base de datos filtrando por su apellido.
    :param conn: Objeto de conexión a la base de datos.
    :param apellido: El apellido a buscar.
    :return: Una lista de filas que coinciden con la búsqueda.
    """
    try:
        cursor = conn.cursor()
        # Se usa un '?' para pasar el apellido de forma segura a la consulta.
        # Esto evita la inyección SQL, que es una vulnerabilidad de seguridad.
        cursor.execute("SELECT * FROM personas WHERE apellido = ?", (apellido,))

        # fetchall() recupera todas las filas del resultado de la consulta.
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error al buscar datos: {e}")
        return []

def main():
    """
    Función principal que orquesta la ejecución del script.
    """
    database = "clase.db"  # Nombre del archivo de la base de datos.

    # 1. Crear una conexión a la base de datos
    conn = crear_conexion(database)

    # Solo proceder si la conexión fue exitosa.
    if conn is not None:
        # 2. Crear la tabla (si es necesario)
        crear_tabla(conn)

        # 3. Insertar datos de ejemplo
        insertar_datos(conn)

        # --- Ejemplo de uso de la función de búsqueda ---
        print("\n--- Buscando personas ---")
        apellido_a_buscar = "Garcia"
        print(f"Buscando personas con el apellido: '{apellido_a_buscar}'")

        # 4. Realizar la búsqueda
        resultados = buscar_persona_por_apellido(conn, apellido_a_buscar)

        # 5. Procesar y mostrar los resultados
        if resultados:
            print("Resultados encontrados:")
            # Iteramos sobre la lista de resultados para mostrarlos.
            for persona in resultados:
                # Cada 'persona' es una tupla, accedemos a sus valores por índice.
                print(f"  ID: {persona[0]}, Nombre: {persona[1]}, Apellido: {persona[2]}, Email: {persona[3]}")
        else:
            print("No se encontraron personas con ese apellido.")

        # 6. Cerrar la conexión a la base de datos. Es importante hacerlo
        #    para liberar recursos.
        conn.close()
        print("\nConexión a la base de datos cerrada.")
    else:
        print("Error: No se pudo crear la conexión a la base de datos.")

# El bloque `if __name__ == '__main__':` asegura que la función `main()`
# solo se ejecute cuando el script es ejecutado directamente.
if __name__ == '__main__':
    main()
