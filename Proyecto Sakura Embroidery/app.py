import os

from flask import Flask, render_template, redirect, url_for, flash, request
from dotenv import load_dotenv
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm

from conexion.conexion import obtener_conexion, inicializar_base_datos
from models import Usuario

load_dotenv()


# ==============================
# CONFIGURACIÓN DE FLASK
# ==============================

app = Flask(__name__)

# La SECRET_KEY se lee de la variable de entorno definida en .env;
# el segundo argumento es solo un valor de respaldo para desarrollo.
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "sakura-embroidery-clave-secreta"
)


# Crea las tablas (si todavía no existen) apenas arranca la app,
# tanto en desarrollo local como en Render. Así no hace falta
# ejecutar sql/esquema.sql a mano con psql.
inicializar_base_datos()


# ==============================
# CONFIGURACIÓN DE FLASK-LOGIN
# ==============================

login_manager = LoginManager()
login_manager.init_app(app)

# Página a la que se redirige automáticamente cuando un usuario no
# autenticado intenta acceder a una ruta protegida con @login_required.
login_manager.login_view = "login"
login_manager.login_message = "Debe iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(id_usuario):
    """
    Flask-Login llama a esta función en cada solicitud para
    reconstruir el objeto de usuario a partir del id almacenado
    en la sesión (cookie firmada con SECRET_KEY).
    """

    return Usuario.obtener_por_id(int(id_usuario))


# ==============================
# DATOS DE LA EMPRESA
# ==============================

nombre_empresa = "Sakura Embroidery"


# ==============================
# FUNCIONES AUXILIARES
# (listas de opciones para los SelectField relacionados
# mediante llave foránea)
# ==============================

def obtener_choices_proveedores():
    """Devuelve la lista de proveedores como choices para un SelectField."""

    choices = [(0, "Seleccione un proveedor")]

    conexion = obtener_conexion()

    if conexion is None:
        return choices

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
    """)

    for fila in cursor.fetchall():
        choices.append((fila["id_proveedor"], fila["nombre"]))

    cursor.close()
    conexion.close()

    return choices


def obtener_choices_clientes():
    """Devuelve la lista de clientes como choices para un SelectField."""

    choices = [(0, "Seleccione un cliente")]

    conexion = obtener_conexion()

    if conexion is None:
        return choices

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_cliente, nombre
        FROM clientes
        ORDER BY nombre
    """)

    for fila in cursor.fetchall():
        choices.append((fila["id_cliente"], fila["nombre"]))

    cursor.close()
    conexion.close()

    return choices


# ==============================
# PÁGINA PRINCIPAL
# ==============================

@app.route("/")
def inicio():

    return render_template(
        "index.html",
        nombre_empresa=nombre_empresa
    )


# ==============================================================
# MÓDULO AUTENTICACIÓN
# (registro, login, logout y panel privado)
# ==============================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    # Si ya hay una sesión activa, no tiene sentido volver a registrarse.
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = UsuarioForm()

    if form.validate_on_submit():

        # La contraseña se transforma a hash ANTES de tocar la base
        # de datos; nunca se guarda ni se envía en texto plano.
        password_hash = generate_password_hash(form.password.data)

        creado = Usuario.crear(form.usuario.data, password_hash)

        if creado:
            flash("Usuario registrado correctamente. Ya puede iniciar sesión.", "success")
            return redirect(url_for("login"))

        flash("No se pudo completar el registro. Intente nuevamente.", "danger")

    return render_template(
        "registro.html",
        form=form
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        fila = Usuario.obtener_por_nombre(form.usuario.data)

        # No se compara la contraseña escrita directamente con el
        # valor almacenado: se usa check_password_hash() sobre el
        # hash guardado en la base de datos.
        if fila and check_password_hash(fila["password"], form.password.data):

            usuario_autenticado = Usuario(fila["id_usuario"], fila["usuario"])
            login_user(usuario_autenticado)

            flash(f"Bienvenido, {usuario_autenticado.usuario}.", "success")

            # Si el usuario fue redirigido al login desde una página
            # protegida, se lo regresa allí después de autenticarse.
            siguiente = request.args.get("next")
            return redirect(siguiente or url_for("dashboard"))

        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template(
        "login.html",
        form=form
    )


@app.route("/logout")
@login_required
def logout():

    logout_user()
    flash("Sesión cerrada correctamente.", "success")

    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        nombre_empresa=nombre_empresa
    )


