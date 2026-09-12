import os
import mysql.connector
from mysql.connector import Error

# ==========================================================
# CONFIGURACIÓN DE LA BASE DE DATOS (MySQL)
# ==========================================================

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "132109xdlolggaa"),
    "database": os.environ.get("DB_NAME", "sakura_embroidery_db"),
}


def obtener_conexion():
    """
    Crea y retorna una nueva conexión hacia la base de datos MySQL.

    Se crea una conexión nueva por cada operación (en lugar de
    mantener una conexión global) para poder cerrarla siempre de
    forma explícita después de cada consulta, tal como lo exige
    la actividad.

    Retorna:
        mysql.connector.connection.MySQLConnection si la conexión
        fue exitosa, o None si ocurrió un error.
    """

    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion

    except Error as error:
        print(f"[ERROR] No se pudo conectar a la base de datos: {error}")
        return None
