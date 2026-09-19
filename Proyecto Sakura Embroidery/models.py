"""
Modelo de Usuario para el sistema de autenticación.

Este módulo define la clase Usuario, compatible con Flask-Login
mediante UserMixin, y las operaciones necesarias contra la base
de datos (MySQL) para registrar usuarios y validar credenciales.
"""

from conexion.conexion import obtener_conexion

from flask_login import UserMixin


class Usuario(UserMixin):
    """
    Representa a un usuario autenticado del sistema.

    Flask-Login solo necesita un objeto con un identificador
    (atributo/propiedad `id`) para poder mantener la sesión; el
    resto de los atributos se añaden para poder mostrarlos en la
    interfaz (por ejemplo, el nombre de usuario en el navbar).
    """

    def __init__(self, id_usuario, usuario):
        self.id = id_usuario
        self.usuario = usuario

    # ----------------------------------------------------------------
    # Métodos de acceso a datos (todas las consultas son parametrizadas)
    # ----------------------------------------------------------------

    @staticmethod
    def obtener_por_id(id_usuario):
        """
        Recupera un usuario según su id.

        Utilizado por la función load_user() de Flask-Login para
        reconstruir el usuario a partir del identificador guardado
        en la sesión.
        """

        conexion = obtener_conexion()

        if conexion is None:
            return None

        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_usuario, usuario
            FROM usuarios
            WHERE id_usuario = %s
        """, (id_usuario,))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila is None:
            return None

        return Usuario(fila["id_usuario"], fila["usuario"])

    @staticmethod
    def obtener_por_nombre(nombre_usuario):
        """
        Recupera el registro completo (incluida la contraseña con
        hash) según el nombre de usuario.

        Se utiliza únicamente durante el login, ya que se necesita
        el hash almacenado para poder compararlo con
        check_password_hash().
        """

        conexion = obtener_conexion()

        if conexion is None:
            return None

        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_usuario, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (nombre_usuario,))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        return fila

    @staticmethod
    def existe(nombre_usuario):
        """Comprueba si ya existe un usuario con ese nombre."""

        conexion = obtener_conexion()

        if conexion is None:
            return False

        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_usuario
            FROM usuarios
            WHERE usuario = %s
        """, (nombre_usuario,))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        return fila is not None

    @staticmethod
    def crear(nombre_usuario, password_hash):
        """
        Registra un nuevo usuario mediante un INSERT parametrizado.

        La contraseña ya debe llegar convertida a hash (generada
        con generate_password_hash en app.py); este método nunca
        recibe ni almacena texto plano.

        Retorna True si el usuario fue creado, o False si ocurrió
        un error (por ejemplo, sin conexión o nombre duplicado por
        una condición de carrera, protegida por el UNIQUE de la
        base de datos además de la validación del formulario).
        """

        conexion = obtener_conexion()

        if conexion is None:
            return False

        cursor = conexion.cursor()

        try:
            cursor.execute("""
                INSERT INTO usuarios (usuario, password)
                VALUES (%s, %s)
            """, (nombre_usuario, password_hash))

            conexion.commit()
            return True

        except Exception:
            conexion.rollback()
            return False

        finally:
            cursor.close()
            conexion.close()