# ==============================================================
# MÓDULO PRODUCTOS
# (módulo con las 4 operaciones completas: listar, agregar,
# modificar, eliminar, todas ejecutadas directamente sobre
# PostgreSQL)
# ==============================================================

@app.route("/productos")
@login_required
def productos():

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return render_template("productos.html", productos=[])

    cursor = conexion.cursor(dictionary=True)

    # Consulta con JOIN: relaciona productos con su proveedor
    # a través de la clave foránea id_proveedor.
    cursor.execute("""
        SELECT
            p.id_producto,
            p.nombre,
            p.categoria,
            p.precio,
            p.stock,
            pr.nombre AS nombre_proveedor
        FROM productos p
        JOIN proveedores pr ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto DESC
    """)

    lista_productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=lista_productos
    )


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():

    form = ProductoForm()
    form.id_proveedor.choices = obtener_choices_proveedores()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:
            flash("No se pudo conectar con la base de datos.", "danger")
            return redirect(url_for("productos"))

        cursor = conexion.cursor()

        # INSERT parametrizado (evita inyección SQL).
        cursor.execute("""
            INSERT INTO productos
            (nombre, categoria, precio, stock, id_proveedor)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Producto registrado correctamente.", "success")

        return redirect(url_for("productos"))

    return render_template(
        "formulario.html",
        form=form,
        titulo="Registrar producto",
        modulo="Producto"
    )


@app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
@login_required
def editar_producto(id_producto):

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return redirect(url_for("productos"))

    cursor = conexion.cursor(dictionary=True)

    # Se recupera primero el registro seleccionado mediante su id.
    cursor.execute("""
        SELECT id_producto, nombre, categoria, precio, stock, id_proveedor
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    if producto is None:
        flash("El producto solicitado no existe.", "warning")
        return redirect(url_for("productos"))

    form = ProductoForm()
    form.id_proveedor.choices = obtener_choices_proveedores()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:
            flash("No se pudo conectar con la base de datos.", "danger")
            return redirect(url_for("productos"))

        cursor = conexion.cursor()

        # UPDATE parametrizado, siempre con WHERE para modificar
        # únicamente el registro seleccionado.
        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data,
            id_producto
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Producto actualizado correctamente.", "success")

        return redirect(url_for("productos"))

    # En método GET se precargan los datos actuales en el formulario.
    if request.method == "GET":
        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]
        form.id_proveedor.data = producto["id_proveedor"]

    return render_template(
        "formulario.html",
        form=form,
        titulo="Editar producto",
        modulo="Producto"
    )


@app.route("/productos/eliminar/<int:id_producto>", methods=["POST"])
@login_required
def eliminar_producto(id_producto):

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return redirect(url_for("productos"))

    cursor = conexion.cursor()

    # DELETE parametrizado con WHERE: elimina únicamente
    # el registro seleccionado.
    cursor.execute("""
        DELETE FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Producto eliminado correctamente.", "success")

    return redirect(url_for("productos"))


# ==============================================================
# MÓDULO CLIENTES
# ==============================================================

@app.route("/clientes")
@login_required
def clientes():

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return render_template("clientes.html", clientes=[])

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_cliente, nombre, telefono, correo
        FROM clientes
        ORDER BY id_cliente DESC
    """)

    lista_clientes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "clientes.html",
        clientes=lista_clientes
    )


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:
            flash("No se pudo conectar con la base de datos.", "danger")
            return redirect(url_for("clientes"))

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO clientes (nombre, telefono, correo)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Cliente registrado correctamente.", "success")

        return redirect(url_for("clientes"))

    return render_template(
        "formulario.html",
        form=form,
        titulo="Registrar cliente",
        modulo="Cliente"
    )


