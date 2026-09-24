import os

import psycopg2
import psycopg2.extras
from psycopg2 import Error


# ==========================================================
# CONFIGURACIÓN DE LA BASE DE DATOS (PostgreSQL)
# ==========================================================
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


# ==========================================================
# INICIALIZACIÓN AUTOMÁTICA DE LAS TABLAS
# ==========================================================

def _leer_sentencias_sql(ruta_archivo):
    """
    Lee un archivo .sql y lo separa en sentencias individuales,
    ignorando las líneas de comentario (las que empiezan con "--").
    """

    with open(ruta_archivo, encoding="utf-8") as archivo:
        lineas_utiles = [
            linea for linea in archivo
            if not linea.strip().startswith("--")
        ]

    contenido = "".join(lineas_utiles)

    return [
        sentencia.strip()
        for sentencia in contenido.split(";")
        if sentencia.strip()
    ]


def inicializar_base_datos():
    """
    Crea las tablas del proyecto (si todavía no existen) ejecutando
    sql/esquema.sql automáticamente al arrancar la aplicación.

    Esto evita depender de que alguien ejecute el script a mano con
    psql: tanto en desarrollo local (`python app.py`) como en Render
    (cada vez que el servicio arranca), la base de datos queda lista
    sin pasos manuales adicionales. Es seguro llamarla más de una
    vez -el script usa "IF NOT EXISTS" / "WHERE NOT EXISTS"- así que
    no falla ni duplica datos si las tablas ya existían.
    """

    raiz_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_esquema = os.path.join(raiz_proyecto, "sql", "esquema.sql")

    if not os.path.exists(ruta_esquema):
        print(
            "[AVISO] No se encontró sql/esquema.sql; se omite la "
            "inicialización automática de la base de datos."
        )
        return

    conexion = obtener_conexion()

    if conexion is None:
        print(
            "[AVISO] No se pudo conectar a la base de datos para "
            "inicializarla. Revise DATABASE_URL o DB_HOST/DB_USER/"
            "DB_PASSWORD/DB_NAME."
        )
        return

    try:
        sentencias = _leer_sentencias_sql(ruta_esquema)
        cursor = conexion.cursor()

        for sentencia in sentencias:
            cursor.execute(sentencia)

        conexion.commit()
        cursor.close()

        print(
            f"[OK] Base de datos verificada/inicializada "
            f"({len(sentencias)} sentencias ejecutadas)."
        )

    except Exception as error:
        conexion.rollback()
        print(f"[ERROR] No se pudo inicializar la base de datos: {error}")

    finally:
        conexion.close()
