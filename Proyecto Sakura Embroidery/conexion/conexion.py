import os

import psycopg2
import psycopg2.extras
from psycopg2 import Error

DATABASE_URL = os.environ.get("DATABASE_URL")

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "dbname": os.environ.get("DB_NAME", "sakura_embroidery_db"),
    "port": os.environ.get("DB_PORT", "5432"),
}

# Render exige SSL para conectarse a su PostgreSQL administrado
# desde fuera de su red interna. DB_SSLMODE permite desactivarlo
# (por ejemplo "disable") cuando se prueba contra un PostgreSQL
# local que no tiene SSL configurado.
DB_SSLMODE = os.environ.get("DB_SSLMODE", "require")


class ConexionPostgres:
    """
    Envoltorio delgado sobre una conexión psycopg2.

    Su único propósito es permitir seguir escribiendo
    `conexion.cursor(dictionary=True)` -tal como se hacía con
    mysql-connector-python- sin tener que modificar cada una de
    las consultas ya existentes en app.py y models.py al migrar
    el proyecto de MySQL a PostgreSQL. Cuando dictionary=True se
    entrega un cursor que devuelve cada fila como diccionario
    (psycopg2.extras.RealDictCursor), igual que hacía MySQL.
    """

    def __init__(self, conexion_psycopg2):
        self._conexion = conexion_psycopg2

    def cursor(self, dictionary=False):
        if dictionary:
            return self._conexion.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )
        return self._conexion.cursor()

    def commit(self):
        self._conexion.commit()

    def rollback(self):
        self._conexion.rollback()

    def close(self):
        self._conexion.close()


def obtener_conexion():
    """
    Crea y retorna una nueva conexión hacia la base de datos
    PostgreSQL.

    Se crea una conexión nueva por cada operación (en lugar de
    mantener una conexión global) para poder cerrarla siempre de
    forma explícita después de cada consulta, tal como lo exige
    la actividad.

    Retorna:
        ConexionPostgres si la conexión fue exitosa, o None si
        ocurrió un error.
    """

    try:
        if DATABASE_URL:
            conexion_real = psycopg2.connect(
                DATABASE_URL,
                sslmode=DB_SSLMODE,
            )
        else:
            conexion_real = psycopg2.connect(**DB_CONFIG)

        return ConexionPostgres(conexion_real)

    except Error as error:
        print(f"[ERROR] No se pudo conectar a la base de datos: {error}")
        return None