@app.route("/clientes/editar/<int:id_cliente>", methods=["GET", "POST"])
@login_required
def editar_cliente(id_cliente):

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return redirect(url_for("clientes"))

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_cliente, nombre, telefono, correo
        FROM clientes
        WHERE id_cliente = %s
    """, (id_cliente,))

    cliente = cursor.fetchone()

    cursor.close()
    conexion.close()

    if cliente is None:
        flash("El cliente solicitado no existe.", "warning")
        return redirect(url_for("clientes"))

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:
            flash("No se pudo conectar con la base de datos.", "danger")
            return redirect(url_for("clientes"))

        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE clientes
            SET nombre = %s,
                telefono = %s,
                correo = %s
            WHERE id_cliente = %s
        """, (
            form.nombre.data,
            form.telefono.data,
            form.correo.data,
            id_cliente
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Cliente actualizado correctamente.", "success")

        return redirect(url_for("clientes"))

    if request.method == "GET":
        form.nombre.data = cliente["nombre"]
        form.telefono.data = cliente["telefono"]
        form.correo.data = cliente["correo"]

    return render_template(
        "formulario.html",
        form=form,
        titulo="Editar cliente",
        modulo="Cliente"
    )


@app.route("/clientes/eliminar/<int:id_cliente>", methods=["POST"])
@login_required
def eliminar_cliente(id_cliente):

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return redirect(url_for("clientes"))

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id_cliente = %s
    """, (id_cliente,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Cliente eliminado correctamente.", "success")

    return redirect(url_for("clientes"))


# ==============================================================
# MÓDULO PROVEEDORES
# ==============================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return render_template("proveedores.html", proveedores=[])

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_proveedor, nombre, producto, telefono
        FROM proveedores
        ORDER BY id_proveedor DESC
    """)

    lista_proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "proveedores.html",
        proveedores=lista_proveedores
    )


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:
            flash("No se pudo conectar con la base de datos.", "danger")
            return redirect(url_for("proveedores"))

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO proveedores (nombre, producto, telefono)
            VALUES (%s, %s, %s)
        """, (
            form.nombre.data,
            form.producto.data,
            form.telefono.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Proveedor registrado correctamente.", "success")

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario.html",
        form=form,
        titulo="Registrar proveedor",
        modulo="Proveedor"
    )


@app.route("/proveedores/editar/<int:id_proveedor>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id_proveedor):

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return redirect(url_for("proveedores"))

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_proveedor, nombre, producto, telefono
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id_proveedor,))

    proveedor = cursor.fetchone()

    cursor.close()
    conexion.close()

    if proveedor is None:
        flash("El proveedor solicitado no existe.", "warning")
        return redirect(url_for("proveedores"))

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:
            flash("No se pudo conectar con la base de datos.", "danger")
            return redirect(url_for("proveedores"))

        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                producto = %s,
                telefono = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.producto.data,
            form.telefono.data,
            id_proveedor
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Proveedor actualizado correctamente.", "success")

        return redirect(url_for("proveedores"))

    if request.method == "GET":
        form.nombre.data = proveedor["nombre"]
        form.producto.data = proveedor["producto"]
        form.telefono.data = proveedor["telefono"]

    return render_template(
        "formulario.html",
        form=form,
        titulo="Editar proveedor",
        modulo="Proveedor"
    )


@app.route("/proveedores/eliminar/<int:id_proveedor>", methods=["POST"])
@login_required
def eliminar_proveedor(id_proveedor):

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return redirect(url_for("proveedores"))

    cursor = conexion.cursor()

    # Nota: si el proveedor tiene productos asociados, la base de
    # datos rechazará la eliminación (ON DELETE RESTRICT) para
    # proteger la integridad referencial.
    try:
        cursor.execute("""
            DELETE FROM proveedores
            WHERE id_proveedor = %s
        """, (id_proveedor,))

        conexion.commit()
        flash("Proveedor eliminado correctamente.", "success")

    except Exception:
        conexion.rollback()
        flash(
            "No se puede eliminar: el proveedor tiene productos asociados.",
            "danger"
        )

    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("proveedores"))


# ==============================================================
# MÓDULO FACTURACIÓN
# ==============================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return render_template("facturacion.html", facturas=[])

    cursor = conexion.cursor(dictionary=True)

    # JOIN entre facturas y clientes a través de la clave foránea.
    cursor.execute("""
        SELECT
            f.id_factura,
            f.numero,
            c.nombre AS cliente,
            f.fecha,
            f.total,
            f.estado
        FROM facturas f
        JOIN clientes c ON f.id_cliente = c.id_cliente
        ORDER BY f.id_factura DESC
    """)

    lista_facturas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "facturacion.html",
        facturas=lista_facturas
    )


@app.route("/facturacion/nueva", methods=["GET", "POST"])
@login_required
def nueva_factura():

    form = FacturacionForm()
    form.id_cliente.choices = obtener_choices_clientes()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:
            flash("No se pudo conectar con la base de datos.", "danger")
            return redirect(url_for("facturacion"))

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO facturas (numero, id_cliente, fecha, total, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.numero.data,
            form.id_cliente.data,
            form.fecha.data,
            form.total.data,
            form.estado.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Factura registrada correctamente.", "success")

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario.html",
        form=form,
        titulo="Registrar factura",
        modulo="Facturación"
    )


@app.route("/facturacion/editar/<int:id_factura>", methods=["GET", "POST"])
@login_required
def editar_factura(id_factura):

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return redirect(url_for("facturacion"))

    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT id_factura, numero, id_cliente, fecha, total, estado
        FROM facturas
        WHERE id_factura = %s
    """, (id_factura,))

    factura = cursor.fetchone()

    cursor.close()
    conexion.close()

    if factura is None:
        flash("La factura solicitada no existe.", "warning")
        return redirect(url_for("facturacion"))

    form = FacturacionForm()
    form.id_cliente.choices = obtener_choices_clientes()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        if conexion is None:
            flash("No se pudo conectar con la base de datos.", "danger")
            return redirect(url_for("facturacion"))

        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE facturas
            SET numero = %s,
                id_cliente = %s,
                fecha = %s,
                total = %s,
                estado = %s
            WHERE id_factura = %s
        """, (
            form.numero.data,
            form.id_cliente.data,
            form.fecha.data,
            form.total.data,
            form.estado.data,
            id_factura
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Factura actualizada correctamente.", "success")

        return redirect(url_for("facturacion"))

    if request.method == "GET":
        form.numero.data = factura["numero"]
        form.id_cliente.data = factura["id_cliente"]
        form.fecha.data = factura["fecha"]
        form.total.data = factura["total"]
        form.estado.data = factura["estado"]

    return render_template(
        "formulario.html",
        form=form,
        titulo="Editar factura",
        modulo="Facturación"
    )


@app.route("/facturacion/eliminar/<int:id_factura>", methods=["POST"])
@login_required
def eliminar_factura(id_factura):

    conexion = obtener_conexion()

    if conexion is None:
        flash("No se pudo conectar con la base de datos.", "danger")
        return redirect(url_for("facturacion"))

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM facturas
        WHERE id_factura = %s
    """, (id_factura,))

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Factura eliminada correctamente.", "success")

    return redirect(url_for("facturacion"))


# ==============================
# EJECUTAR APLICACIÓN
# ==============================

if __name__ == "__main__":
    modo_debug = os.environ.get("FLASK_DEBUG", "True") == "True"
    app.run(debug=modo_debug)